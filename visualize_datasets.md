# 数据集可视化与使用指南

本指南介绍如何使用 LeRobot 可视化数据集、了解常用数据集列表以及进行数据录制。

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

**Unitree G1 (人形机器人双臂操作)** 🦾🦾：

* **机器人**: Unitree G1 双臂人形机器人（支持 Dex1/Dex3 灵巧手）
* **数据来源**: Unitree Robotics 官方
* **任务类型**: 倒水、积木堆叠、相机安装/包装等

```bash
# 倒水任务 - Dex3 灵巧手 (122k 文件)
python lerobot/src/lerobot/scripts/lerobot_dataset_viz.py \
    --repo-id unitreerobotics/G1_Dex3_Pouring_Dataset \
    --episode-index 0

# 烤面包 - Dex3 灵巧手 (352k 文件)
python lerobot/src/lerobot/scripts/lerobot_dataset_viz.py \
    --repo-id unitreerobotics/G1_Dex3_ToastedBread_Dataset \
    --episode-index 0

# 相机安装 - Dex1 灵巧手 (390k 文件)
python lerobot/src/lerobot/scripts/lerobot_dataset_viz.py \
    --repo-id unitreerobotics/G1_Dex1_MountCamera_Dataset \
    --episode-index 0

# 相机包装 - Dex3 灵巧手 (256k 文件)
python lerobot/src/lerobot/scripts/lerobot_dataset_viz.py \
    --repo-id unitreerobotics/G1_Dex3_CameraPackaging_Dataset \
    --episode-index 0

# 抓取方块 - Dex3 灵巧手 (281k 文件)
python lerobot/src/lerobot/scripts/lerobot_dataset_viz.py \
    --repo-id unitreerobotics/G1_Dex3_GraspSquare_Dataset \
    --episode-index 0
```

> **数据集特点**：640×480 分辨率，30 FPS，记录 7 维状态 + 动作数据（双臂 + 灵巧手）。
>
> ⚠️ **注意**：部分数据集可能是 v2.0 格式，如遇兼容性问题需转换到 v3.0。

**Franka Emika Panda (NYU 操作数据集)** 🦾：

* **总剧集数**: 365 (索引 0-364)
* **机器人**: Franka Panda 7-DOF 协作机械臂
* **数据来源**: 纽约大学

```bash
python lerobot/src/lerobot/scripts/lerobot_dataset_viz.py \
    --repo-id lerobot/nyu_franka_play_dataset \
    --episode-index 0
```

**更多 Franka Panda 数据集**：

```bash
# CMU Franka 探索数据集
python lerobot/src/lerobot/scripts/lerobot_dataset_viz.py \
    --repo-id lerobot/cmu_franka_exploration_dataset \
    --episode-index 0

# NVIDIA PhysicalAI - Panda 堆叠任务
python lerobot/src/lerobot/scripts/lerobot_dataset_viz.py \
    --repo-id nvidia/PhysicalAI-Robotics-Manipulation-SingleArm \
    --episode-index 0
```

---

## 2. 运行预训练策略 (生成评估视频)

详细的评估与推理指南已拆分到独立文档：

👉 **[运行预训练策略指南 (run_pretrained_policy.md)](./run_pretrained_policy.md)**

---

## 3. 常用数据集与模型列表

| 任务类型             | 数据集 ID (repo-id)                       | 预训练模型 ID (policy.path)                   | 说明                                    |
| :------------------- | :---------------------------------------- | :-------------------------------------------- | :-------------------------------------- |
| **PushT**      | `lerobot/pusht`                         | `lerobot/diffusion_pusht`                   | 2D 平面 T 形块推动任务                  |
| **Aloha Sim**  | `lerobot/aloha_sim_transfer_cube_human` | `lerobot/act_aloha_sim_transfer_cube_human` | Aloha 机械臂方块传递（模拟）            |
| **Aloha Real** | `lerobot/aloha_mobile_cabinet`          | (查看 Hub)                                    | Aloha 移动机器人开柜子（真实世界数据）  |
| **Libero**     | `lerobot/libero`                        | `lerobot/pi0_libero_finetuned`              | 终身学习基准测试，5 个品类共 130 个任务 |
| **xArm**       | `lerobot/xarm_lift_medium`              | -                                             | xArm 机械臂拾取任务                     |
| **Unitree H1** | `lerobot/unitreeh1_rearrange_objects`   | -                                             | 人形机器人整理/折叠/搬运                |
| **PR2**        | `lerobot/utokyo_pr2_opening_fridge`     | -                                             | PR2 移动机器人开冰箱                    |

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

