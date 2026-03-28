# GeoTaichi MPM 模块结构速查

本文梳理 GeoTaichi 中 MPM（Material Point Method）模块的主要入口与配置位置，说明材料、几何/粒子、边界与荷载的设置方式，以及时间步长、输出与核心 kernel 的调用链。

## 1. 入口与整体流程

- **MPM 对象入口**：`src/mpm/mainMPM.py` 中的 `MPM` 类负责全部高层接口，其中常用方法位置如下：
  - `set_configuration`：39-75 行
  - `set_solver`：100-109 行
  - `memory_allocate`：111-120 行
  - `add_material`：154-156 行，`add_element`：157-160 行
  - `add_region`：161-167 行，`add_body`：168-170 行
  - `add_boundary_condition`：191-199 行，`select_save_data`：213-217 行
  - `run`：300-309 行
- **运行入口**：`MPM.run()` 会调用 `add_essentials()`（创建引擎、记录器、邻域搜索等），随后 `check_critical_timestep()` 校验显式稳定步长，最终调用 `self.solver.Solver(self.scene, self.neighbor)` 或 `Visualize()`（`mainMPM.py` 300-309 行）。
- **求解循环**：`Solver.Solver()` 在 `src/mpm/MPMBase.py` 52-83 行，先做 `pre_calculation`、首帧保存，再执行主循环：`core()` → `generator.regenerate()` → 按 `save_interval` 调用 `save_file()`，并用 `sims.delta` 累加时间与步数。
- **核心一次步**：`Solver.core()`（`MPMBase.py` 159-164 行）依次调用 `engine.reset_grid_messages`、`engine.build_neighbor_list`、`engine.compute`，再执行用户注册的 `postprocess` kernel。

## 2. 材料配置位置

- **接口**：`MPM.add_material()` 将材料字典传入 `scene.activate_material`（`mainMPM.py` 154-156 行）。
- **管理类**：`src/mpm/MaterialManager.py` 的 `MaterialHandle.setup()` 读取全部材料参数并实例化相应本构（`material_handle` 方法，覆盖线弹性、MohrCoulomb、Drucker-Prager、NeoHookean 等，24-120 行）。
- **本构实现**：位于 `src/physics_model/constitutive_model/`（`infinitesimal_strain/`、`finite_strain/`、`strain_rate/`）。
- **示例**：`example/mpm/ElementTest/CompressionMC.py` 30-40 行展示通过 `mpm.add_material(model="MohrCoulomb", material={...})` 配置材料属性。

## 3. 几何、粒子与单元配置

- **区域定义**：`MPM.add_region()` 将区域字典传给 `GenerateManager.add_my_region`（`mainMPM.py` 161-167 行），由 `RegionFunction` 管理几何体。
- **粒子生成**：`MPM.add_body()` 触发 `BodyGenerator.generate_material_points`（`src/mpm/generator/BodyGenerator.py` 150-199 行）根据区域、单元尺寸、`nParticlesPerCell` 等生成粒子，写入 `scene.particle`。
- **粒子数据结构**：`src/mpm/structs/Particle.py` 定义 `ParticleCloud` / `ParticleCloud2D` 等，存储质量、体积、位置、速度、应力、速度梯度、约束标志等字段。
- **单元/网格**：`src/mpm/elements/` 下的 `HexahedronElement8Nodes.py`（3D R8N3D）、`QuadrilateralElement4Nodes.py`（2D Q4）等定义背景网格尺寸、体积与插值节点数量；通过 `MPM.add_element()` 激活（`mainMPM.py` 157-160 行）。
- **示例**：`example/mpm/ElementTest/CompressionMC.py` 42-70 行展示区域与粒子模板配置（矩形区域、每单元 2 颗粒、初始应力与速度等）。

## 4. 边界条件与荷载配置

