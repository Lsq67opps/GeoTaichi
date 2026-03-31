from geotaichi import *


def main(mud_area=0.05):
    init(dim=2, device_memory_GB=3.7)
    mpm = MPM()

    # 常量
    GRAVITY_ACCELERATION = 9.8
    h = 0.005
    water_depth = 1.0  # 1 m 水深，与文献一致
    sound_speed_multiplier = 2.0   # 进一步降低体积模量， 减小初始水泥压差
    c0 = sound_speed_multiplier * (GRAVITY_ACCELERATION * water_depth) ** 0.5
    dt_c = 5.0e-6 

    rho_f = 1000.  # 流体密度 (kg/m^3)
    fluid_bulk = (c0 ** 2) * rho_f  # rho_f * c0^2
    background_water_solid_density = 2625.0
    # 默认泥块面积：mud_area = 5e-4 m^2（可按需调整）
    mud_area = 5e-4  # m^2
    mud_region_side_length = mud_area ** 0.5

    # 1) 配置
    mpm.set_configuration(domain=[1., 1.],
                          background_damping=5.0,     # 提高阻尼以先让静水压力收敛
                          alphaPIC=0.5,
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
        # 1 m × 1 m 计算域，单元 0.005 m，水/泥各 2 粒子/单元（双相重叠）约 16.8 万粒子
        "max_particle_number": 180000,
        "verlet_distance_multiplier": 1.,
        "max_constraint_number": {"max_reflection_constraint": 20000}
    })

    # 4) 材料
    # 若 TwoPhaseSingleLayer 需要骨架参数，用极软的莫尔-库仑近似流体
    mpm.add_material(model="MohrCoulomb", material={  # 背景“水”
        "MaterialID": 1,
        "YoungModulus": 10.0,          # 更软骨架避免伪体积模量
        "PoissonRatio": 0.0,          # 不依赖固相不可压性，体积模量由 FluidBulkModulus 提供
        "Cohesion": 0.0,              # 无粘聚力，模拟无拉强度流体
        "Friction": 0.0,
        "Dilation": 0.0,
        "SolidDensity": 2650.0,
        "FluidDensity": rho_f,
        "Porosity": 0.95,
        "FluidBulkModulus": fluid_bulk,
        "Permeability": 1e-2          # 极高渗透率，水相近乎自由流动
    })

    mpm.add_material(model="MohrCoulomb", material={  # 泥团，alpha_s0 = 0.606 => 孔隙率 0.394
        "MaterialID": 2,
        "YoungModulus": 100，0,          # 软化骨架避免脆裂，利于泥体流动
        "PoissonRatio": 0.3,
        "Cohesion": 1.0,              # 泥体黏聚力， 值越小越易扩散
        "Friction": 0.0,
        "Dilation": 0.0,
        "SolidDensity": 2650.,
        "FluidDensity": rho_f,
        "Porosity": 0.394,
        "FluidBulkModulus": fluid_bulk,
        "Permeability": 1e-7
    })

       # 5) 单元与区域
    mpm.add_element({"ElementType": "Q4N2D", "ElementSize": [h, h]})
    
    # 重新计算泥块的精确坐标，使其顶部与水面齐平 (y=1.0)
    mud_width = mud_region_side_length
    mud_x_start = 0.5 - mud_width / 2.0   # 居中对齐
    mud_x_end = mud_x_start + mud_width
    mud_y_end = water_depth               # 顶部贴紧水面 (1.0)
    mud_y_start = mud_y_end - mud_width   # 泥块底部 y 坐标

    mpm.add_region([
        # 底部水体 (充满整个水槽底部，直到泥块底部的高度)
        {"Name": "tank_bottom", "Type": "Rectangle2D", "BoundingBoxPoint": [0., 0.],
         "BoundingBoxSize": [1., mud_y_start], "ydirection": [0., 1.]},
        
        # 左侧水体 (泥块左侧的区域，高度从 mud_y_start 到水面)
        {"Name": "tank_left", "Type": "Rectangle2D", "BoundingBoxPoint": [0., mud_y_start],
         "BoundingBoxSize": [mud_x_start, mud_width], "ydirection": [0., 1.]},
        
        # 右侧水体 (泥块右侧的区域，高度从 mud_y_start 到水面)
        {"Name": "tank_right", "Type": "Rectangle2D", "BoundingBoxPoint": [mud_x_end, mud_y_start],
         "BoundingBoxSize": [1.0 - mud_x_end, mud_width], "ydirection": [0., 1.]},
         
        # 泥块 (顶部贴紧水面，居中)
        {"Name": "mud", "Type": "Rectangle2D", "BoundingBoxPoint": [mud_x_start, mud_y_start],
         "BoundingBoxSize": [mud_width, mud_width], "ydirection": [0., 1.]}
    ])

    # 6) 物体
    # 将原来的 tank_top 删掉，只保留三个水体区域和泥块
    mpm.add_body({"Template": [
         {"RegionName": "tank_bottom", "nParticlesPerCell": 2, "BodyID": 0, "MaterialID": 1, "InitialVelocity": [0., 0.], "FixVelocity": ["Free", "Free"]},
         {"RegionName": "tank_left",   "nParticlesPerCell": 2, "BodyID": 0, "MaterialID": 1, "InitialVelocity": [0., 0.], "FixVelocity": ["Free", "Free"]},
         {"RegionName": "tank_right",  "nParticlesPerCell": 2, "BodyID": 0, "MaterialID": 1, "InitialVelocity": [0., 0.], "FixVelocity": ["Free", "Free"]},
         # 泥块，MaterialID=2
         {"RegionName": "mud",         "nParticlesPerCell": 2, "BodyID": 0, "MaterialID": 2, "InitialVelocity": [0., 0.], "FixVelocity": ["Free", "Free"]}
    ]})

    # 7) 边界：四面反射墙
    mpm.add_boundary_condition(boundary=[
        {"BoundaryType": "ReflectionConstraint", "Norm": [-1., 0.], "StartPoint": [0., 0.], "EndPoint": [0., 1.]},
        {"BoundaryType": "ReflectionConstraint", "Norm": [1., 0.],  "StartPoint": [1., 0.], "EndPoint": [1., 1.]},
        {"BoundaryType": "ReflectionConstraint", "Norm": [0., -1.], "StartPoint": [0., 0.], "EndPoint": [1., 0.]},
        {"BoundaryType": "ReflectionConstraint", "Norm": [0., 1.],  "StartPoint": [0., 1.], "EndPoint": [1., 1.]}
    ])

    # 8) 输出
    mpm.select_save_data(particle=["MaterialID"], grid=True)

    # 运行
    mpm.run()
    mpm.postprocessing()


if __name__ == "__main__":
    main()
