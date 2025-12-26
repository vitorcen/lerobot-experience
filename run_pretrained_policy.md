# 运行预训练策略 (生成评估视频)

评估脚本 `lerobot_eval.py` 会在模拟环境中运行策略，并生成 MP4 视频作为结果，**不会**启动 Rerun 实时预览。

## 核心参数说明

以下是常用的评估参数：

- `--policy.path`: 预训练模型的 Hugging Face ID (例如 `lerobot/diffusion_pusht`) 或本地路径
- `--env.type`: 环境类型 (例如 `pusht`, `aloha`, `libero`)
- `--eval.batch_size`: **并行评估的环境数量**。增加此值可加快评估速度，但会占用更多内存/显存。
- `--eval.n_episodes`: 总共评估的回合数。
- `--policy.device`: 运行策略的设备 (`cuda` 或 `cpu`)。
- `--seed`: 设置随机种子 (默认 1000)，确保结果可复现。
- `--eval.use_async_envs`: (可选) 是否使用异步环境运行 (多进程)，默认为 `false`。

## 示例 1: Diffusion Policy on PushT (2D 模拟)

最简单的入门示例，运行 Diffusion Policy 完成推方块任务。

```bash
python lerobot/src/lerobot/scripts/lerobot_eval.py \
    --policy.path=lerobot/diffusion_pusht \
    --env.type=pusht \
    --eval.batch_size=10 \
    --eval.n_episodes=10 \
    --policy.use_amp=false \
    --policy.device=cuda
```

## 示例 2: ACT on Aloha (双臂模拟)

运行 Action Chunking Transformer (ACT) 完成双臂传递方块任务。

```bash
python lerobot/src/lerobot/scripts/lerobot_eval.py \
    --policy.path=lerobot/act_aloha_sim_transfer_cube_human \
    --env.type=aloha \
    --env.task=AlohaTransferCube-v0 \
    --eval.batch_size=1 \
    --eval.n_episodes=10 \
    --policy.device=cuda
```

## 示例 3: Pi0 (VLA) on Libero (3D 模拟)

使用 Pi0 (1.4B) 视觉语言动作模型运行 LIBERO 基准测试。

```bash
python lerobot/src/lerobot/scripts/lerobot_eval.py \
    --policy.path=lerobot/pi0_libero_finetuned \
    --env.type=libero \
    --env.task=libero_10 \
    --eval.batch_size=1 \
    --eval.n_episodes=10 \
    --policy.device=cuda
```

## 查看结果

运行完成后，结果保存在 `outputs/eval/{日期}/{时间}_{任务名}` 目录下：

* **视频文件**：`outputs/eval/.../videos/` 包含每个评估回合的 MP4 录像。
* **指标数据**：`eval_info.json` 包含成功率和奖励统计。

### LIBERO 基准测试品类说明

LIBERO 基准测试包含 **5 个任务品类 (suites)**，共计 **130 个任务**，涵盖从简单物体操作到复杂多步骤场景：

| 品类                               | 标识符             | 任务数 | 最大步数 | 说明                                                   |
| :--------------------------------- | :----------------- | :----- | :------- | :----------------------------------------------------- |
| **LIBERO-Spatial**           | `libero_spatial` | 10     | 280      | 需要空间关系推理的任务（例如：将物体放在另一物体旁边） |
| **LIBERO-Object**            | `libero_object`  | 10     | 280      | 以不同物体操作为中心的任务（例如：抓取特定物体）       |
| **LIBERO-Goal**              | `libero_goal`    | 10     | 300      | 目标条件任务，机器人需要适应不断变化的目标             |
| **LIBERO-90 (短序列任务)**   | `libero_90`      | 90     | 400      | 90 个来自 LIBERO-100 的短时间步任务                    |
| **LIBERO-Long (长序列任务)** | `libero_10`      | 10     | 520      | 10 个来自 LIBERO-100 的长时间步任务                    |

**使用示例**：

```bash
# 评估单个品类
python lerobot/src/lerobot/scripts/lerobot_eval.py \
    --policy.path=lerobot/pi0_libero_finetuned \
    --env.type=libero \
    --env.task=libero_spatial \
    --eval.batch_size=1 \
    --eval.n_episodes=10

# 同时评估多个品类（逗号分隔）
python lerobot/src/lerobot/scripts/lerobot_eval.py \
    --policy.path=lerobot/pi0_libero_finetuned \
    --env.type=libero \
    --env.task=libero_spatial,libero_object,libero_goal,libero_10 \
    --eval.batch_size=1 \
    --eval.n_episodes=10
```

> **品类设计理念**：LIBERO 专注于**终身机器人学习 (Lifelong Robot Learning)**，评估机器人如何将已学知识迁移到新情况。不同品类代表不同的知识迁移挑战维度。

## 更多 VLA (视觉语言动作) 模型

LeRobot 支持多种最新的 VLA 模型。

### 1. Pi0 (π₀) - 通用机器人基础模型

**Pi0** (Physical Intelligence 0) 是由 Physical Intelligence 开发的通用机器人基础模型，LeRobot 提供了对其的完整支持。

