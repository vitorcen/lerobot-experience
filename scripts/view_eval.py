#!/usr/bin/env python3
"""Generate an HTML viewer for evaluation results and open it via local HTTP server."""
import argparse
import json
import webbrowser
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from threading import Thread


def find_latest_eval(base: Path) -> Path:
    candidates = sorted(base.rglob("eval_info.json"))
    if not candidates:
        raise FileNotFoundError(f"No eval_info.json found under {base}")
    return candidates[-1].parent


def build_html(eval_dir: Path) -> str:
    info = json.loads((eval_dir / "eval_info.json").read_text())
    overall = info["overall"]

    rows = []
    for t in info.get("per_task", []):
        tg, tid = t["task_group"], t["task_id"]
        m = t["metrics"]
        cells = []
        for i, (ok, vp) in enumerate(zip(m["successes"], m["video_paths"])):
            vpath = Path(vp)
            # relative to eval_dir
            rel = vpath.relative_to(tg) if tg in vpath.parts else vpath
            # just use the tail: suite_taskid/episode.mp4
            parts = vpath.parts
            if len(parts) >= 2:
                rel_url = f"videos/{parts[-2]}/{parts[-1]}"
            else:
                rel_url = f"videos/{vpath.name}"
            mark = "✓" if ok else "✗"
            cls = "pass" if ok else "fail"
            cells.append(
                f'<td><span class="{cls}">{mark}</span><br>'
                f'<video src="{rel_url}" controls muted preload="none"></video></td>'
            )
        n_ok = sum(m["successes"])
        rows.append(
            f"<h3>{tg} task {tid} — {n_ok}/{len(m['successes'])}</h3>"
            f'<table><tr>{"".join(cells)}</tr></table>'
        )

    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>{eval_dir.name}</title>
<style>
  body {{ font-family: sans-serif; margin: 24px; background: #fafafa; }}
  h2 {{ margin-bottom: 4px; }}
  table {{ border-collapse: collapse; margin: 8px 0 24px; }}
  td, th {{ border: 1px solid #ddd; padding: 6px; text-align: center; }}
  th {{ background: #f0f0f0; }}
  .pass {{ color: #1a7f37; font-weight: bold; font-size: 1.4em; }}
  .fail {{ color: #aaa; font-size: 1.4em; }}
  video {{ max-width: 300px; display: block; margin-top: 4px; }}
  .summary {{ font-size: 1.1em; margin: 12px 0; }}
</style></head><body>
<h2>{eval_dir.name}</h2>
<p class="summary">Overall: <b>{overall["pc_success"]:.1f}%</b> success
({overall["n_episodes"]} episodes, {overall["eval_s"]:.0f}s)</p>
{"".join(rows)}
</body></html>"""


def main():
    p = argparse.ArgumentParser(description="View evaluation results in browser")
    p.add_argument("eval_dir", nargs="?", default=None,
                   help="Evaluation output directory (default: latest under outputs/eval)")
    p.add_argument("--port", type=int, default=8765, help="HTTP server port")
    args = p.parse_args()

    base = Path("outputs/eval")
    eval_dir = Path(args.eval_dir) if args.eval_dir else find_latest_eval(base)
    eval_dir = eval_dir.resolve()

    if not (eval_dir / "eval_info.json").exists():
        raise FileNotFoundError(f"eval_info.json not found in {eval_dir}")

    html = build_html(eval_dir)
    (eval_dir / "eval_result.html").write_text(html)

    handler = partial(SimpleHTTPRequestHandler, directory=str(eval_dir))
    server = HTTPServer(("127.0.0.1", args.port), handler)
    url = f"http://127.0.0.1:{args.port}/eval_result.html"

    print(f"Serving at {url}")
    print(f"Press Ctrl+C to stop.")
    webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
        server.server_close()


if __name__ == "__main__":
    main()
