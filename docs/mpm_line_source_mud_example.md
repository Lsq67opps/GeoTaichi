# 在 GeoTaichi 中复现“二维线源瞬时抛泥”问题的最佳 MPM 起点

目标：在 GeoTaichi 中用现有 MPM 算例最小改动地复现文档《论文翻译.md》中的“二维线源瞬时抛泥”问题（平面应变/无限长线源，瞬时释放泥浆并向外扩散）。

## 最适合的起点算例

**`example/mpm/ColumnCollapse/NewtonianFluid2D.py`** —— 2D 牛顿流体自由面算例。

### 选择理由
- **同为 2D 单相流体**：脚本已设置 `material_type="Fluid"`、`Q4` 网格与自由表面演化，匹配泥浆视作牛顿流体的假设。
- **粒子/网格配置简单**：矩形区域 + 反射边界，便于改成“线源小区域瞬时释放”。
- **重力可开关**：可将 `gravity` 设为 `[0., 0.]`，符合无重力的瞬时抛泥或纯扩散情形；也可按需要开启重力。
- **可控分辨率与时间步长**：`ElementSize` 与 `nParticlesPerCell` 容易调节以满足 CFL/扩散尺度。
- **输出方便**：已有 `select_save_data(grid=True)`，如需粒子场可改为 `select_save_data(particle=True, grid=True)`。

## 将该算例改为“线源瞬时抛泥”的最小修改要点

1) **关闭或保留重力**  
   - 线源瞬时抛泥多用于无重力扩散：将 `gravity=[0., 0.]`。  
   - 若需含重力下塌，可保留 `gravity=[0., -9.8]`。

2) **初始化为小尺度线源区域**  
   - 设计算域宽高为 `Lx, Ly`，线源宽/高为 `w, h`（`w << Lx`，`h` 约等于粒子核尺度）。  
   - 将 `region1` 改成沿 \(x\) 方向细长、在 \(y\) 中心附近的窄矩形，如：  
     ```python
     "BoundingBoxPoint": [Lx/2 - w/2, Ly/2 - h/2],
     "BoundingBoxSize": [w, h]
     ```
   - 这样近似无限长线源（平面应变）。

3) **瞬时抛出/初速度设定**  
   - 在 `mpm.add_body` 中的 `Template` 里，为 `InitialVelocity` 字段赋予径向（或上下对称）速度脉冲，例如 `[0., 0.]` → `[0., ±u0]`，或在生成器里按粒子位置自定义。

4) **黏度/模量**  
   - 调整 `Viscosity` 与 `Modulus` 以匹配泥浆流变或弱可压缩声速，保持稳定时间步长：
     ```python
     "Viscosity": mu_mud,
     "Modulus":   K_eff   # 对应可压性/声速
     ```

5) **边界条件**  
   - 原脚本为全反射；若需外扩散无反射，可把边界改为更远的边界盒，或在求解区外围加吸收/远场（可简单增大域尺寸并在输出时截取内区）。

6) **输出粒子场**  
   - 改为 `mpm.select_save_data(particle=True, grid=True)` 以便后处理粒子浓度/速度云图。

## 备选与扩展

- **轴对称扩散**：若需轴对称（点源）而非线源，可参考 `example/mpm/Axisymmetric/Boussinesq.py` 的轴对称开关 `is_2DAxisy=True`，但该脚本为弹性体；要做流体需将材料改为 `Newtonian` 并调整边界/加载。
- **三维情形**：`example/mpm/ColumnCollapse/NewtonianFluid.py`（3D）可用于点源瞬时抛泥，但成本高。

## 结论

以 `example/mpm/ColumnCollapse/NewtonianFluid2D.py` 为基础，关闭重力、缩小初始区域以近似线源，并给定一次性速度脉冲或初始压力，即可最小代价复现“二维线源瞬时抛泥”问题。该脚本的网格、粒子与输出配置简单，便于快速迭代与对比。 
