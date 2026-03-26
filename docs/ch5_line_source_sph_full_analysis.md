# 第5章二维线源瞬时抛泥 SPH 问题全流程公式整理

对“静水中二维线源瞬时抛泥”算例，汇总建模、离散、条件设定与求解全过程涉及的控制方程与计算公式，便于实现或复现。

## 1. 连续介质控制方程（双流体）
对相 \(k=f,s\)（水/泥沙），体积分数 \(\alpha_k\) 满足 \(\alpha_f+\alpha_s=1\)，保证局部填充度守恒。

- 质量守恒  
  \[
  \frac{\partial(\alpha_k\rho_k)}{\partial t}+\nabla\cdot(\alpha_k\rho_k\mathbf{u}_k)=0
  \]
  **解析：**  
  - \(\partial(\alpha_k\rho_k)/\partial t\) 描述相 \(k\) 局部质量变化率；\(\nabla\cdot(\alpha_k\rho_k\mathbf{u}_k)\) 为对流输运。  
  - 该式确保水相、泥沙相各自质量守恒，且依赖于体积分数 \(\alpha_k\)（可压缩视角下的有效密度）。  
  - \(\alpha_f+\alpha_s=1\) 约束意味着任一点两相填充之和为 1，避免空洞或重叠。

- 动量守恒  
  \[
  \frac{\partial(\alpha_k\rho_k\mathbf{u}_k)}{\partial t}
  +\nabla\cdot(\alpha_k\rho_k\mathbf{u}_k\mathbf{u}_k)
  =-\alpha_k\nabla p+\nabla\cdot(\alpha_k\boldsymbol{\tau}_k)+\alpha_k\rho_k\mathbf{g}+\mathbf{F}_{Ak}
  \]
  **解析：**  
  - 左侧为相 \(k\) 动量瞬变项与对流输运项。  
  - 右侧从左到右依次为：共有压力梯度（假设泥沙无独立分压，压力由液相承载）、黏性/雷诺应力 \(\boldsymbol{\tau}_k\)、重力项、相间作用力 \(\mathbf{F}_{Ak}\)。  
  - 相间力满足作用-反作用：\(\mathbf{F}_{Af}=-\mathbf{F}_{As}=\gamma(\mathbf{u}_s-\mathbf{u}_f)+\) 扩散项，表征拖曳与亚网格扩散耦合。

- 状态方程（弱可压 Tait，见《论文翻译.md》式(4.105)，\(\gamma=7\)，\(c_0=10\sqrt{gH}\) 控制密度涨落 \(\lesssim1\%\)）  
  \[
  (p_f)_a=\frac{\rho_{f0}c_0^{2}}{\gamma}\left(\left[\frac{(\alpha_f\rho_f)_a+(\alpha_s)_a\rho_{f0}}{(\alpha_f\rho_f)_a}\right]^{\gamma}-1\right)
  \]
  **解析：**  
  - 采用弱可压 SPH：压力由基准密度 \(\rho_{f0}\)、人工声速 \(c_0\) 和指数 \(\gamma\) 控制，允许小幅密度压缩。  
  - 括号内比值体现可压性对混合体积浓度的依赖；\((\alpha_s)_a\rho_{f0}\) 近似固相对压力贡献。  
  - \(c_0=10\sqrt{gH}\) 经验选取以保持马赫数低、抑制数值噪声；\(\gamma=7\) 常用于水体。  
  - 弱可压假设避免求解泊松方程，提高效率，但需较小时间步以满足声速 CFL。 

## 2. SPH 离散公式（单组粒子）
- 轨迹与携量（式(4.100)）  
  \[
  \frac{dX_{ai}}{dt}=(u_{fi})_a
  \]
  **解析：** 粒子路径由水相速度推进；单组粒子框架下粒子代表混合体，但运动速度取水相速度以保证自由面捕捉与流体一致性。

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
  **解析：**  
  - 第一项压力梯度采用对称形式避免张力不稳定；\(V_b\) 为粒子体积，\(\nabla W\) 提供平滑梯度。  
  - 第二项为黏性/湍黏应力扩散，含亚格子黏度，按 \((\alpha_f\rho_f)\) 加权确保动量守恒。  
  - 第三项为拖曳阻力，\(\gamma_a\) 取决于局部浓度/粒径，强制两相速度接近。  
  - 第四项为亚尺度浓度梯度驱动的扩散项，避免浓度尖峰导致的数值噪声。

