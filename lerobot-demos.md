# LeRobot 演示与推理指南

本指南介绍如何使用 LeRobot 可视化数据集、运行预训练策略以及查看结果。

---

## 1. 可视化数据集 (使用 Rerun)

LeRobot 使用 [Rerun](https://rerun.io/) 来可视化数据集，提供了丰富的交互式时间轴视图。

### 启动可视化

以 PushT 数据集为例 (**共 206 个剧集**，索引 0-205)：

```bash
conda activate lerobot

python lerobot/src/lerobot/scripts/lerobot_dataset_viz.py \
    --repo-id lerobot/pusht \
    --episode-index 0
```

* **交互方式**：脚本启动后会自动在浏览器中打开 Rerun Viewer（默认地址 `http://127.0.0.1:9090`）。你可以拖动时间轴查看机器人状态、动作和相机画面的变化。
* **探索数据**：尝试修改 `--episode-index` (例如 10, 50, 100) 来查看不同的演示。

### 远程服务器可视化

如果你在远程服务器（如 SSH）上运行，可以使用 `--save` 参数保存为 `.rrd` 文件，然后下载到本地查看：

```bash
# 1. 在服务器上生成 .rrd 文件
python lerobot/src/lerobot/scripts/lerobot_dataset_viz.py \
    --repo-id lerobot/pusht \
    --episode-index 0 \
    --save 1 \
    --output-dir ./viz_outputs

# 2. 将生成的 .rrd 文件下载到本地 (使用 scp 或 SFTP)

# 3. 在本地安装 rerun 并打开
pip install rerun-sdk
rerun lerobot_pusht_episode_0.rrd
```

### 更多数据集示例

**Libero (模拟操作任务)**：

* **总剧集数**: 1693 (索引 0-1692)
* **提示**: 尝试修改 `--episode-index` 查看不同的任务演示。

```bash
python lerobot/src/lerobot/scripts/lerobot_dataset_viz.py \
    --repo-id lerobot/libero \
    --episode-index 0
```

**Aloha Real (真实世界开柜子)**：

* **总剧集数**: 85 (索引 0-84)

```bash
python lerobot/src/lerobot/scripts/lerobot_dataset_viz.py \
    --repo-id lerobot/aloha_mobile_cabinet \
    --episode-index 0
```

**xArm (机械臂拾取)**：

* **总剧集数**: 800 (索引 0-799)

```bash
python lerobot/src/lerobot/scripts/lerobot_dataset_viz.py \
    --repo-id lerobot/xarm_lift_medium \
    --episode-index 0
```

**Unitree H1 (人形机器人整理)**：

* **总剧集数**: 30 (索引 0-29)

```bash
python lerobot/src/lerobot/scripts/lerobot_dataset_viz.py \
    --repo-id lerobot/unitreeh1_rearrange_objects \
    --episode-index 0
```

### 其他机器人与任务

**PR2 (开冰箱 - 东京大学)**：

* **总剧集数**: 80 (索引 0-79)

```bash
python lerobot/src/lerobot/scripts/lerobot_dataset_viz.py \
    --repo-id lerobot/utokyo_pr2_opening_fridge \
    --episode-index 0
```

**Unitree H1 (折叠衣物)**：

* **总剧集数**: 38 (索引 0-37)

```bash
python lerobot/src/lerobot/scripts/lerobot_dataset_viz.py \
    --repo-id lerobot/unitreeh1_fold_clothes \
    --episode-index 0
```

---

## 2. 运行预训练策略 (生成评估视频)

评估脚本 `lerobot_eval.py` 会在模拟环境中运行策略，并生成 MP4 视频作为结果，**不会**启动 Rerun 实时预览。

### 运行 Diffusion Policy 控制 PushT

```bash
python lerobot/src/lerobot/scripts/lerobot_eval.py \
    --policy.path=lerobot/diffusion_pusht \
    --env.type=pusht \
    --eval.batch_size=10 \
    --eval.n_episodes=10 \
    --policy.use_amp=false \
    --policy.device=cuda
```

### 查看结果

运行完成后，结果保存在 `outputs/eval/{日期}/{时间}_{任务名}` 目录下：

* **视频文件**：`outputs/eval/.../videos/` 包含每个评估回合的 MP4 录像。
* **指标数据**：`eval_info.json` 包含成功率和奖励统计。

### 运行 ACT 控制 Aloha (模拟环境)

```bash
python lerobot/src/lerobot/scripts/lerobot_eval.py \
    --policy.path=lerobot/act_aloha_sim_transfer_cube_human \
    --env.type=aloha \
    --env.task=AlohaTransferCube-v0 \
    --eval.batch_size=1 \
    --eval.n_episodes=10 \
    --policy.device=cuda
```

> **注意**：首次运行会自动下载模型权重。如果是旧版模型（无 processor 配置），脚本会自动尝试从权重中提取统计信息以兼容运行。

### 运行 Pi0 (VLA) 控制 Libero (模拟环境)

使用 Pi0 (Physical Intelligence) 视觉语言动作模型在 Libero 基准测试上运行。

```bash
python lerobot/src/lerobot/scripts/lerobot_eval.py \
    --policy.path=lerobot/pi0_libero_finetuned \
    --env.type=libero \
    --env.task=libero_10 \
    --eval.batch_size=1 \
    --eval.n_episodes=10 \
    --policy.device=cuda
```

> **注意**：Pi0 是大型模型（1.4B 参数），需要较大的显存（建议 24GB+）。如果显存不足，请尝试减小 batch size 或使用更小的 VLA 模型。

#### LIBERO 基准测试品类说明

LIBERO 基准测试包含 **5 个任务品类 (suites)**，共计 **130 个任务**，涵盖从简单物体操作到复杂多步骤场景：

| 品类                                     | 标识符             | 任务数 | 最大步数 | 说明                                                   |
| :--------------------------------------- | :----------------- | :----- | :------- | :----------------------------------------------------- |
| **LIBERO-Spatial**                 | `libero_spatial` | 10     | 280      | 需要空间关系推理的任务（例如：将物体放在另一物体旁边） |
| **LIBERO-Object**                  | `libero_object`  | 10     | 280      | 以不同物体操作为中心的任务（例如：抓取特定物体）       |
| **LIBERO-Goal**                    | `libero_goal`    | 10     | 300      | 目标条件任务，机器人需要适应不断变化的目标             |
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

### 更多 VLA (视觉语言动作) 模型

LeRobot 支持多种 VLA 模型，从轻量级到大型都有选择：

**SmolVLA (450M 参数) - 轻量级高效 ⚡**

```bash
# 在 LIBERO 基准测试上运行（推荐：显存需求低，约 4-8GB）
export MUJOCO_GL=egl
export PYOPENGL_PLATFORM=egl

python lerobot/src/lerobot/scripts/lerobot_eval.py \
    --policy.path=HuggingFaceVLA/smolvla_libero \
    --env.type=libero \
    --env.task=libero_10 \
    --eval.batch_size=2 \
    --eval.n_episodes=5 \
    --policy.device=cuda
```

> **SmolVLA 优势**：
>
> - ✅ 仅 450M 参数，可在消费级 GPU 运行
> - ✅ 在 LIBERO 和 Meta-World 上表现优异（平均成功率 78.3%）
> - ✅ 支持异步推理，速度提升 30%
> - ✅ 仅用 30k 训练样本，效率极高

**Pi0 - 强大的通用 VLA 模型**

```bash
# Pi0 Libero 微调版（推荐）
python lerobot/src/lerobot/scripts/lerobot_eval.py \
    --policy.path=lerobot/pi0_libero_finetuned \
    --env.type=libero \
    --env.task=libero_10 \
    --eval.batch_size=1 \
    --eval.n_episodes=5 \
    --policy.device=cuda
```

> **注意**：`lerobot/pi05_base` 是基础模型，尚未针对 Libero 观测空间进行微调，直接运行可能会报错（Feature mismatch）。建议使用上面的 `pi0_libero_finetuned`。

**NVIDIA GR00T N1.5 (3B 参数) - 人形机器人专用 ⚠️**

> **重要提示**：GR00T N1.5 需要特殊的集成方式，**不能直接用 `lerobot_eval.py` 运行**。
>
> 如需使用 GR00T，请参考：
>
> - [GR00T 官方文档](https://huggingface.co/docs/lerobot/en/groot)
> - [GR00T LIBERO 微调模型](https://huggingface.co/Tacoin/GR00T-N1.5-3B-LIBERO-LONG)
>
> GR00T 使用专门的 `Gr00tPolicy` API 或推理服务器模式，主要为真实机器人（SO-100/SO-101）设计。

**推荐使用模型优先级**：

1. **SmolVLA** - 最轻量，易于上手，消费级 GPU 友好 ✅
2. **Pi0** - 强大的通用 VLA 模型（需要特殊的 transformers 版本） ✅
3. **Pi0.5** - Pi0 的改进版（需要特殊的 transformers 版本） ✅

> **⚠️ 注意：Pi0/Pi0.5 特殊要求**
>
> Pi0 和 Pi0.5 依赖于一个特定的 `transformers` 分支。`init.sh` 默认会自动安装此版本。
> 如果你遇到 `ValueError: An incorrect transformer version is used` 错误，请重新运行 `./init.sh`。

**VLA 模型对比表**

| 模型                 | 参数量 | 显存需求 | 适用场景                     | 特点                       |
| :------------------- | :----- | :------- | :--------------------------- | :------------------------- |
| **SmolVLA**    | 450M   | 4-8GB    | LIBERO, Meta-World, 轻量应用 | 高效、快速、适合消费级 GPU |
| **Pi0**        | 1.4B   | 24GB+    | 通用机器人控制               | 强大的视觉语言理解         |
| **Pi0.5**      | ~1.4B  | 24GB+    | 多任务微调                   | Pi0 改进版                 |
| **GR00T N1.5** | 3B     | 40GB+    | 人形机器人、复杂操作         | NVIDIA 顶级基础模型        |

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

---

## 3. 常用数据集与模型列表

| 任务类型             | 数据集 ID (repo-id)                       | 预训练模型 ID (policy.path)                   | 说明                                   |
| :------------------- | :---------------------------------------- | :-------------------------------------------- | :------------------------------------- |
| **PushT**      | `lerobot/pusht`                         | `lerobot/diffusion_pusht`                   | 2D 平面 T 形块推动任务                 |
| **Aloha Sim**  | `lerobot/aloha_sim_transfer_cube_human` | `lerobot/act_aloha_sim_transfer_cube_human` | Aloha 机械臂方块传递（模拟）           |
| **Aloha Real** | `lerobot/aloha_mobile_cabinet`          | (查看 Hub)                                    | Aloha 移动机器人开柜子（真实世界数据） |
| **Libero**     | `lerobot/libero`                        | `lerobot/pi0_libero_finetuned`              | 终身学习基准测试，5 个品类共 130 个任务 |
| **xArm**       | `lerobot/xarm_lift_medium`              | -                                             | xArm 机械臂拾取任务                    |
| **Unitree H1** | `lerobot/unitreeh1_rearrange_objects`   | -                                             | 人形机器人整理/折叠/搬运               |
| **PR2**        | `lerobot/utokyo_pr2_opening_fridge`     | -                                             | PR2 移动机器人开冰箱                   |

---

## 4. 实时遥操作与录制 (Rerun)

如果你有真实的机器人硬件或想要进行遥操作，LeRobot 支持通过 Rerun 进行实时可视化。

* **遥操作**：`lerobot_teleoperate.py`
* **数据录制**：`lerobot_record.py`

这些脚本在运行时会启动 Rerun 服务器，允许你实时监控相机画面和机器人状态。

---

## 5. 常见问题 (FAQ)

### Q: 如何实时查看模拟环境运行（而不是看回放视频）？

**A**: `lerobot_eval.py` 设计为批量评估并生成视频报告，默认不显示实时窗口。这是为了支持并行环境和在无头服务器上运行。请查看 `outputs/eval/.../videos` 目录下的 MP4 文件来分析策略表现。

### Q: 显存不足 (OOM) 怎么办？

**A**:

1. 减小 `eval.batch_size`（例如设为 1）。
2. 对于 Pi0 等大模型，确保使用高端 GPU (A100/H100) 或量化版本（如果可用）。
3. 使用 `--policy.device=cpu`（仅作为调试，速度极慢）。

### Q: 找不到 `policy_preprocessor.json` 错误？

**A**: 这是因为加载了旧版本的预训练模型。我们已经对脚本进行了修补，它应该会自动从模型权重中提取统计信息并继续运行。如果仍然报错，请检查网络连接是否正常，以便从 Hugging Face Hub 下载配置文件。

### Q: EGL 渲染错误（EGL_NOT_INITIALIZED）？

**A**: 这是在无头服务器上运行 LIBERO/robosuite 时的常见问题。解决方案：

```bash
# 运行前设置环境变量
export MUJOCO_GL=egl
export PYOPENGL_PLATFORM=egl
export EGL_DEVICE_ID=0

# 然后运行评估命令
python lerobot/src/lerobot/scripts/lerobot_eval.py ...
```

如果 EGL 仍然出错，尝试使用 OSMesa（CPU 软件渲染）：

```bash
export MUJOCO_GL=osmesa
```

**注意**：析构函数中的 "Exception ignored" 警告通常可以忽略，不影响运行结果。

---

**Happy Robot Learning! 🤖**

## 参考资源

- [SmolVLA 官方博客](https://huggingface.co/blog/smolvla)
- [Pi0 和 Pi0-FAST 介绍](https://huggingface.co/blog/pi0)
- [LeRobot v0.4.0 发布说明](https://huggingface.co/blog/lerobot-release-v040)
- [NVIDIA GR00T 集成](https://huggingface.co/blog/nvidia/nvidia-isaac-gr00t-in-lerobot)
- [LeRobot 官方文档](https://huggingface.co/docs/lerobot)
