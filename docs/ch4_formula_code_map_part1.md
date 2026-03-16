# 第4章公式与仓库代码对应表

本文档根据《论文翻译.md》第4章的 140 个公式逐一列出在仓库中的底层实现位置。如果仓库未包含对应的 SPH 双流体实现，则明确标注未找到直接代码。所有条目均按照“代码在前、公式在后”的顺序呈现。

## 公式 (4.1)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ f(x) = \int_{\Omega}f(x^{\prime})\delta (x^{\prime} - x)\mathrm{d}\Omega_{x^{\prime}} \quad (4.1) ]

## 公式 (4.2)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ f(x) \approx \int_{\Omega} f(x^{\prime}) W(x^{\prime} - x, h) \mathrm{d}\Omega_{x^{\prime}} \quad (4.2) ]

## 公式 (4.3)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ f(x) \approx \sum_{j = 1}^{N} f(x_{j}) W(x_{j} - x, h) \mathrm{d}V_{j} \quad (4.3) ]

## 公式 (4.4)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \int_{\Omega}W(x^{\prime} - x,h)\mathrm{d}\Omega_{x^{\prime}} = 1 \quad (4.4) ]

## 公式 (4.5)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \lim_{h\to 0}W(x^{\prime} - x,h) = \delta (x^{\prime} - x) \quad (4.5) ]

## 公式 (4.7)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \begin{array}{r l} & \left[\frac{\partial f}{\partial x}\right]_{x_{i}}\approx \sum_{j = 1}^{N}f(x_{j})\frac{\partial W}{\partial x}\mathrm{d}V_{j}\\ & \left[\frac{\partial^{2}f}{\partial x^{2}}\right]_{x_{i}}\approx \sum_{j = 1}^{N}f(x_{j})\frac{\partial^{2}W}{\partial x^{2}}\mathrm{d}V_{j} \end{array} \quad (4.7) ]

## 公式 (4.8)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \left[\frac{\partial f}{\partial x}\right]_{x_{i}}\approx \sum_{j = 1}^{N}\frac{\phi(x_{j})}{\phi(x_{i})} [f(x_{j}) - f(x_{i})]\frac{\partial W}{\partial x}\mathrm{d}V_{j} \quad (4.8) ]

## 公式 (4.9)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \left[\frac{\partial f}{\partial x}\right]_{x_{i}}\approx \sum_{j = 1}^{N}\left[\frac{\phi(x_{j})}{\phi(x_{i})} f(x_{j}) + \frac{\phi(x_{j})}{\phi(x_{i})} f(x_{i})\right]\frac{\partial W}{\partial x}\mathrm{d}V_{j} \quad (4.9) ]

## 公式 (4.10)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \left[\frac{\partial^{2}f}{\partial x^{2}}\right]_{x_{i}}\approx 2\sum_{j = 1}^{N}\frac{f(x_{i}) - f(x_{j})}{x_{x_{i}} - x_{x_{j}}}\frac{\partial W}{\partial x}\mathrm{d}V_{j} \quad (4.10) ]

## 公式 (4.11)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \rho_{i} = \frac{\sum_{j = 1}^{N}\rho_{j}W_{ij}\mathrm{d}V_{j}}{\sum_{j = 1}^{N}W_{ij}\mathrm{d}V_{j}} \quad (4.11) ]

## 公式 (4.12)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \frac{\partial\rho_{k}}{\partial t} +\frac{\partial(\rho_{k}u_{k j})}{\partial x_{j}} = 0 \quad (4.12) ]

## 公式 (4.13)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \frac{\partial(\rho_{k}u_{k i})}{\partial t} +\frac{\partial(\rho_{k}u_{k i}u_{k j})}{\partial x_{j}} = -\frac{\partial p_{k}}{\partial x_{i}} +\frac{\partial\tau_{k i j}}{\partial x_{j}} +\rho_{k}g_{i} \quad (4.13) ]

## 公式 (4.14)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \langle \phi_{k}\rangle = \frac{1}{V}\int_{V}\phi_{k}\mathrm{d}V \quad (4.14) ]

