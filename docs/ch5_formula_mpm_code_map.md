# 第五章应用模拟公式与MPM底层代码对照表

以下内容围绕《论文翻译.md》第五章“基于SPH方法的双流体模型在疏浚抛泥中的应用”中用于求解的关键公式，逐条对照本仓库 MPM 模块中描述相同物理问题的控制方程底层计算实现。格式均为“公式在前，代码在后”，并给出可直接访问的代码链接，便于后续依据论文公式修改 MPM 求解流程。

---

## 1. 两相体积平均质量守恒（式(4.23)，用于第五章泥沙团运动模拟的质量守恒）

公式：\[ \frac{\partial(\alpha_{k}\rho_{k})}{\partial t} + \frac{\partial(\alpha_{k}\rho_{k}u_{k j})}{\partial x_{j}} = 0 \]

对应底层计算代码（两相粒子质量与动量 P2G 映射）：

- `kernel_mass_momentum_p2g_twophase` 将固相、液相质量分别映射到网格节点，奠定后续质量守恒计算基础。  
  代码链接：[EngineKernel.py#L650-L670](https://github.com/Lsq67opps/GeoTaichi/blob/main/src/mpm/engines/EngineKernel.py#L650-L670)

```python
@ti.kernel
def kernel_mass_momentum_p2g_twophase(total_nodes: int, particleNum: int, node: ti.template(), particle: ti.template(), LnID: ti.template(), shapefn: ti.template(), node_size: ti.template()):
    ...
    nmass = shape_mapping(shapefn[ln], mass)
    nmass_s = shape_mapping(shapefn[ln], mass_s)
    nmass_f = shape_mapping(shapefn[ln], mass_f)
    node[nodeID, bodyID]._update_nodal_mass(nmass, nmass_s, nmass_f)
    node[nodeID, bodyID]._update_nodal_momentum(nmass * velocity, nmass_s * velocity_s, nmass_f * velocity_f)
```

---

## 2. 两相体积平均动量方程（式(4.24)，包含压力梯度、黏性应力、重力与相间作用力）

公式：\[ \frac{\partial(\alpha_{k}\rho_{k}u_{k i})}{\partial t} + \frac{\partial(\alpha_{k}\rho_{k}u_{k i}u_{k j})}{\partial x_{j}} = -\alpha_{k}\frac{\partial p}{\partial x_{i}} + \frac{\partial(\alpha_{k}\tau_{k i j})}{\partial x_{j}} + \alpha_{k}\rho_{k}g_{i} + F_{A k i} \]

对应底层计算代码（两相内力、重力与拖曳力汇聚到网格，再显式积分动量）：

- 网格力装配与相间拖曳（含重力）：`kernel_force_p2g_twophase2D` / `kernel_force_p2g_twophase`  
  代码链接：[EngineKernel.py#L897-L949](https://github.com/Lsq67opps/GeoTaichi/blob/main/src/mpm/engines/EngineKernel.py#L897-L949)

```python
@ti.kernel
def kernel_force_p2g_twophase2D(...):
    ...
    fex, fexf = particle[np]._compute_external_force(gravity)
    fInt, fintf = particle[np]._compute_internal_force()
    drag = particle[np]._compute_drag_force()
    ...
    node[nodeID, bodyID]._update_nodal_force(external_force + internal_force,
                                             external_forcef + drag_force + internal_forcef)
```

- 网格动量更新（显式积分 \(a = f/m\)）：`kernel_compute_grid_kinematic`、`kernel_compute_grid_kinematic_solid`、`kernel_compute_grid_kinematic_fluid`  
  代码链接：[EngineKernel.py#L1394-L1415](https://github.com/Lsq67opps/GeoTaichi/blob/main/src/mpm/engines/EngineKernel.py#L1394-L1415)

```python
@ti.kernel
def kernel_compute_grid_kinematic(cutoff: float, damp: float, node: ti.template(), dt: ti.template()):
    for ng in range(node.shape[0]):
        for nb in range(node.shape[1]):
            if node[ng, nb].m > cutoff:
                node[ng, nb]._compute_nodal_kinematic(damp, dt)
```

---

## 3. 云团边界判定与孔隙/浓度场表示（\[ \alpha_{s} = 0.1\,\alpha_{s}^{m} \] 作为云团边界条件）

公式：\[ \alpha_{s} = 0.1\,\alpha_{s}^{m} \]

对应底层计算代码（两相粒子携带孔隙度、压力并在内力计算中显式使用，为后续基于体积分数阈值的云团宽度/边界提取提供字段）：

- 两相粒子存储孔隙度与相压力，并计算体积力与拖曳力：`Particle._compute_internal_force` / `_compute_drag_force`  
  代码链接：[Particle.py#L230-L291](https://github.com/Lsq67opps/GeoTaichi/blob/main/src/mpm/structs/Particle.py#L230-L291)

```python
@ti.func
def _compute_drag_force(self):
    return -self.porosity * self.porosity * 9.8 * 1000 * self.vol * (self.vf - self.vs) / self.permeability

@ti.func  # total internal force, fluid internal force
def _compute_internal_force(self):
    fluid_pressure = ZEROVEC6f
    fluid_pressure[0] = self.pressure
    fluid_pressure[1] = self.pressure
    fluid_pressure[2] = self.pressure
    return -self.vol * (self.stress - fluid_pressure), self.vol * self.porosity * fluid_pressure
```

> 说明：第五章以 \(\alpha_{s} = 0.1\alpha_{s}^{m}\) 标记云团边界。MPM 中粒子级的 `porosity`、`pressure` 可在后处理时按照同样阈值提取云团宽度/边界，实现与论文定义一致的浓度场判别。

---

## 4. 无量纲特征速度与长度（\[ u_{0} = \sqrt{g\sqrt{q_{0}}} \]，\[ L_{0} = \sqrt{q_{0}} \]；用于第五章速度/距离无量纲化）

公式：\[ u_{0} = \sqrt{g\sqrt{q_{0}}} \]  
公式：\[ L_{0} = \sqrt{q_{0}} \]

对应底层计算代码（设置重力并在 P2G 阶段装配外力，支撑基于 \(g\) 与初始尺度的无量纲化处理）：

- 设置重力向量（示例脚本）：`example/mpm/ColumnCollapse/NewtonianFluid2D.py`  
  代码链接：[NewtonianFluid2D.py#L7-L21](https://github.com/Lsq67opps/GeoTaichi/blob/main/example/mpm/ColumnCollapse/NewtonianFluid2D.py#L7-L21)

```python
mpm.set_configuration(domain=[6., 6.],
                      ...
                      gravity=[0., -9.8],
                      material_type="Fluid",
                      velocity_projection="Affine")
mpm.set_solver({
    "Timestep":       1e-5,
    "SimulationTime": 4,
    ...
})
```

- 将粒子体力 \( \rho g \) 映射到网格：`kernel_force_p2g_2D` 中外力项  
  代码链接：[EngineKernel.py#L699-L733](https://github.com/Lsq67opps/GeoTaichi/blob/main/src/mpm/engines/EngineKernel.py#L699-L733)

```python
fex = particle[np]._compute_external_force(gravity)
external_force = shape_mapping(shapefn[ln], fex)
node[nodeID, bodyID]._update_nodal_force(external_force + internal_force)
```

> 说明：论文中的 \(u_{0}\) 与 \(L_{0}\) 依赖 \(g\) 与初始面积 \(q_{0}\)。MPM 侧通过显式设置 `gravity` 与初始几何尺寸（网格单元大小、初始云团区域）来保持同样的特征尺度，随后即可按论文给出的 \(u_{0}, L_{0}\) 对速度、距离进行无量纲化后处理。

---

以上映射覆盖了第五章应用模拟中涉及的核心控制方程（质量守恒、动量守恒/相间作用力、浓度边界判定、无量纲特征尺度）与 MPM 模块的最底层计算实现，可直接作为后续修改或扩展 MPM 求解以重现论文第五章抛泥模拟的定位参考。
