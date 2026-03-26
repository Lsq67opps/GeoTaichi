# 第5章二维线源瞬时抛泥 SPH 问题全流程公式整理

对“静水中二维线源瞬时抛泥”算例，汇总建模、离散、条件设定与求解全过程涉及的控制方程与计算公式，便于实现或复现。

## 1. 连续介质控制方程（双流体）
对相 \(k=f,s\)（水/泥沙），体积分数 \(\alpha_k\) 满足 \(\alpha_f+\alpha_s=1\)。

- 质量守恒  
  \[
  \frac{\partial(\alpha_k\rho_k)}{\partial t}+\nabla\cdot(\alpha_k\rho_k\mathbf{u}_k)=0
  \]
- 动量守恒  
  \[
  \frac{\partial(\alpha_k\rho_k\mathbf{u}_k)}{\partial t}
  +\nabla\cdot(\alpha_k\rho_k\mathbf{u}_k\mathbf{u}_k)
  =-\alpha_k\nabla p+\nabla\cdot(\alpha_k\boldsymbol{\tau}_k)+\alpha_k\rho_k\mathbf{g}+\mathbf{F}_{Ak}
  \]
  相间作用 \(\mathbf{F}_{Af}=-\mathbf{F}_{As}=\gamma(\mathbf{u}_s-\mathbf{u}_f)+\) 扩散项；泥沙分压忽略，共享压力场。
- 状态方程（弱可压 Tait，式(4.105)，\(\gamma=7\)，\(c_0=10\sqrt{gH}\) 以保证密度涨落 \(\lesssim1\%\)）  
  \[
  (p_f)_a=\frac{\rho_{f0}c_0^{2}}{\gamma}\left(\left[\frac{(\alpha_f\rho_f)_a+(\alpha_s)_a\rho_{f0}}{(\alpha_f\rho_f)_a}\right]^{\gamma}-1\right)
  \]

## 2. SPH 离散公式（单组粒子）
- 轨迹与携量（式(4.100)）  
  \[
  \frac{dX_{ai}}{dt}=(u_{fi})_a
  \]
- 水相动量（式(4.101)）  
  \[
  \frac{d(u_{fi})_a}{dt}= -\frac{1}{\rho_{f0}}\sum_b[(p_f)_a+(p_f)_b]\nabla_a W_{ab}^i V_b+g_i
  \]
  \[
  +\frac{1}{(\alpha_f\rho_f)_a}\sum_b[(\alpha_f\rho_f)_a(\tau^{*}_{fij})_a+(\alpha_f\rho_f)_b(\tau^{*}_{fij})_b]\nabla_a W_{ab}^j V_b
  \]
  \[
  -\frac{\gamma_a(\alpha_s)_a}{(\alpha_f\rho_f)_a}[(u_{fi})_a-(u_{si})_a]
  +\frac{\gamma_a(\alpha_s)_a}{(\alpha_f\rho_f)_a}\frac{(\epsilon_s)_a}{(\alpha_f)_a}\sum_b\ln\frac{(\alpha_s)_b}{(\alpha_s)_a}\nabla_a W_{ab}^i V_b
  \]
- 水相连续（式(4.102)）  
  \[
  \frac{d(\alpha_f\rho_f)_a}{dt}=(\alpha_f\rho_f)_a\sum_b[(u_{fj})_a-(u_{fj})_b]\nabla_a W_{ab}^j V_b
  \]
- 泥沙体积分数（式(4.103)）  
  \[
  \frac{d(\alpha_s)_a}{dt}=(\alpha_s)_a\sum_b[(u_{fj})_a-(u_{fj})_b]\nabla_a W_{ab}^j V_b -
  \]
  \[
  \sum_b V_b\{\max[(u_{sj}-u_{fj})_a\nabla_a W_{ab}^j,0](\alpha_s)_a+
  \min[(u_{sj}-u_{fj})_b\nabla_a W_{ab}^j,0](\alpha_s)_b\}
  \]