- 水相连续（式(4.102)）  
  \[
  \frac{d(\alpha_f\rho_f)_a}{dt}=(\alpha_f\rho_f)_a\sum_b[(u_{fj})_a-(u_{fj})_b]\nabla_a W_{ab}^j V_b
  \]
  **解析：** 通过速度差的散度更新有效密度；对称差分保证局部守恒，且与动量式耦合以保持低马赫下的物质守恒。

- 泥沙体积分数（式(4.103)）  
  \[
  \frac{d(\alpha_s)_a}{dt}=(\alpha_s)_a\sum_b[(u_{fj})_a-(u_{fj})_b]\nabla_a W_{ab}^j V_b -
  \]
  \[
  \sum_b V_b\{\max[(u_{sj}-u_{fj})_a\nabla_a W_{ab}^j,0](\alpha_s)_a+
  \min[(u_{sj}-u_{fj})_b\nabla_a W_{ab}^j,0](\alpha_s)_b\}
  \]
  **解析：**  
  - 第一行为随水相速度的输运（体积分数受水相对流）。  
  - 第二行迎风离散泥沙相对水相的滑移通量，max/min 分段保证沿流向上风、守恒且抑制数值振荡。  
  - 通量形式来自改写 Donor–Acceptor，适应粒子邻域非结构特性。

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
  **解析：**  
  - 首项为滑移对流的迎风扩散，限制泥沙速度梯度导致的振荡。  
  - 压力梯度项用水相压力驱动泥沙（假设孔隙水压力传递给颗粒骨架）。  
  - 重力与拖曳项体现颗粒下沉和与水相耦合。  
  - 剪切应力项含 \(\ln(\alpha_s)\) 权，反映颗粒浓度对有效黏度的影响；扩散项抑制浓度尖峰导致的数值不稳定。

- 迎风通量/对流离散（式(4.92)、(4.93)、(4.94)、(4.95)）  
  \[
  \left[-\nabla\cdot(\phi\mathbf{u}_\phi)\right]_a=-\sum_b V_b\{\max[(\mathbf{u}_\phi)_a\cdot\nabla_a W_{ab},0]\phi_a+\min[(\mathbf{u}_\phi)_b\cdot\nabla_a W_{ab},0]\phi_b\}
  \]
  **解析：** 通用迎风模板，\(\phi\) 可为 \(\alpha_s\) 或 \(u_s\) 分量；通过邻域速度投影决定上风粒子，保证通量守恒与数值耗散方向正确。

- 剪切应力与梯度（式(4.90)、(4.91)）  
  \[
  \left[\frac{\partial\tau^{*}_{sij}}{\partial x_j}\right]_a=\sum_b[(\tau^{*}_{sij})_a+(\tau^{*}_{sij})_b]\nabla_a W_{ab}^j V_b
  \]
  \[
  \left[\tau^{*}_{sij}\frac{\partial\ln\alpha_s}{\partial x_j}\right]_a=\sum_b\frac{[(\tau^{*}_{sij})_a+(\tau^{*}_{sij})_b]}{2}\ln\frac{(\alpha_s)_b}{(\alpha_s)_a}\nabla_a W_{ab}^j V_b
  \]
  **解析：**  
  - 对称形式保证剪切力在粒子对之间守恒。  
  - \(\ln(\alpha_s)\) 梯度项捕捉浓度对应力的非线性影响，避免在稀疏/高浓度区出现非物理振荡。

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
  **解析：**  
  - 前两式为动量交换（拖曳）在水相、泥沙方程的对偶体现，数值上保证作用-反作用。  
  - 后两式为相间扩散，\(\epsilon_s\) 代表涡粘/相间扩散系数，使用对数浓度差减少负浓度风险。  
  - 这些项控制相间动量与浓度耦合强度，是双流体模型与单相 SPH 的关键差异。