## 6. 其他机器人平台与数据集

LeRobot 不仅支持 PushT、Aloha、LIBERO 等模拟环境，还支持多种真实世界机器人平台。以下是三个重要的机器人平台及其可用数据集。

### 🦾 Franka Emika Panda

**机器人简介**：7 自由度协作机械臂，研究界最流行的机器人之一，以力控精准、安全性高著称。

**价格**：约 $25,000（科研级）

**LeRobot 可用数据集**：

| 数据集 ID                                             | Episodes | 说明                         |
| :---------------------------------------------------- | :------- | :--------------------------- |
| `lerobot/nyu_franka_play_dataset`                   | 365      | NYU 创建的 Franka 操作数据集 |
| `lerobot/cmu_franka_exploration_dataset`            | -        | CMU Franka 探索数据集        |
| `IPEC-COMMUNITY/droid_lerobot`                      | 76,000+  | DROID 大规模真实世界操作任务 |
| `nvidia/PhysicalAI-Robotics-Manipulation-SingleArm` | 6 子集   | 堆叠、开柜、开抽屉等任务     |

**快速体验**：

```bash
# 可视化 NYU Franka 数据集
python lerobot/src/lerobot/scripts/lerobot_dataset_viz.py \
    --repo-id lerobot/nyu_franka_play_dataset \
    --episode-index 0
```

**子数据集详情（NVIDIA PhysicalAI）**：

- `panda-stack-wide` - 方块堆叠（宽）
- `panda-stack-platforms` - 平台堆叠
- `panda-stack-platforms-texture` - 纹理平台堆叠
- `panda-open-cabinet-left` - 左侧开柜
- `panda-open-cabinet-right` - 右侧开柜
- `panda-open-drawer` - 开抽屉

---

### 🕷️ WidowX

**机器人简介**：Trossen Robotics 的低成本 6 自由度机械臂，广泛用于 Berkeley RAIL 实验室的 Bridge 数据集，是性价比最高的研究平台。

**价格**：约 $2,000（教学级，极具性价比）

**LeRobot 可用数据集**：

| 数据集 ID                                   | Episodes | 说明                                   |
| :------------------------------------------ | :------- | :------------------------------------- |
| `jesbu1/bridge_v2_lerobot`                | 53,896   | Bridge V2 数据集（需转换到 v3.0） ⚠️ |
| ~~`IPEC-COMMUNITY/bridge_orig_lerobot`~~ | 53,192   | 旧版格式，不兼容                       |

**数据集规模（Bridge V2）**：

- **总 Episodes**：53,896 trajectories
- **环境数**：24 个不同环境
- **机器人**：低成本公开可用机器人
- **数据集大小**：23 GB

**使用前需要转换**：

```bash
# 转换到 v3.0 格式（需要下载 23GB，耗时较长）
python -m lerobot.datasets.v30.convert_dataset_v21_to_v30 \
    --repo-id=jesbu1/bridge_v2_lerobot

# 转换完成后可视化
python lerobot/src/lerobot/scripts/lerobot_dataset_viz.py \
    --repo-id jesbu1/bridge_v2_lerobot \
    --episode-index 0
```

> **💡 快速替代方案**：如果只是想体验真实机器人数据集，可以先使用 **Franka Panda** 或 **xArm**，它们已经是 v3.0 格式，可以直接使用。

**应用场景**：