- 泥沙动量（式(4.104)）  
  \[
  \frac{d(u_{si})_a}{dt}= \sum_b \min[(u_{sj}-u_{fj})_b\nabla_a W_{ab}^j,0][(u_{si})_a-(u_{si})_b]V_b
  \]
  \[
  -\frac{1}{\rho_s}\sum_b[(p_f)_a+(p_f)_b]\nabla_a W_{ab}^i V_b + g_i + \frac{\gamma_a}{\rho_s}[(u_{fi})_a-(u_{si})_a]
  \]
  \[
  +\sum_b[(\tau^{*}_{sij})_a+(\tau^{*}_{sij})_b]\left[1+\frac{1}{2}\ln\frac{(\alpha_s)_b}{(\alpha_s)_a}\right]\nabla_a W_{ab}^j V_b
  -\frac{\gamma_a}{\rho_s}\frac{(\epsilon_s)_a}{(\alpha_f)_a}\sum_b\ln\frac{(\alpha_s)_b}{(\alpha_s)_a}\nabla_a W_{ab}^i V_b
  \]
- 迎风通量/对流离散（式(4.92)、(4.93)、(4.94)、(4.95)）  
  \[
  \left[-\nabla\cdot(\phi\mathbf{u}_\phi)\right]_a=-\sum_b V_b\{\max[(\mathbf{u}_\phi)_a\cdot\nabla_a W_{ab},0]\phi_a+\min[(\mathbf{u}_\phi)_b\cdot\nabla_a W_{ab},0]\phi_b\}
  \]
- 剪切应力与梯度（式(4.90)、(4.91)）  
  \[
  \left[\frac{\partial\tau^{*}_{sij}}{\partial x_j}\right]_a=\sum_b[(\tau^{*}_{sij})_a+(\tau^{*}_{sij})_b]\nabla_a W_{ab}^j V_b
  \]
  \[
  \left[\tau^{*}_{sij}\frac{\partial\ln\alpha_s}{\partial x_j}\right]_a=\sum_b\frac{[(\tau^{*}_{sij})_a+(\tau^{*}_{sij})_b]}{2}\ln\frac{(\alpha_s)_b}{(\alpha_s)_a}\nabla_a W_{ab}^j V_b
  \]
- 相间作用/扩散（式(4.96)~(4.99)）  
  \[
  \left[-\frac{\gamma\alpha_s}{\alpha_f\rho_f}(u_{fi}-u_{si})\right]_a=-\frac{\gamma_a(\alpha_s)_a}{(\alpha_f\rho_f)_a}[(u_{fi})_a-(u_{si})_a]
  \]
  \[
  \left[\frac{\gamma}{\rho_s}(u_{fi}-u_{si})\right]_a=\frac{\gamma_a}{\rho_s}[(u_{fi})_a-(u_{si})_a]
  \]
  \[
  \left[\frac{\gamma\alpha_s}{\alpha_f\rho_f}\frac{\epsilon_s}{\alpha_f}\frac{\partial\ln\alpha_s}{\partial x_i}\right]_a=\frac{\gamma_a(\alpha_s)_a}{(\alpha_f\rho_f)_a}\frac{(\epsilon_s)_a}{(\alpha_f)_a}\sum_b\ln\frac{(\alpha_s)_b}{(\alpha_s)_a}\nabla_a W_{ab}^i V_b
  \]
  \[
  \left[-\frac{\gamma}{\rho_s}\frac{\epsilon_s}{\alpha_f}\frac{\partial\ln\alpha_s}{\partial x_i}\right]_a=-\frac{\gamma_a}{\rho_s}\frac{(\epsilon_s)_a}{(\alpha_f)_a}\sum_b\ln\frac{(\alpha_s)_b}{(\alpha_s)_a}\nabla_a W_{ab}^i V_b
  \]