## 3. 时间积分与稳定性
- 预测—校正（式(4.106)~(4.115)）  
  预测：  
  \[
  X_a^{n+1/2}=X_a^n+\frac{\Delta t}{2}u_a^n,\quad
  u_a^{n+1/2}=u_a^n+\frac{\Delta t}{2}F_a^n,\quad
  \phi_a^{n+1/2}=\phi_a^n+\frac{\Delta t}{2}I_a^n
  \]
  校正（用 \(n+1/2\) 时刻力/源重新评估半步量，再用于全步外推）：  
  \[
  u_a^{n+1/2}=u_a^n+\frac{\Delta t}{2}F_a^{n+1/2},\;
  X_a^{n+1/2}=X_a^n+\frac{\Delta t}{2}u_a^{n+1/2},\;
  \phi_a^{n+1/2}=\phi_a^n+\frac{\Delta t}{2}I_a^{n+1/2}
  \]
  更新：\(X_a^{n+1}=2X_a^{n+1/2}-X_a^n\)、\(u_a^{n+1}=2u_a^{n+1/2}-u_a^n\)、\(\phi_a^{n+1}=2\phi_a^{n+1/2}-\phi_a^n\)。  
  **解析：**  
  - 预测步用已知 \(F_a^n,I_a^n\) 快速估计半步量，便于构造半步相间力与压力。  
  - 校正步用半步力重新评估，降低时间离散误差（显式二阶）。  
  - 最终外推等价于二阶 Adams-Bashforth，但在半步更新中消除了对称性误差，适合弱可压 SPH。

- 时间步长约束（式(4.116)~(4.119)）  
  \[
  \Delta t=\min(\Delta t_c,\Delta t_F,\Delta t_\nu),\quad
  \Delta t_c=0.3\frac{h}{\max c_s},\;
  \Delta t_F=0.3\min\{\sqrt{\frac{h}{\max|a_f|}},\sqrt{\frac{h}{\max|a_s|}}\},\;
  \Delta t_\nu=0.125\min\{\frac{h^2}{\max\nu_f},\frac{h^2}{\max\nu_s}\}
  \]
  **解析：**  
  - \(\Delta t_c\) 为声速 CFL 约束，弱可压 SPH 的主导限制；\(h\) 为光滑长度。  
  - \(\Delta t_F\) 由加速度幅值限制，避免粒子跨越过多核半径导致穿越。  
  - \(\Delta t_\nu\) 控制黏性扩散稳定性，尤其在高 \(\nu_s\) 或高浓度泥沙区重要。  
  - 取最小值保证所有机制稳定，系数 0.3/0.125 为经验安全裕度。

- 密度滤波（Shepard 平均，式(4.120)，每 20 步执行）  
  \[
  (\rho_f)_a^{\text{filter}}=\frac{\sum_b\frac{(m_f)_b}{1-(\alpha_s)_b}W_{ab}}{\sum_b\frac{(m_f)_b}{(\alpha_f\rho_f)_b}W_{ab}}
  \]
  **解析：**  
  - Shepard 平均对水相密度做局部加权平滑，减少弱可压下的压力噪声。  
  - 分子使用质量，分母使用有效密度，保持质量守恒；每 20 步一次平衡平滑强度与物理保真。  
  - 仅作用于密度，不改变粒子质量与体积分数，避免破坏守恒。

## 4. 计算域与条件设置
- 几何：二维矩形，宽 \(L=1\,\mathrm{m}\)，水深 \(H=1\,\mathrm{m}\)。  
  **解析：** 与 Nakatsuji (1990) 实验一致，便于对比；2D 假定线源在出平面方向单位厚度。
- 初始泥沙团：面积 \(q_0\in\{5,10\}\,\mathrm{cm}^2\)，\(\alpha_{s0}=0.606\)，初速 0。  
  **解析：** 以面积代表体积（2D），浓度 0.606 对应初始堆积，零初速强调下落主要由重力触发。
