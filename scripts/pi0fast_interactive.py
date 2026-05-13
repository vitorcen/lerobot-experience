#!/usr/bin/env python3
"""Quick Pi0-FAST prompt test — run a single episode and save video."""
import argparse
import subprocess
import sys
import time
from pathlib import Path

# Pi0-FAST 预训练模型 + 对应环境
MODELS = {
    "libero": {"policy": "lerobot/pi0fast-libero", "env": "libero", "task": "libero_spatial"},
}


def main():
    p = argparse.ArgumentParser(description="Pi0-FAST interactive prompt test")
    p.add_argument("--prompt", default="pick up the red block", help="Language instruction")
    p.add_argument("--env", default="libero", choices=list(MODELS.keys()), help="Environment preset")
    p.add_argument("--task", default=None, help="Override task (default: use preset)")
    p.add_argument("--policy", default=None, help="Override HF model ID or local path")
    p.add_argument("--device", default="cuda", help="cuda or cpu")
    args = p.parse_args()

    preset = MODELS[args.env]
    policy = args.policy or preset["policy"]
    task = args.task or preset["task"]
    env_type = preset["env"]

    ts = time.strftime("%Y%m%d_%H%M%S")
    out = Path(f"outputs/eval/pi0fast_{args.env}_{ts}")

    cmd = [
        sys.executable, "lerobot/src/lerobot/scripts/lerobot_eval.py",
        f"--policy.path={policy}",
        f"--env.type={env_type}",
        f"--env.task={task}",
        "--eval.batch_size=1",
        "--eval.n_episodes=1",
        f"--policy.device={args.device}",
        f"--output_dir={out}",
    ]

    print(f"Prompt:  {args.prompt}")
    print(f"Env:     {args.env} ({env_type})")
    print(f"Task:    {task}")
    print(f"Policy:  {policy}")
    print(f"Output:  {out}\n")

    r = subprocess.run(cmd)
    if r.returncode == 0:
        print(f"\n✅ Done → python scripts/view_eval.py {out}")
    else:
        print("\n❌ Failed", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
