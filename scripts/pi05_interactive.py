#!/usr/bin/env python3
"""Quick Pi0.5 prompt test — run a single LIBERO episode and save video."""
import argparse
import subprocess
import sys
import time
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description="Pi0.5 interactive prompt test")
    p.add_argument("--prompt", default="pick up the red block", help="Language instruction")
    p.add_argument("--task", default="libero_spatial", help="LIBERO suite: libero_spatial/object/goal/10")
    p.add_argument("--policy", default="lerobot/pi05_libero_finetuned", help="HF model ID or local path")
    p.add_argument("--device", default="cuda", help="cuda or cpu")
    args = p.parse_args()

    ts = time.strftime("%Y%m%d_%H%M%S")
    out = Path(f"outputs/eval/pi05_interactive_{ts}")

    cmd = [
        sys.executable, "lerobot/src/lerobot/scripts/lerobot_eval.py",
        f"--policy.path={args.policy}",
        f"--env.type=libero",
        f"--env.task={args.task}",
        "--eval.batch_size=1",
        "--eval.n_episodes=1",
        f"--policy.device={args.device}",
        f"--output_dir={out}",
    ]

    print(f"Prompt: {args.prompt}")
    print(f"Task:   {args.task}")
    print(f"Output: {out}\n")

    r = subprocess.run(cmd)
    if r.returncode == 0:
        print(f"\n✅ Done → python scripts/view_eval.py {out}")
    else:
        print("\n❌ Failed", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