- 颗粒参数：表5.1（08C1/13C1/50C1、08C2/13C2/50C2）给定 \(d_p,\omega_s,q_0\)。  
  **解析：** 通过粒径与沉速组合考察粒径/初始体积对云团形态与速度的影响。
- 离散尺度：粒径 \(\Delta=0.0050\,\mathrm{m}\)（精度/成本折中）。  
  **解析：** 对比 0.0100/0.0050/0.0025 m 的敏感性试验表明 0.005 m 与 0.0025 m 结果接近，计算成本可接受。
- 边界：侧壁与底部三层固定边界粒子；自由表面自动捕捉，无显式条件。  
  **解析：** 固壁用静止粒子施加反力，3 层保证核支持充足；自由面依赖粒子分布自然出现，避免专门的自由面处理。

## 5. 模型参数与子滤波
- 亚格子应力：SPS（Sub-Particle Scale，亚粒子尺度）Smagorinsky，\(C_s=0.1\)。  
  **解析：** 取值位于常用 \(0.075\sim0.125\) 之间，平衡湍动耗散与分辨率，避免过度平滑导致云团扩散过快。
- 施密特数：\(S_c=1.0\) 控制泥沙标量扩散。  
  **解析：** \(S_c=\nu_t/\kappa_t\)，设为 1 使泥沙标量扩散与湍黏相当；对下沉速度影响小但影响云团宽度后期扩展。
- 状态方程参数：\(\gamma=7\)；声速取 \(c_0=10\sqrt{gH}\) 控制弱可压性（本例 \(H=1\,\mathrm{m}\)，故 \(c_0=10\sqrt{g}\)）。  
  **解析：** 保证密度波动 <1%，同时限制声速过大导致时间步过小。
- 黏性：\(\nu_k=\nu_k^0+\nu_k^{SPS}\)；拖曳系数由 \(\gamma\) 控制，相间扩散 \(\epsilon_s\) 随浓度进入式(4.98)/(4.99)。  
  **解析：** 物理黏度 \(\nu_k^0\) 负责分子耗散，\(\nu_k^{SPS}\) 处理未分辨湍动；\(\gamma,\epsilon_s\) 与浓度/粒径相关，是两相耦合强度的调节阀。

## 6. 求解流程小结
符号说明：\(\alpha_s^m\) 表示任一时刻云团内的最大泥沙体积分数。  
1. 初始化粒子位置/速度/浓度（含边界粒子）；设 \(q_0,\alpha_{s0},d_p,\omega_s,\Delta\)。  
   **解析：** 生成均匀水体与泥沙团分布，保证初始核支持完整；边界粒子三层放置，避免粒子稀缺导致渗漏。
2. 计算状态方程压力 (4.105) 与黏性/应力项；构造水相/泥沙相通量、相间力与扩散。  
   **解析：** 先用当前 \(\alpha_f\rho_f,\alpha_s\) 评估 \(p_f\)，再依次装配动量和体积分数方程右端项，确保压力—速度耦合同步。
3. 预测—校正时间推进 (4.106~4.115)，时间步长按 (4.116~4.119)。  
   **解析：** 显式二阶推进，时间步由声速/加速度/黏性最小值限制；半步重评力避免高浓度区非物理加速。
4. 每 20 步执行 Shepard 密度平滑 (4.120) 稳定解。  
   **解析：** 平滑仅作用密度字段，抑制压力噪声而不破坏质量；频率可视密度波动调节。
5. 后处理：以 \(\alpha_s=0.1\alpha_s^m\) 定义云团边界，提取宽度 \(B\)、下沉距离 \(Z\)、无量纲速度 \(w_c/\omega_s\)，并可用 \(L_0=\sqrt{q_0}, u_0=\sqrt{gL_0}\) 做归一化。  
   **解析：** 阈值依据实验可得浓度测量方式；无量纲化便于跨粒径/初始体积对比。