- **接口**：`MPM.add_boundary_condition()` 支持传入字典/列表或文件路径；内部调用 `scene.boundary.iterate_boundary_constraint` 或读取文本（`mainMPM.py` 191-199 行）。
- **约束类型与存储**：`src/mpm/boundaries/BoundaryConstraint.py` 定义 `BoundaryConstraints`，在 `activate_boundary_constraints()` 中按 `Simulation` 中的最大数量分配 `velocity_boundary`、`traction_boundary`、`friction_boundary`、`reflection_boundary`、`absorbing_boundary` 及粒子荷载 `particle_traction`（53-109 行）。
- **设置接口**：同文件中提供 `set_velocity_constraints*`、`set_traction_constraints`、`set_particle_traction` 等方法，支持区域/节点选择与自由度控制。
- **底层 kernel**：`src/mpm/boundaries/BoundaryCore.py` 提供 `kernel_initialize_boundary`、`set_reflection_constraint`、`set_friction_constraint` 以及网格/粒子荷载设置相关的 Taichi kernel（如 `set_*constraint`、`set_particle_traction_*`），用于初始化与施加各类边界或荷载。
- **示例**：`example/mpm/ElementTest/CompressionMC.py` 72-155 行直接对 `mpm.scene.velocity_boundary[i]`、`traction_boundary[i]` 填写节点号、层级、速度或面力并更新 `velocity_list`/`traction_list`。

## 5. 时间步长与结果输出

- **时间步长与总时长**：`MPM.set_solver()` 在 `mainMPM.py` 100-109 行设置 `Timestep`、`SimulationTime`、`CFL`、`AdaptiveTimestep`、`SaveInterval`、`SavePath`。`Simulation.set_timestep()` 把值写入 `sims.dt` 和 `sims.delta`（`Simulation.py` 307-334 行）。
- **稳定性检查**：`MPM.check_critical_timestep()`（`mainMPM.py` 311-318 行）对显式求解检查 CFL 条件并可能缩小步长。
- **循环推进**：`Solver.Solver()` 用 `sims.delta` 更新时间，直到 `sims.current_time <= sims.time`（`MPMBase.py` 52-83 行）。
- **输出/监控**：`Solver.save_file()` 调用 `Recorder.WriteFile.output()`（`MPMBase.py` 41-44 行；`Recorder.py` 11-164 行），根据 `Simulation.monitor_type` 保存粒子/网格/对象数据并写入 VTK/NPZ。输出频率由 `SaveInterval` 控制，路径默认 `OutputData`。
- **输出选择**：`MPM.select_save_data()` 设置是否保存粒子/网格/对象（`mainMPM.py` 213-217 行）。

## 6. 核心 kernel 的调用链

- **引擎选择**：`MPM.add_engine()` 根据配置选择 `ULExplicitEngine`、`ULImplicitEngine`、`TLExplicitEngine` 等，并由 `Engine.choose_engine()` 将 `compute` 指向具体更新方案（`src/mpm/engines/Engine.py` 42-63 行），例如 USL/USF/MUSL/G2P2G。
- **显式 UL 引擎示例**（`src/mpm/engines/ULExplicitEngine.py`）：
  - `usl_updating()`：292-305 行，USL 更新顺序。
  - `usf_updating()`：307-323 行，USF 更新顺序。
  - `musl_updating()`：325-343 行，常用 MUSL 更新，依次执行 P2G 插值、网格动量/力计算、施加粒子与网格荷载、接触处理、G2P 回写、速度梯度与应力更新、平滑等。
- **一次步核心入口**：`Engine.compute` 在上述更新函数里调用 `EngineKernel` 中的 Taichi kernel（P2G/G2P、力与速度更新、应力积分等），典型 kernel 如 `grid_reset`、`calculate_interpolations`、`compute_grid_velocity`、`compute_stress_strain` 位于 `src/mpm/engines/EngineKernel.py`。
- **调用链串联**：`Solver.core()` → `engine.reset_grid_messages()`（网格清零，`EngineKernel.grid_reset` 等）→ `engine.build_neighbor_list()`（接触/邻居搜索）→ `engine.compute()`（选择的更新函数内部调用 `EngineKernel` 中的 `@ti.kernel` 实现 P2G/G2P、力学计算）→ 可选 `postprocess` 自定义 kernel。

## 7. 典型使用顺序（示例）

以 `example/mpm/ElementTest/CompressionMC.py` 为例：
1. `set_configuration()`：域大小、重力、映射与形函数。
2. `set_solver()`：时间步长、总时长、输出间隔。
3. `memory_allocate()`：材料/粒子/约束最大数量。
4. `add_material()`、`add_element()`、`add_region()`、`add_body()`：定义本构、网格、区域与粒子。
5. 填写 `scene.velocity_boundary` / `traction_boundary` 等边界与荷载。
6. `select_save_data()` 选择输出内容。
7. `run()` 执行求解并按间隔输出结果。

以上路径覆盖了材料、几何、边界/荷载、时间步长、输出以及核心 kernel 的调用位置，可作为快速定位和二次开发的索引。
