#!/usr/bin/env python3
"""Quick SmolVLA prompt test — run a single episode and save video."""
import argparse
import subprocess
import sys
import time
from pathlib import Path

# SmolVLA 预训练模型 + 对应环境
MODELS = {
    "libero":     {"policy": "lerobot/smolvla_libero",     "env": "libero",     "task": "libero_spatial"},
    "metaworld":  {"policy": "lerobot/smolvla_metaworld",  "env": "metaworld",  "task": "assembly-v3"},
    "robocasa":   {"policy": "lerobot/smolvla_robocasa",   "env": "robocasa",   "task": "default",   "manual_install": "see docs/source/robocasa.mdx"},
    "robotwin":   {"policy": "lerobot/smolvla_robotwin",   "env": "robotwin",   "task": "place_empty_cup", "manual_install": "see docs/source/robotwin.mdx"},
}

# 需要手动安装的环境
MANUAL_INSTALL_ENVS = {"robocasa", "robotwin"}


def main():
    p = argparse.ArgumentParser(description="SmolVLA interactive prompt test")
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

    # 检查是否需要手动安装（如果已安装则直接放行）
    if args.env in MANUAL_INSTALL_ENVS:
        pkg_map = {"robocasa": "robocasa", "robotwin": "robotwin"}
        pkg = pkg_map.get(args.env)
        try:
            __import__(pkg)
        except ImportError:
            install_guide = preset.get("manual_install", "")
            print(f"⚠️  {args.env.upper()} 需要手动安装，不是 pip extra", flush=True)
            print(f"   安装指南: {install_guide}", flush=True)
            print(f"   跳过此环境，使用 --env libero 或 --env metaworld 测试\n", flush=True)
            sys.exit(1)

    ts = time.strftime("%Y%m%d_%H%M%S")
    out = Path(f"outputs/eval/smolvla_{args.env}_{ts}")

    cmd = [
        sys.executable, "-u", "lerobot/src/lerobot/scripts/lerobot_eval.py",
        f"--policy.path={policy}",
        f"--env.type={env_type}",
        f"--env.task={task}",
        "--eval.batch_size=1",
        "--eval.n_episodes=1",
        f"--policy.device={args.device}",
        f"--output_dir={out}",
    ]

    # SmolVLA metaworld model expects 3 cameras, but env only outputs one.
    # Map the single camera to camera1 and let the model zero-pad camera2/3.
    if args.env == "metaworld":
        cmd.append('--rename_map={"observation.image": "observation.images.camera1"}')
        cmd.append("--policy.empty_cameras=2")

    # RoboCasa native camera keys -> SmolVLA camera1/2/3 layout.
    if args.env == "robocasa":
        cmd.append(
            '--rename_map={"observation.images.robot0_agentview_left": "observation.images.camera1", '
            '"observation.images.robot0_eye_in_hand": "observation.images.camera2", '
            '"observation.images.robot0_agentview_right": "observation.images.camera3"}'
        )
        # Async envs cause extremely slow init in RoboCasa; disable them.
        cmd.append("--eval.use_async_envs=false")

    print(f"Prompt:  {args.prompt}", flush=True)
    print(f"Env:     {args.env} ({env_type})", flush=True)
    print(f"Task:    {task}", flush=True)
    print(f"Policy:  {policy}", flush=True)
    print(f"Output:  {out}\n", flush=True)

    r = subprocess.run(cmd)
    if r.returncode == 0:
        print(f"\n✅ Done → python scripts/view_eval.py {out}", flush=True)
    else:
        print("\n❌ Failed", file=sys.stderr, flush=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
