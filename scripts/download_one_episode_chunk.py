#!/usr/bin/env python3
"""Download only the data/video chunks needed for a single episode, then preview."""
import argparse
import json
import sys
import time
from pathlib import Path

from huggingface_hub import hf_hub_download, list_repo_files, list_repo_tree
from huggingface_hub.errors import EntryNotFoundError


def download_with_retry(fn, retries=3, delay=2, **kwargs):
    """Wrapper with retry for unstable network (especially behind SOCKS proxy)."""
    last_err = None
    for attempt in range(1, retries + 1):
        try:
            return fn(**kwargs)
        except Exception as e:
            last_err = e
            print(f"  [attempt {attempt}/{retries}] failed: {e}")
            if attempt < retries:
                print(f"  retrying in {delay}s...")
                time.sleep(delay)
    raise last_err


def download_meta_files(repo_id: str, local_dir: Path):
    """Download all files under meta/ directory."""
    print("[1/4] Downloading meta/ files ...")
    files = download_with_retry(list_repo_files, repo_id=repo_id, repo_type="dataset")
    meta_files = [f for f in files if f.startswith("meta/")]
    for f in meta_files:
        download_with_retry(
            hf_hub_download,
            repo_id=repo_id,
            filename=f,
            repo_type="dataset",
            local_dir=local_dir,
        )


def list_files_in_dir(repo_id: str, path_in_repo: str, repo_type: str = "dataset"):
    """List files under a specific directory in the repo."""
    try:
        items = list(list_repo_tree(repo_id, repo_type=repo_type, path_in_repo=path_in_repo))
        return [item.path for item in items if not item.path.endswith("/")]
    except Exception:
        return []


def read_episode_row(meta_dir: Path, episode: int, chunk_size: int):
    """Read episode metadata from all parquet files in the episode chunk directory."""
    import pandas as pd

    ep_chunk_idx = episode // chunk_size
    ep_dir = meta_dir / "meta" / "episodes" / f"chunk-{ep_chunk_idx:03d}"
    if not ep_dir.exists():
        raise FileNotFoundError(f"Episode metadata directory not found: {ep_dir}")

    parquet_files = sorted(ep_dir.glob("*.parquet"))
    if not parquet_files:
        raise FileNotFoundError(f"No episode metadata parquet files in: {ep_dir}")

    df = pd.concat([pd.read_parquet(f) for f in parquet_files], ignore_index=True)
    ep_row = df[df["episode_index"] == episode]
    if len(ep_row) == 0:
        raise ValueError(f"Episode {episode} not found in metadata")
    return ep_row.iloc[0]


def download_or_fallback(repo_id: str, filename: str, local_dir: Path, label: str = "file"):
    """Download a file; if it doesn't exist, list the directory and download all matching files."""
    try:
        download_with_retry(
            hf_hub_download,
            repo_id=repo_id,
            filename=filename,
            repo_type="dataset",
            local_dir=local_dir,
        )
        return
    except EntryNotFoundError:
        pass  # fall through to directory listing

    # Expected file not found — list directory and grab everything relevant
    dir_path = str(Path(filename).parent)
    ext = Path(filename).suffix
    print(f"  Expected {label} not found ({filename}). Listing {dir_path}/ ...")
    files = list_files_in_dir(repo_id, dir_path)
    matches = [f for f in files if f.endswith(ext)]
    if not matches:
        raise FileNotFoundError(f"No {ext} files found in {dir_path}/")

    print(f"  Found {len(matches)} alternate {label}(s): {matches}")
    for f in matches:
        download_with_retry(
            hf_hub_download,
            repo_id=repo_id,
            filename=f,
            repo_type="dataset",
            local_dir=local_dir,
        )


def main():
    parser = argparse.ArgumentParser(description="Download chunks for one episode and preview")
    parser.add_argument("repo_id", help="HF dataset repo ID")
    parser.add_argument("--episode", type=int, default=0)
    parser.add_argument("--root", default="./peek_cache", help="Local cache dir")
    args = parser.parse_args()

    root = Path(args.root) / args.repo_id
    root.mkdir(parents=True, exist_ok=True)

    # 1. Download all meta files
    download_meta_files(args.repo_id, root)

    # 2. Read info.json
    info_path = root / "meta" / "info.json"
    with open(info_path) as f:
        info = json.load(f)

    total_ep = info["total_episodes"]
    chunk_size = info.get("chunks_size", 1000)
    data_path_tmpl = info["data_path"]
    video_path_tmpl = info.get("video_path")
    video_keys = [k for k, v in info["features"].items() if v.get("dtype") == "video"]

    if args.episode >= total_ep:
        raise ValueError(f"Episode {args.episode} >= total {total_ep}")

    # 3. Read episode metadata
    print("[2/4] Reading episode index ...")
    ep_row = read_episode_row(root, args.episode, chunk_size)

    data_chunk = int(ep_row["data/chunk_index"])
    data_file = int(ep_row["data/file_index"])

    # 4. Download data chunk
    data_fname = data_path_tmpl.format(chunk_index=data_chunk, file_index=data_file)
    print(f"[3/4] Downloading data chunk: {data_fname} ...")
    download_or_fallback(args.repo_id, data_fname, root, label="data")

    # 5. Download video chunks
    if video_path_tmpl:
        for vk in video_keys:
            vid_chunk = int(ep_row[f"videos/{vk}/chunk_index"])
            vid_file = int(ep_row[f"videos/{vk}/file_index"])
            vid_fname = video_path_tmpl.format(
                video_key=vk, chunk_index=vid_chunk, file_index=vid_file
            )
            print(f"[4/4] Downloading video chunk: {vid_fname} ...")
            download_or_fallback(args.repo_id, vid_fname, root, label="video")

    print(f"\nDone. Episode {args.episode} chunks cached in: {root}")

    # 6. Preview — use Python API directly
    print("\nLaunching preview ...")
    sys.path.insert(0, str(Path(__file__).parent.parent / "lerobot" / "src"))
    from lerobot.datasets import LeRobotDataset
    from lerobot.scripts.lerobot_dataset_viz import visualize_dataset

    dataset = LeRobotDataset(
        args.repo_id,
        episodes=[args.episode],
        root=str(root),
        tolerance_s=1e-4,
    )
    visualize_dataset(dataset, episode_index=args.episode)


if __name__ == "__main__":
    main()