> **澄清**：请注意不要将此模型与 NVIDIA 的 [VLA-0](https://github.com/NVlabs/vla0) 混淆。LeRobot 目前暂不支持 NVIDIA VLA-0。

**安装依赖**：

```bash
pip install -e ".[pi]"
# 注意：Pi0 依赖特定的 transformers 版本，如果遇到问题请运行 ./init.sh
```

**运行示例 (Libero)**：

```bash
python lerobot/src/lerobot/scripts/lerobot_eval.py \
    --policy.path=lerobot/pi0_libero_finetuned \
    --env.type=libero \
    --env.task=libero_spatial \
    --eval.batch_size=1 \
    --eval.n_episodes=5 \
    --policy.device=cuda
```

### 2. Pi0.5 (π₀.₅) - 开放世界通用模型 🆕

Pi0.5 是 Pi0 的升级版，专注于跨环境泛化，支持更强的开放世界能力。

**安装依赖**：

```bash
pip install -e ".[pi]"
```

**运行示例**：

```bash
# 运行 Pi0.5 在 Libero 上的微调版本
python lerobot/src/lerobot/scripts/lerobot_eval.py \
    --policy.path=lerobot/pi05_libero_finetuned \
    --env.type=libero \
    --env.task=libero_spatial \
    --eval.batch_size=1 \
    --eval.n_episodes=5 \
    --policy.device=cuda
```

### 3. OpenVLA (通过 X-VLA / SmolVLA 支持)

LeRobot **不直接包含** 名为 `openvla` 的策略类型，而是提供 **SmolVLA** 和 **X-VLA** 作为更高效的替代方案。X-VLA 使用软提示（Soft Prompts）来适应不同的机器人形态，被视为下一代适应性更强的 VLA 架构。

**X-VLA 运行示例**：

```bash
# 安装依赖
pip install -e ".[xvla]"

# 运行 X-VLA 在 Libero 上的微调版本
python lerobot/src/lerobot/scripts/lerobot_eval.py \
    --policy.path=lerobot/xvla-libero \
    --env.type=libero \
    --env.task=libero_spatial,libero_goal,libero_10 \
    --eval.batch_size=1 \
    --eval.n_episodes=1 \
    --env.episode_length=800
```

### 4. NVIDIA GR00T N1.5 - 人形机器人专用 ⚠️

GR00T 是 NVIDIA 的通用人形机器人基础模型。

**安装依赖**：

```bash
pip install flash-attn --no-build-isolation
pip install -e "./lerobot[groot]"
```

**运行方式**：
通常建议使用专门的 `groot` 脚本或确保环境配置正确后运行。

```bash
python lerobot/src/lerobot/scripts/lerobot_eval.py \
    --policy.path=aractingi/bimanual-handover-groot-10k \
    --env.type=libero \
    --env.task=libero_spatial \
    --eval.batch_size=1 \
    --eval.n_episodes=5 \
    --policy.device=cuda
```

> **注意**：目前 Hugging Face 上**没有**公开的预训练 GR00T Libero 权重，上述代码仅作为运行指令模板。
>
> **提示**：开发人员可尝试使用 `aractingi/bimanual-handover-groot-10k` 模型进行代码通路测试（需配合参数 `--policy.embodiment_tag=gr1`），但请注意该模型并非针对 Libero 任务训练，因此评估分数没有参考意义。

### 5. SmolVLA (450M 参数) - 轻量级高效 ⚡

适合消费级 GPU 的轻量级模型。

**安装依赖**：

```bash
pip install -e ".[smolvla]"
```

**运行示例**：

```bash
python lerobot/src/lerobot/scripts/lerobot_eval.py \
    --policy.path=HuggingFaceVLA/smolvla_libero \
    --env.type=libero \
    --env.task=libero_10 \
    --eval.batch_size=2 \
    --eval.n_episodes=5 \
    --policy.device=cuda
```

## VLA 模型对比总结

| 模型                 | 参数量 | 显存需求 | 特点         | 适用场景                    |
| :------------------- | :----- | :------- | :----------- | :-------------------------- |
| **SmolVLA**    | 450M   | 4-8GB    | 轻量、快速   | 消费级显卡、边缘计算        |
| **Pi0** (π₀) | 1.4B   | 24GB+    | 基础通用模型 | 通用机器人控制              |
| **Pi0.5**      | ~1.4B  | 24GB+    | 开放世界泛化 | 跨环境、未见场景            |
| **X-VLA**      | 0.9B+  | 16GB+    | 跨形态适应   | 多种机器人形态适配 (软提示) |
| **GR00T**      | 3B     | 40GB+    | 人形机器人   | NVIDIA 生态、人形操作       |

**无头服务器渲染配置（重要）**

如果在无头服务器（SSH 远程）运行 LIBERO/robosuite 环境，需要设置环境变量：

```bash
# GPU 加速渲染（推荐）
export MUJOCO_GL=egl
export PYOPENGL_PLATFORM=egl
export EGL_DEVICE_ID=0  # 如果有多个 GPU，指定 GPU ID

# 或者使用 CPU 软件渲染（更稳定但慢）
export MUJOCO_GL=osmesa
```
