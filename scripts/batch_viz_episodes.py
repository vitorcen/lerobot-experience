#!/usr/bin/env python3
"""批量可视化指定范围的 episodes，生成 .rrd 文件供本地查看"""
import subprocess
import sys

REPO_ID = "lerobot/robotwin_unified"
START_EP = 0
END_EP = 10   # 不包含，即 0~9
OUTPUT_DIR = "./viz_outputs"

for ep in range(START_EP, END_EP):
    print(f"[episode {ep}] 生成 .rrd ...")
    subprocess.run([
        "python", "lerobot/src/lerobot/scripts/lerobot_dataset_viz.py",
        f"--repo-id={REPO_ID}",
        f"--episode-index={ep}",
        "--save=1",
        f"--output-dir={OUTPUT_DIR}",
    ])
    print(f"[episode {ep}] 完成\n")

print(f"全部完成。用以下命令在本地查看：")
print(f"  rerun {OUTPUT_DIR}/*.rrd")
