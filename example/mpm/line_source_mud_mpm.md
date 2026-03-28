# GeoTaichi MPM 复现二维线源瞬时抛泥问题改造指南

本说明基于 `example/mpm/ColumnCollapse/NewtonianFluid2D.py`，结合仓库中的 MPM 结构速查文档与 SPH 公式整理（`抛泥问题SPH法解析.md`），梳理如何在 GeoTaichi 的 MPM 框架下复现“二维线源瞬时抛泥”算例。重点给出需要修改或新增的脚本段落、参数设置以及对应代码位置，方便在现有能力范围内快速搭建和后续拓展。本文所有公式均使用纯文本写法（如 `alpha_s = 1 - phi`、`dt_c = 0.3*h/c0`）。

## 1. 相关模块快速定位
- 配置与总体流程：`src/mpm/mainMPM.py`（`set_configuration`、`set_solver`、`run`），执行循环在 `src/mpm/MPMBase.py::Solver`。
- 两相粒子与引擎：`ParticleCloudTwoPhase2D`（`src/mpm/structs/Particle.py`，包含 `ms/mf/vs/vf/porosity/permeability`）与 `ULExplicitTwoPhaseEngine`（`src/mpm/engines/ULExplicitTwoPhaseEngine.py`，绑定 P2G/G2P、双相应力更新）。
- 两相粒子生成：`src/mpm/generator/BodyGenerator.py` 中的 `kernel_add_body_twophase2D` 路径；需要 `material_type="TwoPhaseSingleLayer"` 才会走该分支。
- 输出：`src/mpm/Recorder.py::MonitorParticleTwoPhase` 会存储总/固/液速度、质量、孔隙度、压力等，便于后处理云团浓度和下沉速度。

## 2. 方案概述
抛泥算例可视为水–泥沙双流体瞬时释放。GeoTaichi 已内置单层两相 MPM 数据结构与显式 UL 引擎，可直接用于“水体+泥沙团”耦合计算。思路：
- 选用 `material_type="TwoPhaseSingleLayer"` 激活两相引擎与粒子字段。
- 通过 **两个材料号** 区分背景水体与初始泥沙团，分别设置孔隙度/固相密度/流体体积弹性模量/渗透率，使 `ms/mf` 反映初始体积分数 \(\alpha_s, \alpha_f\)。
- 采用 MUSL/USL 显式格式与 Affine/Taylor PIC 投影控制数值耗散，时间步长取 SPH 文档中的 CFL/黏性约束最小值。
- 边界使用反射约束（线段），域宽高按文献 \(L=H=1\) 设定；输出粒子数据用于后处理泥沙云团宽度/下沉距离。

## 3. 基于 `NewtonianFluid2D.py` 的最小改动示例
以下片段展示核心改动（仅示意关键字段，保持原脚本结构与 API）：

```python
from geotaichi import *

init(dim=2, device_memory_GB=3.7)
mpm = MPM()

# 1) 配置：启用两相、UL 显式、Affine PIC，域 1 m × 1 m
mpm.set_configuration(domain=[1., 1.],
                      background_damping=0.0,
                      alphaPIC=1.0,
                      mapping="USL",                # 或 MUSL
                      shape_function="QuadBSpline",
                      gravity=[0., -9.8],
                      material_type="TwoPhaseSingleLayer",
                      velocity_projection="Affine")

# 2) 求解器：时间步长取 min(dt_c, dt_F, dt_nu)，下方示例用 SPH 声速 CFL
h = 0.005
c0 = 10 * (9.8 ** 0.5)                     # c0 = 10*sqrt(g)
dt_c = 0.3 * h / c0
mpm.set_solver({"Timestep":       dt_c,
                "SimulationTime": 4.0,
                "SaveInterval":   0.05,
                "SavePath":       "line_source_mud"})

# 3) 预分配：粒子数覆盖水体 + 泥沙团 + 边界粒子
mpm.memory_allocate(memory={
    "max_material_number": 2,
    "max_particle_number": 120000,
    "verlet_distance_multiplier": 1.,
    "max_constraint_number": {"max_reflection_constraint": 20000}
})

# 4) 材料：区分水体与泥沙团（示例数值可按表 5.1 微调）
fluid_bulk = (c0 ** 2) * 1000.            # rho_f * c0^2
mpm.add_material(model="LinearElastic", material={  # 背景水体近似无固相
    "MaterialID":       1,
    "Young":            1e3,        # 极软，避免剪切刚度影响
    "Poisson":          0.495,
    "SolidDensity":     10.0,       # 近似 0，保留正值避免除零
    "FluidDensity":     1000.,
    "Porosity":         0.999,
    "FluidBulkModulus": fluid_bulk,  # rho_f * c0^2
    "Permeability":     1e-6
})
mpm.add_material(model="LinearElastic", material={  # 泥沙团，按 αs0=0.606
    "MaterialID":       2,
    "Young":            5e4,       # 可调以控制屈服/扩散
    "Poisson":          0.3,
    "SolidDensity":     2650.,
    "FluidDensity":     1000.,
    "Porosity":         0.394,     # 1 - alpha_s0
    "FluidBulkModulus": fluid_bulk,
    "Permeability":     1e-7      # 控制拖曳强度
})

# 5) 网格与区域
mpm.add_element({"ElementType": "Q4N2D", "ElementSize": [0.005, 0.005]})
mpm.add_region([  # 背景水体
    {"Name": "tank", "Type": "Rectangle2D", "BoundingBoxPoint": [0., 0.],
     "BoundingBoxSize": [1., 1.], "ydirection": [0., 1.]},
    # 泥沙初始团（面积 q0，可切换 0.05/0.10 m^2）
    {"Name": "mud", "Type": "Rectangle2D", "BoundingBoxPoint": [0.45, 0.7],
     "BoundingBoxSize": [0.2236, 0.2236], "ydirection": [0., 1.]}
])

# 6) 粒子：水体与泥沙分体生成，初速为零
mpm.add_body({"Template": [
    {"RegionName": "tank", "nParticlesPerCell": 2, "BodyID": 0, "MaterialID": 1,
     "InitialVelocity": [0., 0.], "FixVelocity": ["Free", "Free"]},
    {"RegionName": "mud", "nParticlesPerCell": 2, "BodyID": 1, "MaterialID": 2,
     "InitialVelocity": [0., 0.], "FixVelocity": ["Free", "Free"]}
]})

# 7) 边界：四周反射（与原算例一致）
mpm.add_boundary_condition(boundary=[
    {"BoundaryType": "ReflectionConstraint", "Norm": [-1., 0.], "StartPoint": [0., 0.], "EndPoint": [0., 1.]},
    {"BoundaryType": "ReflectionConstraint", "Norm": [1., 0.],  "StartPoint": [1., 0.], "EndPoint": [1., 1.]},
    {"BoundaryType": "ReflectionConstraint", "Norm": [0., -1.], "StartPoint": [0., 0.], "EndPoint": [1., 0.]},
    {"BoundaryType": "ReflectionConstraint", "Norm": [0., 1.],  "StartPoint": [0., 1.], "EndPoint": [1., 1.]}
])

mpm.select_save_data(grid=True)  # 粒子默认已保存，开启网格便于诊断
mpm.run()
mpm.postprocessing()
```

