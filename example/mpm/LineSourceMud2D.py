from geotaichi import *


def main():
    init(dim=2, device_memory_GB=3.7)
    mpm = MPM()

    # 常量
    GRAVITY_ACCELERATION = 9.8
    h = 0.005
    water_depth = 1.0
    sound_speed_multiplier = 10  # 弱可压缩 SPH 经验：c0 = 10*sqrt(g*H)；此处 H=水深=1 m
    c0 = sound_speed_multiplier * (GRAVITY_ACCELERATION * water_depth) ** 0.5
    dt_c = 0.3 * h / c0

    rho_f = 1000.  # 流体密度 (kg/m^3)
    fluid_bulk = (c0 ** 2) * rho_f  # rho_f * c0^2
    background_water_solid_density = 1.0  # kg/m^3，刻意远小于 2650 以模拟水；保证两相质量项非零且稳定
    mud_area = 0.05  # m^2；若采用文献中更大的初始泥块可改为 0.10
    mud_region_side_length = mud_area ** 0.5

    # 1) 配置
    mpm.set_configuration(domain=[1., 1.],
                          background_damping=0.0,
                          alphaPIC=1.0,
                          mapping="USL",               # 也支持 MUSL
                          shape_function="QuadBSpline",
                          gravity=[0., -GRAVITY_ACCELERATION],
                          material_type="TwoPhaseSingleLayer",
                          velocity_projection="Affine")

    # 2) 求解器
    mpm.set_solver({"Timestep": dt_c,
                    "SimulationTime": 4.0,
                    "SaveInterval": 0.05,
                    "SavePath": "line_source_mud_output"})

    # 3) 内存分配
    mpm.memory_allocate(memory={
        "max_material_number": 2,
        "max_particle_number": 160000,  # 1 m × 1 m 区域，0.005 m 单元，水与泥各 2 粒子/单元（同域叠加）需约 16 万粒子上限
        "verlet_distance_multiplier": 1.,
        "max_constraint_number": {"max_reflection_constraint": 20000}
    })

    # 4) 材料
    mpm.add_material(model="LinearElastic", material={  # 背景“水”替代
        "MaterialID": 1,
        "YoungModulus": 1e3,          # 1e3 Pa (1 kPa)；可用 1e2~1e4 Pa 保持流动性
        "PoissonRatio": 0.495,
        "SolidDensity": background_water_solid_density,
        "FluidDensity": rho_f,
        "Porosity": 0.999,
        "FluidBulkModulus": fluid_bulk,
        "Permeability": 1e-6          # m^2；较大渗透率以模拟自由水流
    })

    mpm.add_material(model="LinearElastic", material={  # 泥云，alpha_s0 = 0.606 => 孔隙率 0.394
        "MaterialID": 2,
        "YoungModulus": 5e4,          # 增大可加硬骨架、减少泥云扩散；减小则扩散更多
        "PoissonRatio": 0.3,
        "SolidDensity": 2650.,
        "FluidDensity": rho_f,
        "Porosity": 0.394,
        "FluidBulkModulus": fluid_bulk,
        "Permeability": 1e-7          # m^2；更小渗透率增强泥-水阻力
    })

    # 5) 单元与区域
    mpm.add_element({"ElementType": "Q4N2D", "ElementSize": [h, h]})
    mpm.add_region([
        {"Name": "tank", "Type": "Rectangle2D", "BoundingBoxPoint": [0., 0.],
         "BoundingBoxSize": [1., 1.], "ydirection": [0., 1.]},
        {"Name": "mud", "Type": "Rectangle2D", "BoundingBoxPoint": [0.45, 0.7],
         "BoundingBoxSize": [mud_region_side_length, mud_region_side_length],
         "ydirection": [0., 1.]}
    ])

    # 6) 物体
    mpm.add_body({"Template": [
        {"RegionName": "tank", "nParticlesPerCell": 2, "BodyID": 0, "MaterialID": 1,
         "InitialVelocity": [0., 0.], "FixVelocity": ["Free", "Free"]},
        # 仅启用单层网格（未开启接触检测），两个物体共享 BodyID=0
        {"RegionName": "mud", "nParticlesPerCell": 2, "BodyID": 0, "MaterialID": 2,
         "InitialVelocity": [0., 0.], "FixVelocity": ["Free", "Free"]}
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