## 公式 (4.15)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \hat{\phi}_{k} = \frac{1}{V_{k}}\int_{V_{k}}\phi_{k}\mathrm{d}V \quad (4.15) ]

## 公式 (4.16)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \langle \phi_{k}\rangle = \frac{\alpha_{k}}{V_{k}}\int_{V_{k}}\phi_{k}\mathrm{d}V = \alpha_{k}\hat{\phi}_{k} \quad (4.16) ]

## 公式 (4.17)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \langle \frac{\partial\phi_{k}}{\partial t}\rangle = \frac{\partial\langle\phi_{k}\rangle}{\partial t} -\frac{1}{V}\int_{A}\phi_{k}u_{A k j}n_{A k j}\mathrm{d}A \quad (4.17) ]

## 公式 (4.18)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \langle \frac{\partial\phi_{k}}{\partial x_{i}}\rangle = \frac{\partial\langle\phi_{k}\rangle}{\partial x_{i}} +\frac{1}{V}\int_{A}\phi_{k}n_{A k i}\mathrm{d}A \quad (4.18) ]

## 公式 (4.19)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \frac{\partial(\alpha_{k}\hat{\rho}_{k})}{\partial t} +\frac{\partial(\alpha_{k}\hat{\rho}_{k}\hat{u}_{k j})}{\partial x_{j}} = \frac{1}{V}\int_{A}\rho_{k}(u_{A k j} - u_{k j})n_{A k j}\mathrm{d}A \quad (4.19) ]

## 公式 (4.x-19)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \frac{\partial(\alpha_{k}\hat{\rho}_{k}\hat{u}_{k i})}{\partial t} +\frac{\partial(\alpha_{k}\hat{\rho}_{k}\hat{u}_{k i}\hat{u}_{k j})}{\partial x_{j}} = -\frac{\partial(\alpha_{k}\hat{\rho}_{k})}{\partial x_{i}} +\frac{\partial(\alpha_{k}\hat{\tau}_{k i j})}{\partial x_{j}} +\alpha_{k}\hat{\rho}_{k}g_{i} + \frac{1}{V}\int_{A}\rho_{k}u_{k i}(u_{A k j} - u_{k j})n_{A k j}\mathrm{d}A - \frac{1}{V}\int_{A}\rho_{A k}n_{A k i}\mathrm{d}A + \frac{1}{V}\int_{A}\tau_{A k i j}n_{A k j}\mathrm{d}A ]

## 公式 (4.21)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ -\frac{1}{V}\int_{A}\rho_{A k}n_{A k i}\mathrm{d}A = \hat{p}_{A k}(-\frac{1}{V}\int_{A}n_{A k i}\mathrm{d}A) = \hat{p}_{A k}\frac{\partial\alpha_{k}}{\partial x_{i}} \quad (4.21) ]

## 公式 (4.22)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ F_{A k i} = \frac{1}{V}\int_{A}\tau_{A k i j}n_{A k j}\mathrm{d}A \quad (4.22) ]

## 公式 (4.23)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \frac{\partial(\alpha_{k}\rho_{k})}{\partial t} +\frac{\partial(\alpha_{k}\rho_{k}u_{k j})}{\partial x_{j}} = 0 \quad (4.23) ]

## 公式 (4.24)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \frac{\partial(\alpha_{k}\rho_{k}u_{k i})}{\partial t} +\frac{\partial(\alpha_{k}\rho_{k}u_{k i}u_{k j})}{\partial x_{j}} = -\alpha_{k}\frac{\partial\rho_{j}}{\partial x_{i}} +\frac{\partial(\alpha_{k}\tau_{k i j})}{\partial x_{j}} +\alpha_{k}\rho_{k}g_{i} + F_{A k i} \quad (4.24) ]

## 公式 (4.25)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \bar{\phi}_{k} = \frac{\alpha_{k}\rho_{k}\bar{\phi}_{k}}{\alpha_{k}\rho_{k}} \quad (4.25) ]