- ✅ 常用于训练 OpenVLA, RDT 等 VLA 模型
- ✅ 支持 ROS 集成（参考 [Issue #979](https://github.com/huggingface/lerobot/issues/979)）
- ✅ 适合教学和轻量级操作任务

---

### 🏭 KUKA

**机器人简介**：德国 KUKA 工业机器人，以精度高、负载大著称，广泛应用于汽车制造等工业领域。

**价格**：约 $50,000+（工业级）

**LeRobot 可用数据集**：

| 数据集 ID                                    | 说明                        |
| :------------------------------------------- | :-------------------------- |
| `lerobot/stanford_kuka_multimodal_dataset` | Stanford 多模态 KUKA 数据集 |

**特点**：

- 工业级精度和可靠性
- 适合重载和高精度任务
- 支持多模态数据（视觉 + 力觉）

---

### 🤖 Unitree G1

**机器人简介**：Unitree G1 双臂人形机器人，支持 Dex1/Dex3 灵巧手，专为双臂精细操作和全身运动控制设计。

**价格**：约 $16,000（人形机器人中性价比极高）

**LeRobot 可用数据集**：

| 数据集 ID | 文件数 | 说明 |
|:---|:---|:---|
| `unitreerobotics/G1_Dex3_Pouring_Dataset` | 122k | 倒水操作（Dex3） |
| `unitreerobotics/G1_Dex3_ToastedBread_Dataset` | 352k | 烤面包（Dex3） |
| `unitreerobotics/G1_Dex3_CameraPackaging_Dataset` | 256k | 相机包装（Dex3） |
| `unitreerobotics/G1_Dex3_GraspSquare_Dataset` | 281k | 抓取方块（Dex3） |
| `unitreerobotics/G1_Dex3_ObjectPlacement_Dataset` | 98k | 物体放置（Dex3） |
| `unitreerobotics/G1_Dex1_MountCamera_Dataset` | 390k | 相机安装（Dex1） |
| `unitreerobotics/G1_Dex1_MountCameraRedGripper_Dataset` | 173k | 红色夹具相机安装（Dex1） |

**数据集特点**：
- **分辨率**：640×480
- **帧率**：30 FPS
- **记录内容**：7 维状态 + 动作数据（双臂 + 灵巧手）
- **任务类型**：拧瓶盖、倒水、堆叠、包装、存储、双臂抓放

**快速体验**：

```bash
# 可视化倒水数据集（Dex3）
python lerobot/src/lerobot/scripts/lerobot_dataset_viz.py \
    --repo-id unitreerobotics/G1_Dex3_Pouring_Dataset \
    --episode-index 0
```

**应用场景**：
- ✅ 人形机器人全身运动控制（GR00T 策略）
- ✅ 双臂协作操作
- ✅ 灵巧手精细操作（支持 Dex1/Dex3）
- ✅ 适合研究双臂协调和全身平衡

**相关资源**：
- [Unitree IL LeRobot](https://github.com/unitreerobotics/unitree_IL_lerobot) - 官方集成项目
- [G1 设置指南](https://huggingface.co/docs/lerobot/unitree_g1) - LeRobot 文档
- [GR00T 策略](https://huggingface.co/nepyope/GR00T-WholeBodyControl_g1) - 全身控制模型

---

### 📊 机器人平台对比

| 机器人 | 成本 | 自由度 | 应用场景 | LeRobot 数据集 | 适合新手？ |
|:---|:---|:---|:---|:---|:---|
| **xArm** | $$ ($5k-10k) | 6-7 DOF | 通用操作 | 1+ | ⭐⭐⭐⭐ |
| **Aloha** | $$ ($8k) | 双臂 14 DOF | 双手协作 | 20+ | ⭐⭐⭐⭐ |
| **Unitree G1** | $$ ($16k) | 双臂 + 全身 | 人形双臂操作、灵巧手 | 5+ | ⭐⭐⭐ |
| **Franka Panda** | $$$ ($25k) | 7 DOF | 科研、精细操作、力控 | 4+ | ⭐⭐⭐ |
| **KUKA** | $$$$ ($50k+) | 6-7 DOF | 工业、重载、高精度 | 1+ | ⭐⭐ |
| **Unitree H1** | $$$$$ (未公开) | 全身人形 | 复杂操作、移动 | 4+ | ⭐⭐ |
| **WidowX** | $ ($2k) | 6 DOF | 教学、轻量操作 | 2+ (Bridge) | ⭐⭐⭐⭐ |

---

### 🎯 选择建议

**双手协作任务**：
→ **Aloha** (专为双臂设计，数据集完善，$8k)

**人形机器人 + 双臂操作 + 灵巧手**：
→ **Unitree G1** (性价比极高的人形平台，$16k，5+ 数据集，支持 GR00T)

**人形机器人 + 全身移动 + 复杂任务**：
→ **Unitree H1** (完整人形系统，全身控制)

**工业应用 + 高负载**：
→ **KUKA** (工业级可靠性，高精度)

**预算有限 + 初学者**：
→ **WidowX** (Bridge 数据集丰富，社区支持好，仅 $2k)

**科研项目 + 需要力控**：
→ **Franka Panda** (研究标准，文献多，力控精准)

---

## 7. 使用其他数据集训练 VLA 模型

所有上述数据集都可以用于训练 VLA 模型（如 SmolVLA, Pi0）。只需将 `--dataset.repo_id` 指向对应数据集：

```bash
# 使用 Bridge V2 (WidowX) 数据集训练 SmolVLA
lerobot-train \
  --policy.type=smolvla \
  --policy.repo_id=${HF_USER}/smolvla-bridge \
  --dataset.repo_id=jesbu1/bridge_v2_lerobot \
  --output_dir=./outputs/ \
  --steps=100000 \
  --batch_size=4

# 使用 Franka 数据集训练
lerobot-train \
  --policy.type=smolvla \
  --dataset.repo_id=lerobot/nyu_franka_play_dataset \
  --output_dir=./outputs/ \
  --steps=50000
```

---

**Happy Robot Learning! 🤖**

## 参考资源

### VLA 模型与基准测试

- [SmolVLA 官方博客](https://huggingface.co/blog/smolvla)
- [Pi0 和 Pi0-FAST 介绍](https://huggingface.co/blog/pi0)
- [LeRobot v0.4.0 发布说明](https://huggingface.co/blog/lerobot-release-v040)
- [NVIDIA GR00T 集成](https://huggingface.co/blog/nvidia/nvidia-isaac-gr00t-in-lerobot)
- [LeRobot 官方文档](https://huggingface.co/docs/lerobot)

### Franka Panda 数据集

- [NVIDIA PhysicalAI Dataset](https://huggingface.co/datasets/nvidia/PhysicalAI-Robotics-Manipulation-SingleArm)
- [NYU Franka Play Dataset](https://huggingface.co/datasets/lerobot/nyu_franka_play_dataset)
- [DROID LeRobot](https://huggingface.co/datasets/IPEC-COMMUNITY/droid_lerobot)
- [CMU Franka Exploration](https://huggingface.co/datasets/lerobot/cmu_franka_exploration_dataset)

### WidowX Bridge 数据集

- [Bridge V2 LeRobot](https://huggingface.co/datasets/jesbu1/bridge_v2_lerobot) ✅ **推荐**
- [Bridge V2 官方论文](https://arxiv.org/abs/2308.12952)
- [Bridge V2 项目页面](https://rail-berkeley.github.io/bridgedata/)
- [LeRobot WidowX Integration Issue](https://github.com/huggingface/lerobot/issues/979)

### KUKA 数据集

- Stanford KUKA Multimodal Dataset (在 `lerobot/stanford_kuka_multimodal_dataset`)

### Unitree G1 数据集

**Dex3 系列（5 指灵巧手）**：
- [G1_Dex3_Pouring_Dataset](https://huggingface.co/datasets/unitreerobotics/G1_Dex3_Pouring_Dataset) - 倒水操作 ✅
- [G1_Dex3_ToastedBread_Dataset](https://huggingface.co/datasets/unitreerobotics/G1_Dex3_ToastedBread_Dataset) - 烤面包 ✅
- [G1_Dex3_CameraPackaging_Dataset](https://huggingface.co/datasets/unitreerobotics/G1_Dex3_CameraPackaging_Dataset) - 相机包装 ✅
- [G1_Dex3_GraspSquare_Dataset](https://huggingface.co/datasets/unitreerobotics/G1_Dex3_GraspSquare_Dataset) - 抓取方块 ✅
- [G1_Dex3_ObjectPlacement_Dataset](https://huggingface.co/datasets/unitreerobotics/G1_Dex3_ObjectPlacement_Dataset) - 物体放置 ✅

**Dex1 系列（2 指夹具）**：
- [G1_Dex1_MountCamera_Dataset](https://huggingface.co/datasets/unitreerobotics/G1_Dex1_MountCamera_Dataset) - 相机安装 ✅
- [G1_Dex1_MountCameraRedGripper_Dataset](https://huggingface.co/datasets/unitreerobotics/G1_Dex1_MountCameraRedGripper_Dataset) - 红色夹具安装 ✅

**相关资源**：
- [Unitree IL LeRobot](https://github.com/unitreerobotics/unitree_IL_lerobot) - 官方集成项目
- [G1 设置指南](https://huggingface.co/docs/lerobot/unitree_g1) - LeRobot 文档
- [Unitree Robotics 组织](https://huggingface.co/unitreerobotics) - 查看所有数据集

### 通用资源

- [LeRobot Dataset v3.0 文档](https://huggingface.co/blog/lerobot-datasets-v3)
- [LeRobot GitHub](https://github.com/huggingface/lerobot)
- [LeRobot 数据集可视化工具](https://huggingface.co/spaces/lerobot/visualize_dataset)