## 3. 时间积分与稳定性
- 预测—校正（式(4.106)~(4.115)）  
  预测：  
  \[
  X_a^{n+1/2}=X_a^n+\frac{\Delta t}{2}u_a^n,\quad
  u_a^{n+1/2}=u_a^n+\frac{\Delta t}{2}F_a^n,\quad
  \phi_a^{n+1/2}=\phi_a^n+\frac{\Delta t}{2}I_a^n
  \]
  校正（用半步力/源项改进半步解，作为全步外推基准）：  
  \[
  u_a^{n+1/2}=u_a^n+\frac{\Delta t}{2}F_a^{n+1/2},\;
  X_a^{n+1/2}=X_a^n+\frac{\Delta t}{2}u_a^{n+1/2},\;
  \phi_a^{n+1/2}=\phi_a^n+\frac{\Delta t}{2}I_a^{n+1/2}
  \]
  更新：\(X_a^{n+1}=2X_a^{n+1/2}-X_a^n\)、\(u_a^{n+1}=2u_a^{n+1/2}-u_a^n\)、\(\phi_a^{n+1}=2\phi_a^{n+1/2}-\phi_a^n\)。
- 时间步长约束（式(4.116)~(4.119)）  
  \[
  \Delta t=\min(\Delta t_c,\Delta t_F,\Delta t_\nu),\quad
  \Delta t_c=0.3\frac{h}{\max c_s},\;
  \Delta t_F=0.3\min\{\sqrt{\frac{h}{\max|a_f|}},\sqrt{\frac{h}{\max|a_s|}}\},\;
  \Delta t_\nu=0.125\min\{\frac{h^2}{\max\nu_f},\frac{h^2}{\max\nu_s}\}
  \]
- 密度滤波（Shepard 平均，式(4.120)，每 20 步执行）  
  \[
  (\rho_f)_a^{\text{filter}}=\frac{\sum_b\frac{(m_f)_b}{1-(\alpha_s)_b}W_{ab}}{\sum_b\frac{(m_f)_b}{(\alpha_f\rho_f)_b}W_{ab}}
  \]

## 4. 计算域与条件设置
- 几何：二维矩形，宽 \(L=1\,\mathrm{m}\)，水深 \(H=1\,\mathrm{m}\)。
- 初始泥沙团：面积 \(q_0\in\{5,10\}\,\mathrm{cm}^2\)，\(\alpha_{s0}=0.606\)，初速 0。
- 颗粒参数：表5.1（08C1/13C1/50C1、08C2/13C2/50C2）给定 \(d_p,\omega_s,q_0\)。
- 离散尺度：粒径 \(\Delta=0.0050\,\mathrm{m}\)（精度/成本折中）。
- 边界：侧壁与底部三层固定边界粒子；自由表面自动捕捉，无显式条件。

## 5. 模型参数与子滤波
- 亚格子应力：SPS Smagorinsky，\(C_s=0.1\)。
- 施密特数：\(S_c=1.0\) 控制泥沙标量扩散。
- 状态方程参数：\(\gamma=7\)；声速取 \(c_0=10\sqrt{gH}\) 控制弱可压性（本例 \(H=1\,\mathrm{m}\)，故 \(c_0=10\sqrt{g}\)）。
- 黏性：\(\nu_k=\nu_k^0+\nu_k^{SPS}\)；拖曳系数由 \(\gamma\) 控制，相间扩散 \(\epsilon_s\) 随浓度进入式(4.98)/(4.99)。

## 6. 求解流程小结
1. 初始化粒子位置/速度/浓度（含边界粒子）；设 \(q_0,\alpha_{s0},d_p,\omega_s,\Delta\)。
2. 计算状态方程压力 (4.105) 与黏性/应力项；构造水相/泥沙相通量、相间力与扩散。
3. 预测—校正时间推进 (4.106~4.115)，时间步长按 (4.116~4.119)。
4. 每 20 步执行 Shepard 密度平滑 (4.120) 稳定解。
5. 后处理：以 \(\alpha_s=0.1\alpha_s^m\) 定义云团边界，提取宽度 \(B\)、下沉距离 \(Z\)、无量纲速度 \(w_c/\omega_s\)，并可用 \(L_0=\sqrt{q_0}, u_0=\sqrt{gL_0}\) 做归一化。
