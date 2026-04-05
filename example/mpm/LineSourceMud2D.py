from geotaichi import *


def main():
    # 初始化
    init(dim=2, arch='cpu')
    mpm = MPM()

    # === 常量配置 ===
    GRAVITY_ACCELERATION = 9.8
    h = 0.01                  # 网格尺寸
    water_depth = 1.0         # 水深 1 m

    # 声速 / 体积模量（与你之前稳定的水体设置保持同一量级）
    sound_speed_multiplier = 5.0
    c0 = sound_speed_multiplier * (GRAVITY_ACCELERATION * water_depth) ** 0.5

    rho_f = 1000.0
    fluid_bulk = (c0 ** 2) * rho_f

    dt_c = 1.0e-5

    # === 1) 配置：TwoPhaseSingleLayer ===
    mpm.set_configuration(
        domain=[1.2, 1.2],          # 上下左右各留 0.1 m 缓冲
        background_damping=0.2,     # 适中且略偏小的阻尼
        alphaPIC=0.02,              # 较小数值耗散，让小块泥能动起来
        mapping="USF",
        shape_function="GIMP",
        gravity=[0.0, -GRAVITY_ACCELERATION],
        material_type="TwoPhaseSingleLayer",
        velocity_projection="Affine"
    )

    # === 2) 求解器 ===
    mpm.set_solver({
        "Timestep": dt_c,
        "SimulationTime": 1.0,      # 拉长到 1.0 s，便于观察下沉
        "SaveInterval": 0.05,
        "SavePath": "water_mud_output"
    })

    # === 3) 内存分配 ===
    mpm.memory_allocate(memory={
        "max_material_number": 2,     # 水 + 泥
        "max_particle_number": 80000,
        "verlet_distance_multiplier": 1.0,
        "max_constraint_number": {
            "max_velocity_constraint": 20000,
            "max_absorbing_constraint": 20000,
            "max_particle_traction_constraint": 10000
        }
    })

    # === 4) 材料：水 + 泥（TwoPhaseSingleLayer） ===
    # 有效密度大致：rho_eff ≈ (1-n)*SolidDensity + n*FluidDensity

    # 水体：高孔隙、较轻骨架 → 有效密度接近 ρ_f
    mpm.add_material(model="LinearElastic", material={
        "MaterialID": 1,
        "SolidDensity": 2000.0,       # 骨架相对较轻
        "FluidDensity": rho_f,
        "Porosity": 0.90,             # 高孔隙率 → rho_eff^w ≈ 1100 kg/m^3
        "FluidBulkModulus": fluid_bulk,
        "Permeability": 1e-3,
        "YoungModulus": 5e6,
        "PossionRatio": 0.30,
    })

    # 泥团：致密且重 → 有效密度远大于水体
    mpm.add_material(model="LinearElastic", material={
        "MaterialID": 2,
        "SolidDensity": 2600.0,       # 较重骨架
        "FluidDensity": rho_f,
        "Porosity": 0.40,             # 孔隙率显著更低 → rho_eff^m ≈ 1960 kg/m^3
        "FluidBulkModulus": fluid_bulk,
        "Permeability": 5e-4,
        "YoungModulus": 8e6,          # 稍硬，保持一定形状
        "PossionRatio": 0.30,
    })

    # === 5) 单元 ===
    mpm.add_element({
        "ElementType": "Q4N2D",
        "ElementSize": [h, h]
    })

    # === 6) 区域：水体 + 泥团 ===
    water_region = {
        "Name": "tank_all",
        "Type": "Rectangle2D",
        "BoundingBoxPoint": [0.0, 0.0],
        "BoundingBoxSize": [1.0, water_depth],
        "ydirection": [0.0, 1.0]
    }

    mud_size = 0.04
    mud_x_start = 0.5 - mud_size / 2.0
    mud_y_end = water_depth
    mud_y_start = mud_y_end - mud_size
    mud_region = {
        "Name": "mud",
        "Type": "Rectangle2D",
        "BoundingBoxPoint": [mud_x_start, mud_y_start],
        "BoundingBoxSize": [mud_size, mud_size],
        "ydirection": [0.0, 1.0]
    }

    mpm.add_region([water_region, mud_region])

    # === 7) 物体：水 + 泥 ===
    mpm.add_body({
        "Template": [
            {
                "RegionName": "tank_all",
                "nParticlesPerCell": 2,
                "BodyID": 0,
                "MaterialID": 1,
                "ParticleStress": {
                    "GravityField": False,
                    "InternalStress": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    "PorePressure": 1.0e4   # 近似静水孔压
                },
                "InitialVelocity": [0.0, 0.0],
                "FixVelocity": ["Free", "Free"]
            },
            {
                "RegionName": "mud",
                "nParticlesPerCell": 2,
                "BodyID": 0,
                "MaterialID": 2,
                # 如需数值“助推”，可把下一行改为 [0.0, -0.05] 试试
                "InitialVelocity": [0.0, -0.05],
                "FixVelocity": ["Free", "Free"]
            }
        ]
    })

    # === 8) 边界条件：底固定，左右竖直滑移，上自由 ===
    mpm.add_boundary_condition(boundary=[
        # 底部完全固定
        {
            "BoundaryType": "VelocityConstraint",
            "Velocity": [0.0, 0.0],
            "StartPoint": [0.0, 0.0],
            "EndPoint": [1.0, 0.0],
            "NLevel": 0
        },
        # 左右侧仅约束水平位移
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
        # 顶面自由
    ])

    # === 9) 输出 ===
    mpm.select_save_data(particle=["MaterialID", "Velocity"], grid=True)

    # 运行与后处理
    mpm.run()
    mpm.postprocessing(read_path="water_mud_output",
                       write_background_grid=True)


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
