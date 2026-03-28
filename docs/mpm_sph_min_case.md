# 在 GeoTaichi 中选择最接近“最小版 SPH 问题”的 MPM 算例

目标：以最少改动复用已有 MPM 算例，快速得到与经典 SPH“自由液柱崩塌/水柱落下”相似的最小流体算例，用于对照或移植。

## 推荐算例

**`example/mpm/ColumnCollapse/NewtonianFluid2D.py`** —— 2D 牛顿流体柱坍塌。

- **相似度理由**
  - **自由液面 & 单相牛顿流体**：与常见 SPH benchmark（2D 水柱崩塌）一致。
  - **简单几何**：矩形水柱在封闭槽内下落，便于对照 SPH 自由面演化。
  - **参数直观**：仅需密度、黏度、体模量（Modulus）和网格尺度，可直接映射到 SPH 中的人造声速/黏度设定。
  - **2D 维度**：粒子数量和成本更低，便于做“最小版”验证。
  - **已有保存路径**：`SavePath: 'large_tank'`，便于快速输出场数据对比。

## 如何最小化修改以贴近 SPH 设定

- **重力/自由面**：脚本已开启重力 `[0, -9.8]`，边界为反射条件，可直接形成自由面演化。
- **时间步长与稳定性**：`Timestep=1e-5` 对于 0.02 m 单元和 \(c_L\approx1\) 较安全；若对标 SPH 的弱可压声速，可调小 `Timestep` 或提高 `Modulus`。
- **粒子分辨率**：`nParticlesPerCell=2`；如需接近 SPH 粒度，可提高到 3–4 以获得更平滑自由面。
- **初始水柱尺寸**：`BoundingBoxSize=[2.24, 1.12]`，可按 SPH benchmark（如 2×1 m）缩放。
- **输出选择**：脚本使用 `select_save_data(grid=True)`；若需粒子字段对照 SPH，可改为同时保存粒子量。

## 若需要三维或更复杂耦合

- **三维流体柱**：`example/mpm/ColumnCollapse/NewtonianFluid.py`（3D），但粒子数和计算成本更高。
- **两相/耦合**：仓库中有 `ULExplicitTwoPhaseEngine`，但现有示例主要为单相；若仅做 SPH 对照，优先从 `NewtonianFluid2D.py` 精简开始。

## 结论

直接复用并微调 `example/mpm/ColumnCollapse/NewtonianFluid2D.py` 是在 GeoTaichi 中搭建“最小版 SPH 问题” MPM 算例的最佳起点。保持 2D、单相、自由液面条件即可快速与经典 SPH 水柱崩塌基准进行对照。 
