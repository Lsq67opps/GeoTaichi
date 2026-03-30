from geotaichi import *


def main():
    init(dim=2, device_memory_GB=3.7)
    mpm = MPM()

    # 常量
    GRAVITY_ACCELERATION = 9.8
    h = 0.005
    water_depth = 1.0  # 1 m 水深，与文献保持一致
    sound_speed_multiplier = 6   # 降低体积模量以减小初始水-泥压力跳变
    c0 = sound_speed_multiplier * (GRAVITY_ACCELERATION * water_depth) ** 0.5
    dt_c = 0.3 * h / c0

    rho_f = 1000.  # 流体密度 (kg/m^3)
    fluid_bulk = (c0 ** 2) * rho_f  # rho_f * c0^2
    background_water_solid_density = 1.0  # kg/m^3，刻意远小于 2650 以模拟水；保证两相质量项非零且稳定
    mud_area = 0.05  # m^2；若采用文献中更大的初始泥块可改为 0.10
    mud_region_side_length = mud_area ** 0.5

    # 1) 配置
    mpm.set_configuration(domain=[1., 1.],
                          background_damping=0.02,
                          alphaPIC=0.2,
                          mapping="USL",               # 也支持 MUSL
                          shape_function="QuadBSpline",
                          gravity=[0., -GRAVITY_ACCELERATION],
                          material_type="TwoPhaseSingleLayer",
                          velocity_projection="Affine")

    # 2) 求解器
    mpm.set_solver({"Timestep": min(dt_c, 2.0e-5),
                    "SimulationTime": 4.0,
                    "SaveInterval": 0.05,
                    "SavePath": "line_source_mud_output"})

    # 3) 内存分配
    mpm.memory_allocate(memory={
        "max_material_number": 2,
        # 1 m × 1 m 区域，0.005 m 单元，水/泥各 2 粒子/单元（同域叠加、双相）实际生成约 16.8 万粒子
        "max_particle_number": 180000,
        "verlet_distance_multiplier": 1.,
        "max_constraint_number": {"max_reflection_constraint": 20000}
    })

    # 4) 材料
    mpm.add_material(model="LinearElastic", material={  # 背景“水”替代
        "MaterialID": 1,
        "YoungModulus": 5e2,          # 更软的背景水体以减小体积应力
        "PoissonRatio": 0.495,
        "SolidDensity": background_water_solid_density,
        "FluidDensity": rho_f,
        "Porosity": 0.999,
        "FluidBulkModulus": fluid_bulk,
        "Permeability": 1e-6          # m^2；较大渗透率以模拟自由水流
    })

    mpm.add_material(model="LinearElastic", material={  # 泥云，alpha_s0 = 0.606 => 孔隙率 0.394
        "MaterialID": 2,
        "YoungModulus": 2e4,          # 稍软化骨架以降低瞬时应力峰值
        "PoissonRatio": 0.25,
        "SolidDensity": 2650.,
        "FluidDensity": rho_f,
        "Porosity": 0.394,
        "FluidBulkModulus": fluid_bulk,
        "Permeability": 1e-7          # m^2；更小渗透率增强泥-水阻力
    })

    # 5) 单元与区域
    mpm.add_element({"ElementType": "Q4N2D", "ElementSize": [h, h]})
    
    mud_x_start = 0.45
    mud_width = mud_region_side_length
    mud_x_end = mud_x_start + mud_width
    mud_y_start = 0.7
    mud_y_end = mud_y_start + mud_width

    mpm.add_region([
        # 底部水体
        {"Name": "tank_bottom", "Type": "Rectangle2D", "BoundingBoxPoint": [0., 0.],
         "BoundingBoxSize": [1., mud_y_start], "ydirection": [0., 1.]},
        # 顶部水体
        {"Name": "tank_top", "Type": "Rectangle2D", "BoundingBoxPoint": [0., mud_y_end],
         "BoundingBoxSize": [1., water_depth - mud_y_end], "ydirection": [0., 1.]},
        # 左侧水体
        {"Name": "tank_left", "Type": "Rectangle2D", "BoundingBoxPoint": [0., mud_y_start],
         "BoundingBoxSize": [mud_x_start, mud_width], "ydirection": [0., 1.]},
        # 右侧水体
        {"Name": "tank_right", "Type": "Rectangle2D", "BoundingBoxPoint": [mud_x_end, mud_y_start],
         "BoundingBoxSize": [1.0 - mud_x_end, mud_width], "ydirection": [0., 1.]},
        # 泥块
        {"Name": "mud", "Type": "Rectangle2D", "BoundingBoxPoint": [mud_x_start, mud_y_start],
         "BoundingBoxSize": [mud_width, mud_width], "ydirection": [0., 1.]}
    ])

    # 6) 物体
    # 将四个水体区域合并为背景水，全部赋给 MaterialID=1
    mpm.add_body({"Template": [
         {"RegionName": "tank_bottom", "nParticlesPerCell": 2, "BodyID": 0, "MaterialID": 1, "InitialVelocity": [0., 0.], "FixVelocity": ["Free", "Free"]},
         {"RegionName": "tank_top",    "nParticlesPerCell": 2, "BodyID": 1, "MaterialID": 1, "InitialVelocity": [0., 0.], "FixVelocity": ["Free", "Free"]},
         {"RegionName": "tank_left",   "nParticlesPerCell": 2, "BodyID": 2, "MaterialID": 1, "InitialVelocity": [0., 0.], "FixVelocity": ["Free", "Free"]},
         {"RegionName": "tank_right",  "nParticlesPerCell": 2, "BodyID": 3, "MaterialID": 1, "InitialVelocity": [0., 0.], "FixVelocity": ["Free", "Free"]},
         # 泥块，MaterialID=2
         {"RegionName": "mud",         "nParticlesPerCell": 2, "BodyID": 4, "MaterialID": 2, "InitialVelocity": [0., 0.], "FixVelocity": ["Free", "Free"]}
    ]})

    # 7) 边界：四面反射壁
    mpm.add_boundary_condition(boundary=[
        {"BoundaryType": "ReflectionConstraint", "Norm": [-1., 0.], "StartPoint": [0., 0.], "EndPoint": [0., 1.]},
        {"BoundaryType": "ReflectionConstraint", "Norm": [1., 0.],  "StartPoint": [1., 0.], "EndPoint": [1., 1.]},
        {"BoundaryType": "ReflectionConstraint", "Norm": [0., -1.], "StartPoint": [0., 0.], "EndPoint": [1., 0.]},
        {"BoundaryType": "ReflectionConstraint", "Norm": [0., 1.],  "StartPoint": [0., 1.], "EndPoint": [1., 1.]}
    ])

    # 8) 输出
    mpm.select_save_data(grid=True)

    # 运行
    mpm.run()
    mpm.postprocessing()


if __name__ == "__main__":
    main()