要点说明：
- 以 `Porosity` 控制固相体积分数（alpha_s = 1 - phi）；背景水体令 `phi≈1`，泥沙团用 `phi=0.394` 对应 alpha_s0=0.606。
- `Permeability` 与 `porosity` 共同决定 `ParticleCloudTwoPhase2D._compute_drag_force`，可近似 SPH 里的阻力系数 gamma。减小渗透率或提高固相密度可增强拖曳/沉降。
- 将 `FluidBulkModulus` 设为 `rho_f * c0^2` 模拟 SPH 的 Tait EOS 弱可压假设；`Young/Poisson` 取软值，使固相应力主要由孔压驱动。
- 若需更低数值耗散，可把 `mapping="MUSL"`、`velocity_projection="Taylor PIC"`。

## 4. 时间步长与监控
- 参考 SPH 约束：`dt_c = 0.3*h/c0`，`dt_F = 0.3*sqrt(h/max|a|)`，`dt_nu = 0.125*h^2/max(nu)`，取三者最小。在 MPM 中可：
  - 直接将 `Timestep` 设为上述最小值；或开启 `AdaptiveTimestep=True`，并在循环外自适应更新 `sims.dt`（需要少量自定义 hook）。
  - `Simulation.check_critical_timestep()` 仅检查 MPM 的 CFL，可在 `mpm.run()` 前手动覆写 `sims.dt[None] = min(...)` 以纳入黏性/加速度约束。
- 输出粒子文件里已有 `porosity` 与 `solid_mass/fluid_mass`，浓度可后处理为 `alpha_s = 1 - phi`，下沉速度用 `solid_velocity` 或总速 `velocity` 计算。

## 5. 可选代码增强（按需）
若需更贴近 SPH 文档中的公式，可考虑：
1) **允许两相使用流体型本构**：在 `MaterialManager.material_handle` 中为 `TwoPhaseSingleLayer` 加入 `Newtonian/Bingham` 路径，或实现一个轻量 `UserDefined` 流变，令剪切应力直接由黏度控制而非固相弹性模量。
2) **拖曳/扩散系数外显化**：在 `ParticleCloudTwoPhase2D._compute_drag_force` 中暴露经验系数（对应文档中的 gamma、epsilon_s），并通过 `Material` 参数传递，便于与表 5.1 粒径/沉速匹配。
3) **自适应时间步**：在 `MPMBase.Solver` 主循环内加入基于最大速度/加速度/剪切速率的在线 `dt` 更新，与 SPH 的 `dt_F`、`dt_nu` 对齐。
4) **后处理接口**：添加脚本读取 `npz` 输出，计算云团宽度 B、下沉距离 Z、无量纲速度 `w_c/omega_s`（阈值 `alpha_s = 0.1 * alpha_s_max`），复用 `MonitorParticleTwoPhase` 结果即可。

按照上述设置即可在不改动核心 kernel 的前提下，用 MPM 版本的两相显式求解复现二维线源瞬时抛泥过程；若需更高保真度，可逐步采用“可选代码增强”部分的改进。
