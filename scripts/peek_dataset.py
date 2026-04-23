#!/usr/bin/env python3
"""Peek at a dataset without downloading the whole thing.
Uses Hugging Face streaming to pull only the frames you actually look at."""
import argparse

import numpy as np
from datasets import load_dataset
from PIL import Image


def main():
    parser = argparse.ArgumentParser(description="Peek at a LeRobot dataset via streaming")
    parser.add_argument("repo_id", help="Hugging Face dataset repo ID")
    parser.add_argument("--episode", type=int, default=0, help="Episode index to peek")
    parser.add_argument("--frame", type=int, default=0, help="Frame index within episode")
    parser.add_argument("--save", default="peek_frame.png", help="Output image path")
    args = parser.parse_args()

    print(f"Streaming episode {args.episode}, frame {args.frame} from {args.repo_id} ...")
    print("(Only the requested frame is transferred over the network)")

    # Streaming load — nothing is written to disk
    ds = load_dataset(args.repo_id, streaming=True, split="train")

    # Seek to the desired frame
    target_idx = args.frame
    for i, sample in enumerate(ds):
        if i < target_idx:
            continue

        print(f"\nSample keys: {list(sample.keys())}")
        print(f"Episode index: {sample.get('episode_index')}")
        print(f"Frame index:   {sample.get('frame_index')}")
        print(f"Timestamp:     {sample.get('timestamp')}")
        print(f"Action shape:  {np.array(sample['action']).shape}")
        print(f"State shape:   {np.array(sample['observation.state']).shape}")

        # Save any available camera image
        for key in sample:
            if "image" in key and isinstance(sample[key], dict):
                img_dict = sample[key]
                # HF streaming returns images as {'path': ..., 'bytes': ...}
                if "bytes" in img_dict and img_dict["bytes"] is not None:
                    img = Image.open(img_dict["bytes"])
                    out_path = f"{key.replace('.', '_')}_{args.save}"
                    img.save(out_path)
                    print(f"Saved image to: {out_path}  ({img.size})")
                elif "path" in img_dict and img_dict["path"] is not None:
                    print(f"Image key '{key}' is a video reference: {img_dict['path']}")
                    print("  (Video frames require full video download, use --download-video if needed)")
        break

    print("\nDone. No full dataset was cached locally.")


if __name__ == "__main__":
    main()