## 公式 (4.26)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \left\{ \begin{array}{l}\displaystyle \frac{\partial\phi_{k}}{\partial t} = \frac{\partial\bar{\phi}_{k}}{\partial t} \\ \displaystyle \frac{\partial\phi_{k}}{\partial x_{i}} = \frac{\partial\bar{\phi}_{k}}{\partial x_{i}} \end{array} \right. \quad (4.26) ]

## 公式 (4.27)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \frac{\partial(\overline{{\alpha_{k}\rho_{k}}})}{\partial t} +\frac{\partial(\overline{{\alpha_{k}\rho_{k}}}\overline{{u}}_{k j})}{\partial x_{j}} = 0 \quad (4.27) ]

## 公式 (4.x-27)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \frac{\partial(\overline{{\alpha_{k}\rho_{k}}}\overline{{u}}_{k i})}{\partial t} +\frac{\partial(\overline{{\alpha_{k}\rho_{k}}}\overline{{u}}_{k j}\overline{{u}}_{k j})}{\partial x_{j}} = -\overline{{\alpha_{k}}}\frac{\partial p_{f}}{\partial x_{i}} +\frac{\partial(\overline{{\alpha_{k}}}\tau_{k i j})}{\partial x_{j}} +\overline{{\alpha_{k}\rho_{k}}}\overline{{g}}_{i} + ]

## 公式 (4.x-28)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \widehat{F}_{A k i} + \frac{\partial[\overline{{\alpha_{k}\rho_{k}}} (\overline{{u}}_{k i}\overline{{u}}_{k j} - \overline{{u}}_{k i}\overline{{u}}_{k j})]}{\partial x_{j}} ]

## 公式 (4.28)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ (4.28) ]

## 公式 (4.29)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ -\alpha_{k}\frac{\partial p_{f}}{\partial x_{i}} = -\hat{\alpha}_{k}\frac{\partial\hat{p}_{f}}{\partial x_{i}} \quad (4.29) ]

## 公式 (4.30)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \frac{\partial\overline{{\alpha_{k}\tau_{kij}}}}{\partial x_{j}} = \frac{\partial}{\partial x_{j}}\left(\overline{{\alpha_{k}\rho_{k}}}\frac{\tau_{kij}}{\rho_{k}}\right) \quad (4.30) ]

## 公式 (4.31)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \frac{\overline{{\tau}}_{kij}}{\rho_{k}} = \nu_{k}^{0}\left[\frac{\partial\overline{{u}}_{k i}}{\partial x_{j}} +\frac{\partial\overline{{u}}_{k j}}{\partial x_{i}}\right] \quad (4.31) ]

## 公式 (4.32)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \nu_{s}^{0} = \frac{1.2\lambda^{2}\nu_{f}^{0}\rho_{f}}{\rho_{s}} \quad (4.32) ]

## 公式 (4.33)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \lambda = \left[\left(\frac{\alpha_{s m}}{\hat{\alpha}_{s}}\right)^{1 / 3} - 1\right]^{-1} \quad (4.33) ]

## 公式 (4.34)

