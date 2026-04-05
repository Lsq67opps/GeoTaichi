from geotaichi import *


def main():
    # 初始化
    init(dim=2, arch='cpu')
    mpm = MPM()

    # === 常量配置 ===
    GRAVITY_ACCELERATION = 9.8
    h = 0.01                  # 网格尺寸
    rho_f = 1000.0            # 流体密度 (kg/m³)
    water_depth = 1.0         # 水深 1 m

    # 声速 / 体积模量
    sound_speed_multiplier = 5.0
    c0 = sound_speed_multiplier * (GRAVITY_ACCELERATION * water_depth) ** 0.5
    fluid_bulk = (c0 ** 2) * rho_f

    dt_c = 1.0e-5

    # === 泥团几何参数 ===
    mud_area    = 0.05
    mud_x_start = 0.5 - mud_area / 2.0   # 0.475
    mud_x_end   = 0.5 + mud_area / 2.0   # 0.525
    mud_y_start = water_depth - mud_area  # 0.95 (泥底 = 水面以下 5 cm)
    mud_y_end   = water_depth             # 1.00 (泥顶 = 自由液面)
    H_surface   = mud_y_end              # 自由液面高度

    # === 1) 配置：TwoPhaseSingleLayer ===
    # velocity_projection="Affine" 对 TwoPhaseSingleLayer 无效（引擎内部覆盖），
    # 不设置以避免混淆。
    mpm.set_configuration(
        domain=[1.2, 1.2],
        background_damping=0.01,    # 进一步降低阻尼，避免把微小下沉速度数值抹平
        alphaPIC=0.02,
        mapping="USF",
        shape_function="GIMP",
        gravity=[0.0, -GRAVITY_ACCELERATION],
        material_type="TwoPhaseSingleLayer"
    )

    # === 2) 求解器 ===
    mpm.set_solver({
        "Timestep": dt_c,
        "SimulationTime": 2.0,
        "SaveInterval": 0.05,
        "SavePath": "water_mud_output"
    })

    # === 3) 内存分配 ===
    mpm.memory_allocate(memory={
        "max_material_number": 2,
        "max_particle_number": 80000,
        "verlet_distance_multiplier": 1.0,
        "max_constraint_number": {
            "max_velocity_constraint": 20000,
            "max_absorbing_constraint": 20000,
            "max_particle_traction_constraint": 10000
        }
    })

    # === 4) 材料：水 + 泥（TwoPhaseSingleLayer） ===
    # 有效混合密度：rho_mix = (1-n)*rho_s + n*rho_f

    # 水体：高孔隙率 n=0.90 → rho_mix ≈ 1100 kg/m³
    mpm.add_material(model="LinearElastic", material={
        "MaterialID": 1,
        "SolidDensity": 2000.0,
        "FluidDensity": rho_f,
        "Porosity": 0.90,
        "FluidBulkModulus": fluid_bulk,
        "Permeability": 5e-2,
        "YoungModulus": 5e4,
        "PoissonRatio": 0.30,   # 修正拼写（原 PossionRatio 会被框架忽略）
    })

    # 泥团：低孔隙率 n=0.40 → rho_mix ≈ 1960 kg/m³（比水重约 860 kg/m³）
    mpm.add_material(model="LinearElastic", material={
        "MaterialID": 2,
        "SolidDensity": 2600.0,
        "FluidDensity": rho_f,
        "Porosity": 0.40,
        "FluidBulkModulus": fluid_bulk,
        "Permeability": 2e-3,
        "YoungModulus": 8e6,
        "PoissonRatio": 0.30,   # 修正拼写
    })

    # === 5) 单元 ===
    mpm.add_element({
        "ElementType": "Q4N2D",
        "ElementSize": [h, h]
    })

    # === 6) 区域定义 —— 水区与泥区严格不重叠 ===
    #
    #  y=1.00 ─────────────────────────────── (自由液面)
    #          water_left | mud | water_right   (y: 0.95–1.00)
    #  y=0.95 ───────────────────────────────
    #          water_below (全宽)               (y: 0.00–0.95)
    #  y=0.00 ───────────────────────────────
    #
    # 【关键修复】原代码水区 [0,0]→[1,1] 与泥区 [0.475,0.95]→[0.525,1.0] 完全重叠：
    #   - 同一网格节点同时接收水粒子和泥粒子的动量贡献
    #   - 水粒子数量远多于泥粒子，节点动量被水主导
    #   - 泥粒子做 G2P 时获得的是水速度，无法独立下沉
    # 修复方案：将水区拆分为三个互不重叠的矩形，与泥区共同覆盖整个液域。

    water_below = {
        "Name": "water_below",
        "Type": "Rectangle2D",
        "BoundingBoxPoint": [0.0, 0.0],
        "BoundingBoxSize": [1.0, mud_y_start],           # 全宽，泥底以下
        "ydirection": [0.0, 1.0]
    }
    water_left = {
        "Name": "water_left",
        "Type": "Rectangle2D",
        "BoundingBoxPoint": [0.0, mud_y_start],
        "BoundingBoxSize": [mud_x_start, mud_area],      # 泥团左侧，同高
        "ydirection": [0.0, 1.0]
    }
    water_right = {
        "Name": "water_right",
        "Type": "Rectangle2D",
        "BoundingBoxPoint": [mud_x_end, mud_y_start],
        "BoundingBoxSize": [1.0 - mud_x_end, mud_area],  # 泥团右侧，同高
        "ydirection": [0.0, 1.0]
    }
    mud_region = {
        "Name": "mud",
        "Type": "Rectangle2D",
        "BoundingBoxPoint": [mud_x_start, mud_y_start],
        "BoundingBoxSize": [mud_area, mud_area],
        "ydirection": [0.0, 1.0]
    }

    mpm.add_region([water_below, water_left, water_right, mud_region])

    # === 7) 初始孔压：各区域形心处的静水压力 p = rho_f * g * (H_surface - y_centroid) ===
    # 形心 y 坐标：
    #   water_below  → y_c = mud_y_start / 2 = 0.475
    #   water_left/right → y_c = mud_y_start + mud_area/2 = 0.975
    #   mud          → y_c = mud_y_start + mud_area/2 = 0.975（近液面，压力极小）
    p_water_below = rho_f * GRAVITY_ACCELERATION * (H_surface - mud_y_start / 2.0)
    p_water_sides = rho_f * GRAVITY_ACCELERATION * (H_surface - (mud_y_start + mud_area / 2.0))
    # 泥团采用单独孔压系数：略低于局部静水压，打破近似“中性平衡”初始态
    mud_pore_pressure_factor = 0.85
    p_mud = mud_pore_pressure_factor * rho_f * GRAVITY_ACCELERATION * (H_surface - (mud_y_start + mud_area / 2.0))

    # === 8) 物体：水（三段）+ 泥 ===
    mpm.add_body({
        "Template": [
            # 主水体（泥底以下）
            {
                "RegionName": "water_below",
                "nParticlesPerCell": 2,
                "BodyID": 0,
                "MaterialID": 1,
                "ParticleStress": {
                    "InternalStress": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    "PorePressure": p_water_below
                },
                # 给泥团一个很小的向下扰动速度，帮助触发下沉分支
                "InitialVelocity": [0.0, -0.03],
                "FixVelocity": ["Free", "Free"]
            },
            # 泥团左侧水体
            {
                "RegionName": "water_left",
                "nParticlesPerCell": 2,
                "BodyID": 0,
                "MaterialID": 1,
                "ParticleStress": {
                    "InternalStress": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    "PorePressure": p_water_sides
                },
                "InitialVelocity": [0.0, 0.0],
                "FixVelocity": ["Free", "Free"]
            },
            # 泥团右侧水体
            {
                "RegionName": "water_right",
                "nParticlesPerCell": 2,
                "BodyID": 0,
                "MaterialID": 1,
                "ParticleStress": {
                    "InternalStress": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    "PorePressure": p_water_sides
                },
                "InitialVelocity": [0.0, 0.0],
                "FixVelocity": ["Free", "Free"]
            },
            # 泥团（与所有水区均不重叠，可独立运动）
            {
                "RegionName": "mud",
                "nParticlesPerCell": 2,
                "BodyID": 0,
                "MaterialID": 2,
                "ParticleStress": {
                    "InternalStress": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    "PorePressure": p_mud   # 与周围水体孔压匹配，消除界面压力跳跃
                },
                "InitialVelocity": [0.0, 0.0],
                "FixVelocity": ["Free", "Free"]
            }
        ]
    })

    # === 9) 边界条件：底固定，左右竖直滑移，顶面自由 ===
    mpm.add_boundary_condition(boundary=[
        {
            "BoundaryType": "VelocityConstraint",
            "Velocity": [0.0, 0.0],
            "StartPoint": [0.0, 0.0],
            "EndPoint": [1.0, 0.0],
            "NLevel": 0
        },
        {
            "BoundaryType": "VelocityConstraint",
            "Velocity": [0.0, None],
            "StartPoint": [0.0, 0.0],
            "EndPoint": [0.0, 1.2]
        },
        {
            "BoundaryType": "VelocityConstraint",
            "Velocity": [0.0, None],
            "StartPoint": [1.0, 0.0],
            "EndPoint": [1.0, 1.2]
        }
    ])

    # === 10) 输出 ===
    mpm.select_save_data(particle=["MaterialID", "Velocity"], grid=True)

    mpm.run()
    mpm.postprocessing(read_path="water_mud_output",
                       write_background_grid=True)


if __name__ == "__main__":
    main()