**代码位置：** `src/mpdem/fluid_dynamics/DragForceModel.py` [L87-L92](https://github.com/Lsq67opps/GeoTaichi/blob/main/src/mpdem/fluid_dynamics/DragForceModel.py#L87-L92)  \
**对应关系说明：** 线性拖曳力律用于计算粒子与流体之间的拖曳项，形式对应式(4.34)的 F_{Asi}。

```python
    def linear_drag_law(self, fluid_volume_fraction, fluid_density, fluid_viscosity, particle_radius, relative_velocity):
        particle_reynold = self.compute_particle_reynold(fluid_volume_fraction, fluid_density, fluid_viscosity, particle_radius, relative_velocity)
        particle_volume = 4. / 3. * PI * particle_radius * particle_radius * particle_radius
        beta = self.GidaspowModel(fluid_volume_fraction, fluid_density, fluid_viscosity, particle_radius, particle_reynold, relative_velocity)
        drag_force = particle_volume / (1. - fluid_volume_fraction) * beta * relative_velocity
        return drag_force
```

**公式：**
[ F_{A s i} = \lambda_{d}\alpha_{s}\frac{3C_{D}\rho_{f}}{4d_{p}}\left|u_{f} - u_{s}\right|\left(u_{f i} - u_{s i}\right) \quad (4.34) ]

## 公式 (4.35)

**代码位置：** `src/mpdem/fluid_dynamics/SemiResolved.py` [L68-L72](https://github.com/Lsq67opps/GeoTaichi/blob/main/src/mpdem/fluid_dynamics/SemiResolved.py#L68-L72)  \
**对应关系说明：** 拖曳力映射到流体场，实现 F_{Af i} = -F_{As i} 的对称作用。

```python
        relative_velocity = velocity_f - particle[np].v
        drag_force = drag_coefficient_model.drag_law(epsilon_f, fluid_density, fluid_viscosity, particle_radius, relative_velocity)
        interaction_force = drag_force + particle_volume * force_f #- particle_volume * fluid_density * gravity 
        particle[np].contact_force += interaction_force
        drag_force_mapping(influence_domain, cnum, grid_size, igrid_size, position, particle_radius, normalized_cell_volume, cell_drag_force, -drag_force)
```

**公式：**
[ F_{A f i} = -F_{A s i} \quad (4.35) ]

## 公式 (4.36)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \widehat{F}_{A s i} = \gamma \widehat{\alpha}_{s}\left(u_{f i} - u_{s i}\right) \quad (4.36) ]

## 公式 (4.37)

**代码位置：** `src/mpdem/fluid_dynamics/DragForceModel.py` [L86-L100](https://github.com/Lsq67opps/GeoTaichi/blob/main/src/mpdem/fluid_dynamics/DragForceModel.py#L86-L100)  \
**对应关系说明：** 拖曳系数随粒子雷诺数和相对速度更新，对应式(4.37)的 \gamma 计算。

```python
    @ti.func
    def linear_drag_law(self, fluid_volume_fraction, fluid_density, fluid_viscosity, particle_radius, relative_velocity):
        particle_reynold = self.compute_particle_reynold(fluid_volume_fraction, fluid_density, fluid_viscosity, particle_radius, relative_velocity)
        particle_volume = 4. / 3. * PI * particle_radius * particle_radius * particle_radius
        beta = self.GidaspowModel(fluid_volume_fraction, fluid_density, fluid_viscosity, particle_radius, particle_reynold, relative_velocity)
        drag_force = particle_volume / (1. - fluid_volume_fraction) * beta * relative_velocity
        return drag_force

    @ti.func
    def quadratic_drag_law(self, fluid_volume_fraction, fluid_density, fluid_viscosity, particle_radius, relative_velocity):
        particle_reynold = self.compute_particle_reynold(fluid_volume_fraction, fluid_density, fluid_viscosity, particle_radius, relative_velocity)
        kappa = 3.7 - 0.65 * ti.exp(-0.5 * (1.5 - ti.log(particle_reynold)) * (1.5 - ti.log(particle_reynold)))
        drag_coeff = self.drag_coefficient(particle_reynold)
        drag_force = 0.5 * PI * drag_coeff * fluid_density * particle_radius * particle_radius * fluid_volume_fraction ** (2. - kappa) * relative_velocity.norm() * relative_velocity
        return drag_force
```

**公式：**
[ \gamma = \lambda_{d}\frac{3C_{D}\rho_{f}}{4d_{p}}\left|\bar{u}_{f} - \bar{u}_{s}\right| \quad (4.37) ]

## 公式 (4.38)

**代码位置：** `src/mpdem/fluid_dynamics/DragForceModel.py` [L54-L83](https://github.com/Lsq67opps/GeoTaichi/blob/main/src/mpdem/fluid_dynamics/DragForceModel.py#L54-L83)  \
**对应关系说明：** Schiller-Naumann 模型的分段 Cd 实现，对应式(4.38)。

```python
    def SchillerNaumannModel(self, particle_reynold):
        Cd0 = 24. / particle_reynold * (1. + 0.15 * particle_reynold ** 0.687)
        return Cd0

    @ti.func
    def BrownLawlerModel(self, particle_reynold):
        Cd0 = 24. / particle_reynold * (1. + 0.15 * particle_reynold ** 0.681) + 0.407 / (1. + 8710 / particle_reynold)
        return Cd0

    @ti.func
    def EmpiricalModel(self, particle_reynold):
        temp_val = 0.63 + 1.5 / ti.sqrt(particle_reynold)
        Cd0 = temp_val * temp_val
        return Cd0

    @ti.func
    def AbrahamModel(self, particle_reynold):
        temp_val = 1. + 9.06 / ti.sqrt(particle_reynold)
        Cd0 = 24. / (9.06 * 9.06) * temp_val * temp_val
        return Cd0

    @ti.func
    def drag_coefficient(self, particle_reynold):
        Cd0 = 0.
        if particle_reynold <= 1.:
            Cd0 = 24. / particle_reynold
        elif particle_reynold < 1000.:
            Cd0 = self.drag_coefficient_model(particle_reynold)
        else:
            Cd0 = 0.44
```

**公式：**
[ C_{D} = \left\{ \begin{array}{l l} \displaystyle \frac{24}{Re_{s}} (1.0 + 0.15 Re_{s}^{0.687}) & Re_{s}< 1000\\ 0.44 & Re_{s} \geq 1000 \end{array} \right. \quad (4.38) ]

## 公式 (4.39)

**代码位置：** `src/mpdem/fluid_dynamics/DragForceModel.py` [L41-L51](https://github.com/Lsq67opps/GeoTaichi/blob/main/src/mpdem/fluid_dynamics/DragForceModel.py#L41-L51)  \
**对应关系说明：** Gidaspow 模型中的 (1-α_s)^{-1.65} 修正与式(4.39)的 λ_d 形式相同。

```python
    def GidaspowModel(self, fluid_volume_fraction, fluid_density, fluid_viscosity, particle_radius, particle_reynold, relative_velocity):
        beta = 0.
        relative_velocity_norm = relative_velocity.norm()
        solid_volume_fraction = 1. - fluid_volume_fraction
        particle_diameter = 2. * particle_radius
        if fluid_volume_fraction <= 0.8:
            beta = 150 * solid_volume_fraction * solid_volume_fraction * fluid_viscosity / (fluid_volume_fraction * particle_diameter * particle_diameter) + 1.75 * solid_volume_fraction * fluid_density / particle_diameter * relative_velocity_norm
        else:
            Cd = self.SchillerNaumannModel(particle_reynold)
            beta = 0.75 * Cd * fluid_density * relative_velocity_norm * solid_volume_fraction / particle_diameter * fluid_volume_fraction ** (-1.65)
        return beta
```

**公式：**
[ \lambda_{d} = \frac{1}{(1 - \widehat{\alpha}_{s})^{1.65}} \quad (4.39) ]

## 公式 (4.40)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \widehat{\alpha_{s}u_{f i}} = \widehat{\alpha}_{s}\widetilde{u}_{f i} + \left[1 + \frac{\widehat{\alpha}_{s}}{\widehat{\alpha}_{f}}\right]\widehat{\Delta\alpha_{s}}\Delta u_{f i} \quad (4.40) ]

## 公式 (4.41)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \overline{{\Delta\alpha_{s}\Delta u_{f i}}} = -\frac{\nu_{f}^{S P S}}{S c}\frac{\partial\tilde{\alpha}_{s}}{\partial x_{i}} = -\epsilon_{s}\frac{\partial\tilde{\alpha}_{s}}{\partial x_{i}} \quad (4.41) ]

## 公式 (4.42)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \widehat{F}_{A s i} = \gamma \hat{\alpha}_{s}(\bar{u}_{f i} - \bar{u}_{s i}) - \gamma \frac{\epsilon_{s}}{\hat{\alpha}_{f}}\frac{\partial\hat{\alpha}_{s}}{\partial x_{i}} \quad (4.42) ]

## 公式 (4.43)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \frac{\overline{{\tau_{k i j}^{S P S}}}}{\rho_{k}} = \overline{{u}}_{k i}\overline{{u}}_{k j} - \overline{{u}}_{k i}\overline{{u}}_{k j} \quad (4.43) ]

## 公式 (4.44)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \frac{\overline{{\tau_{k i j}^{S P S}}}}{\rho_{k}} = \nu_{k}^{S P S}\left(\frac{\partial\overline{{u}}_{k i}}{\partial x_{j}} +\frac{\partial\overline{{u}}_{k j}}{\partial x_{i}}\right) \quad (4.44) ]

## 公式 (4.45)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \nu_{f}^{SPS} = (C_{s}\Delta)^{2} |S_{f}| (1 + n\alpha_{s})^{-1} \quad (4.45) ]

## 公式 (4.46)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \nu_{s}^{SPS} = (C_{s}\Delta)^{2} |S_{s}| \quad (4.46) ]

## 公式 (4.47)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ |S_{k}| = \sqrt{2\frac{\partial u_{k i}}{\partial x_{j}}\frac{\partial u_{k j}}{\partial x_{i}}} \quad (4.47) ]

## 公式 (4.48)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \tau_{k i j}^{*} = \nu_{k}^{0}\left(\frac{\partial u_{k i}}{\partial x_{j}} + \frac{\partial u_{k j}}{\partial x_{i}}\right) + \nu_{k}^{SPS}\left(\frac{\partial u_{k i}}{\partial x_{j}} + \frac{\partial u_{k j}}{\partial x_{i}}\right) \quad (4.48) ]

## 公式 (4.49)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \tau_{k i j}^{*} = (\nu_{k}^{0} + \nu_{k}^{SPS})\left(\frac{\partial u_{k i}}{\partial x_{j}} + \frac{\partial u_{k j}}{\partial x_{i}}\right) \quad (4.49) ]

## 公式 (4.50)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \nu_{k}^{*} = \nu_{k}^{0} + \nu_{k}^{SPS} \quad (4.50) ]

## 公式 (4.51)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \frac{\partial(\alpha_{k}\rho_{k})}{\partial t} +\frac{\partial(\alpha_{k}\rho_{k}u_{k j})}{\partial x_{j}} = 0 \quad (4.51) ]

## 公式 (4.x-53)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \frac{\partial(\alpha_{k}\rho_{k}u_{k i})}{\partial t} +\frac{\partial(\alpha_{k}\rho_{k}u_{k i}u_{k j})}{\partial x_{j}} = -\alpha_{k}\frac{\partial p_{f}}{\partial x_{i}} +\frac{\partial(\alpha_{k}\rho_{k}\tau_{k i j}^{*})}{\partial x_{j}} + ]

## 公式 (4.52)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ (-1)^{\delta_{f k}}\gamma \alpha_{s}(u_{f i} - u_{s i}) - (-1)^{\delta_{f k}}\gamma \frac{\epsilon_{s}}{\alpha_{f}}\frac{\partial\alpha_{s}}{\partial x_{i}} +\alpha_{k}\rho_{k}g_{i} \quad (4.52) ]

## 公式 (4.53)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \frac{\mathrm{d}\phi_{k}}{\mathrm{d}t} = \frac{\partial\phi_{k}}{\partial t} +u_{f j}\frac{\partial\phi_{k}}{\partial x_{j}} \quad (4.53) ]

## 公式 (4.54)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \frac{\mathrm{d}X_{p i}}{\mathrm{d}t} = u_{f i} \quad (4.54) ]

## 公式 (4.x-57)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \frac{\mathrm{d}u_{f i}}{\mathrm{d}t} = -\frac{1}{\rho_{f_{0}}}\frac{\partial p_{f}}{\partial x_{i}} +\frac{1}{\alpha_{f}\rho_{f}}\frac{\partial(\alpha_{f}\rho_{f}\tau_{f i j}^{*})}{\partial x_{j}} +g_{i} - ]

## 公式 (4.55)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \frac{\gamma\alpha_{s}}{\alpha_{f}\rho_{f}} (u_{f i} - u_{s i}) + \frac{\gamma}{\alpha_{f}\rho_{f}}\frac{\epsilon_{s}}{\alpha_{f}}\frac{\partial\alpha_{s}}{\partial x_{i}} \quad (4.55) ]

## 公式 (4.56)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \frac{\mathrm{d}m_{f_{a}}}{\mathrm{d}t} = \frac{\mathrm{d}(\alpha_{f}\rho_{f}V_{a})}{\mathrm{d}t} = 0 \quad (4.56) ]

## 公式 (4.57)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \frac{\mathrm{d}(\alpha_{f}\rho_{f})}{\mathrm{d}t} = -(\alpha_{f}\rho_{f})\frac{\partial u_{f j}}{\partial x_{j}} \quad (4.57) ]

## 公式 (4.58)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ -\frac{1}{V_{a}}\frac{\mathrm{d}V_{a}}{\mathrm{d}t} = \frac{\partial u_{f j}}{\partial x_{j}} \quad (4.58) ]

## 公式 (4.59)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \frac{\mathrm{d}\alpha_{s}}{\mathrm{d}t} = -\frac{\partial(\alpha_{s}u_{s j})}{\partial x_{j}} +u_{f j}\frac{\partial\alpha_{s}}{\partial x_{j}} \quad (4.59) ]

## 公式 (4.60)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \frac{\mathrm{d}\alpha_{s}}{\mathrm{d}t} = -\alpha_{s}\frac{\partial u_{f j}}{\partial x_{j}} -\frac{\partial[\alpha_{s}(u_{s j} - u_{f j})]}{\partial x_{j}} \quad (4.60) ]

## 公式 (4.x-64)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \frac{\partial(\alpha_{s}\rho_{s}u_{s i})}{\partial t} +\frac{\partial(\alpha_{s}\rho_{s}u_{s i}u_{s j})}{\partial x_{j}} = \alpha_{s}\rho_{s}\frac{\partial u_{s i}}{\partial t} +\alpha_{s}\rho_{s}u_{s j}\frac{\partial u_{s i}}{\partial x_{j}} ]

## 公式 (4.x-65)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ = \alpha_{s}\rho_{s}\frac{\mathrm{d}u_{s i}}{\mathrm{d}t} +\alpha_{s}\rho_{s}(u_{s j} - u_{f j})\frac{\partial u_{s i}}{\partial x_{j}} ]

## 公式 (4.61)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ = \alpha_{s}\rho_{s}\frac{\mathrm{d}u_{s i}}{\mathrm{d}t} +\alpha_{s}\rho_{s}\Bigg\{\frac{\partial[u_{s i}(u_{s j} - u_{f j})]}{\partial x_{j}} -u_{s i}\frac{\partial(u_{s j} - u_{f j})}{\partial x_{j}}\Bigg\} \quad (4.61) ]

## 公式 (4.62)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \frac{\mathrm{d}u_{s i}}{\mathrm{d}t} = -\frac{\partial[u_{s i}(u_{s j} - u_{f j})]}{\partial x_{j}} +u_{s i}\frac{\partial(u_{s j} - u_{f j})}{\partial x_{j}} -\frac{1}{\rho_{s}}\frac{\partial p_{f}}{\partial x_{i}} +g_{i} + \frac{\partial(\tau_{s i j}^{*})}{\partial x_{j}} +\frac{\tau_{s i j}^{*}}{\alpha_{s}}\frac{\partial\alpha_{s}}{\partial x_{j}} +\frac{\gamma}{\rho_{s}}(u_{f i} - u_{s i}) - \frac{\gamma}{\alpha_{s}\rho_{s}}\frac{\epsilon_{s}}{\alpha_{f}}\frac{\partial\alpha_{s}}{\partial x_{i}} \quad (4.62) ]

## 公式 (4.x-68)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \frac{\mathrm{d}u_{s i}}{\mathrm{d}t} = -\frac{\partial\big[u_{s i}(u_{s j} - u_{f j})\big]}{\partial x_{j}} +u_{s i}\frac{\partial(u_{s j} - u_{f j})}{\partial x_{j}} -\frac{1}{\rho_{s}}\frac{\partial p_{f}}{\partial x_{i}} +g_{i} + ]

## 公式 (4.63)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \frac{\partial(\tau_{s i j}^{*})}{\partial x_{j}} +\tau_{s i j}^{*}\frac{\partial\ln\alpha_{s}}{\partial x_{j}} +\frac{\gamma}{\rho_{s}}(u_{f i} - u_{s i}) - \frac{\gamma}{\rho_{s}}\frac{\epsilon_{s}}{\alpha_{f}}\frac{\partial\ln\alpha_{s}}{\partial x_{i}} \quad (4.63) ]

## 公式 (4.64)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \frac{\mathrm{d}X_{p i}}{\mathrm{d}t} = u_{f i} \quad (4.64) ]

## 公式 (4.x-71)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \frac{\mathrm{d}u_{f i}}{\mathrm{d}t} = \frac{1}{\rho_{f_{0}}}\frac{\partial p_{f}}{\partial x_{i}} +\frac{1}{\alpha_{f}\rho_{f}}\frac{\partial(\alpha_{f}\rho_{f}\tau_{f i j}^{*})}{\partial x_{j}} +g_{i} - ]

## 公式 (4.65)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \frac{\gamma\alpha_{s}}{\alpha_{f}\rho_{f}}(u_{f i} - u_{s i}) + \frac{\gamma\alpha_{s}}{\alpha_{f}\rho_{f}}\frac{\epsilon_{s}}{\alpha_{f}}\frac{\partial\ln\alpha_{s}}{\partial x_{i}} \quad (4.65) ]

## 公式 (4.66)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \frac{\mathrm{d}(\alpha_{f}\rho_{f})}{\mathrm{d}t} = -(\alpha_{f}\rho_{f})\frac{\partial u_{f j}}{\partial x_{j}} \quad (4.66) ]

## 公式 (4.67)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \frac{\mathrm{d}\alpha_{s}}{\mathrm{d}t} = -\alpha_{s}\frac{\partial u_{f j}}{\partial x_{j}} -\frac{\partial[\alpha_{s}(u_{s j} - u_{f j})]}{\partial x_{j}} \quad (4.67) ]

## 公式 (4.x-75)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \frac{\mathrm{d}u_{s i}}{\mathrm{d}t} = -\frac{\partial\big[u_{s i}(u_{s j} - u_{f j})\big]}{\partial x_{j}} +u_{s i}\frac{\partial(u_{s j} - u_{f j})}{\partial x_{j}} -\frac{1}{\rho_{s}}\frac{\partial p_{f}}{\partial x_{i}} +g_{i} + ]

## 公式 (4.68)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ \frac{\partial(\tau_{s i j}^{*})}{\partial x_{j}} +\tau_{s i j}^{*}\frac{\partial\ln\alpha_{s}}{\partial x_{j}} +\frac{\gamma}{\rho_{s}}(u_{f i} - u_{s i}) - \frac{\gamma}{\rho_{s}}\frac{\epsilon_{s}}{\alpha_{f}}\frac{\partial\ln\alpha_{s}}{\partial x_{i}} \quad (4.68) ]

## 公式 (4.69)

**代码位置：** 未找到与该公式直接对应的实现（GeoTaichi 仓库主要提供 DEM/MPM/DEM-MPM 计算，未包含文中 SPH 双流体离散核）。\
**对应关系说明：** 需要新增 SPH 双流体求解模块后才能对应该公式。

```text
// 未找到对应实现
```

**公式：**
[ p_{f} = \frac{c_{0}^{2}\rho_{f_{0}}}{\gamma^{\prime}}\left[\left[\frac{\rho_{f}}{\rho_{f_{0}}}\right]^{\gamma^{\prime}} - 1\right] \quad (4.69) ]
