from geotaichi import *


def main(mud_area=5e-4, enforce_08c1=True):
    init(dim=2, device_memory_GB=3.7)
    mpm = MPM()

    # Constants
    GRAVITY_ACCELERATION = 9.8
    h = 0.005
    water_depth = 1.0  # 1 m water depth, consistent with literature
    sound_speed_multiplier = 4   # Reduce bulk modulus further to lessen initial water–mud pressure jump
    c0 = sound_speed_multiplier * (GRAVITY_ACCELERATION * water_depth) ** 0.5
    dt_c = 0.3 * h / c0

    rho_f = 1000.  # Fluid density (kg/m^3)
    fluid_bulk = (c0 ** 2) * rho_f  # rho_f * c0^2
    background_water_solid_density = 1.0  # kg/m^3, deliberately << 2650 to mimic water; keeps two-phase mass terms non-zero
    # 08C1 case: q0 = 5 cm^2 (= 5e-4 m^2); enforce literature value by default
    expected_08c1_area = 5e-4  # 08C1 literature value (5 cm^2)
    if enforce_08c1 and abs(mud_area - expected_08c1_area) > 1e-9:
        raise ValueError(f"08C1 requires mud area = 5e-4 m^2 (5 cm^2); got {mud_area}")
    mud_region_side_length = mud_area ** 0.5

    # 1) Configuration
    mpm.set_configuration(domain=[1., 1.],
                          background_damping=0.2,     # Increase damping to let hydrostatic pressure settle first
                          alphaPIC=0.2,
                          mapping="USL",               # Also supports MUSL
                          shape_function="QuadBSpline",
                          gravity=[0., -GRAVITY_ACCELERATION],
                          material_type="TwoPhaseSingleLayer",
                          velocity_projection="Affine")

    # 2) Solver
    mpm.set_solver({"Timestep": min(dt_c, 2.0e-5),
                    "SimulationTime": 4.0,
                    "SaveInterval": 0.05,
                    "SavePath": "line_source_mud_output"})

    # 3) Memory allocation
    mpm.memory_allocate(memory={
        "max_material_number": 2,
        # 1 m × 1 m domain, 0.005 m cells, water/mud 2 particles/cell (overlapped two-phase) yields ~168k particles
        "max_particle_number": 180000,
        "verlet_distance_multiplier": 1.,
        "max_constraint_number": {"max_reflection_constraint": 20000}
    })

    # 4) Materials
    # If TwoPhaseSingleLayer needs skeleton parameters, use very soft Mohr-Coulomb to approximate fluid
    mpm.add_material(model="MohrCoulomb", material={  # Background “water”
        "MaterialID": 1,
        "YoungModulus": 1e2,          # Softer skeleton to avoid spurious bulk modulus
        "PoissonRatio": 0.0,          # Do not rely on solid incompressibility; FluidBulkModulus provides bulk modulus
        "Cohesion": 0.0,              # No cohesion, simulating tensile-free fluid
        "Friction": 0.0,
        "Dilation": 0.0,
        "SolidDensity": background_water_solid_density,
        "FluidDensity": rho_f,
        "Porosity": 0.999,
        "FluidBulkModulus": fluid_bulk,
        "Permeability": 1e-2          # Very high permeability; water phase flows freely
    })

    mpm.add_material(model="MohrCoulomb", material={  # Mud cloud, alpha_s0 = 0.606 => porosity 0.394
        "MaterialID": 2,
        "YoungModulus": 5e3,          # Softened skeleton avoids brittle fracture, promotes mud flow
        "PoissonRatio": 0.3,
        "Cohesion": 5.0,              # Mud cohesion; smaller values disperse more easily
        "Friction": 15.0,
        "Dilation": 0.0,
        "SolidDensity": 2650.,
        "FluidDensity": rho_f,
        "Porosity": 0.394,
        "FluidBulkModulus": fluid_bulk,
        "Permeability": 1e-7
    })

    # 5) Elements and regions
    mpm.add_element({"ElementType": "Q4N2D", "ElementSize": [h, h]})
    
    mud_x_start = 0.5 - 0.5 * mud_region_side_length  # Center the mud block horizontally
    mud_width = mud_region_side_length
    mud_x_end = mud_x_start + mud_width
    mud_y_start = 0.7
    mud_y_end = mud_y_start + mud_width

    mpm.add_region([
        # Bottom water
        {"Name": "tank_bottom", "Type": "Rectangle2D", "BoundingBoxPoint": [0., 0.],
         "BoundingBoxSize": [1., mud_y_start], "ydirection": [0., 1.]},
        # Top water
        {"Name": "tank_top", "Type": "Rectangle2D", "BoundingBoxPoint": [0., mud_y_end],
         "BoundingBoxSize": [1., water_depth - mud_y_end], "ydirection": [0., 1.]},
        # Left water
        {"Name": "tank_left", "Type": "Rectangle2D", "BoundingBoxPoint": [0., mud_y_start],
         "BoundingBoxSize": [mud_x_start, mud_width], "ydirection": [0., 1.]},
        # Right water
        {"Name": "tank_right", "Type": "Rectangle2D", "BoundingBoxPoint": [mud_x_end, mud_y_start],
         "BoundingBoxSize": [1.0 - mud_x_end, mud_width], "ydirection": [0., 1.]},
        # Mud block
        {"Name": "mud", "Type": "Rectangle2D", "BoundingBoxPoint": [mud_x_start, mud_y_start],
         "BoundingBoxSize": [mud_width, mud_width], "ydirection": [0., 1.]}
    ])

    # 6) Bodies
    # Merge four water regions into background water, all assigned MaterialID=1
    mpm.add_body({"Template": [
         # Approximate hydrostatic pore pressure to reduce shock from sudden gravity
         {"RegionName": "tank_bottom", "nParticlesPerCell": 2, "BodyID": 0, "MaterialID": 1,
          "InitialVelocity": [0., 0.], "FixVelocity": ["Free", "Free"],
          "ParticleStress": {"PorePressure": rho_f * GRAVITY_ACCELERATION * (water_depth - 0.5 * mud_y_start)}},
         {"RegionName": "tank_top",    "nParticlesPerCell": 2, "BodyID": 0, "MaterialID": 1,
          "InitialVelocity": [0., 0.], "FixVelocity": ["Free", "Free"],
          "ParticleStress": {"PorePressure": rho_f * GRAVITY_ACCELERATION * (water_depth - (mud_y_end + 0.5 * (water_depth - mud_y_end)))}},
         {"RegionName": "tank_left",   "nParticlesPerCell": 2, "BodyID": 0, "MaterialID": 1,
          "InitialVelocity": [0., 0.], "FixVelocity": ["Free", "Free"],
          "ParticleStress": {"PorePressure": rho_f * GRAVITY_ACCELERATION * (water_depth - (mud_y_start + 0.5 * mud_width))}},
         {"RegionName": "tank_right",  "nParticlesPerCell": 2, "BodyID": 0, "MaterialID": 1,
          "InitialVelocity": [0., 0.], "FixVelocity": ["Free", "Free"],
          "ParticleStress": {"PorePressure": rho_f * GRAVITY_ACCELERATION * (water_depth - (mud_y_start + 0.5 * mud_width))}},
         # Mud block, MaterialID=2
         {"RegionName": "mud",         "nParticlesPerCell": 2, "BodyID": 0, "MaterialID": 2, "InitialVelocity": [0., 0.], "FixVelocity": ["Free", "Free"]}
    ]})

    # 7) Boundaries: four reflection walls
    mpm.add_boundary_condition(boundary=[
        {"BoundaryType": "ReflectionConstraint", "Norm": [-1., 0.], "StartPoint": [0., 0.], "EndPoint": [0., 1.]},
        {"BoundaryType": "ReflectionConstraint", "Norm": [1., 0.],  "StartPoint": [1., 0.], "EndPoint": [1., 1.]},
        {"BoundaryType": "ReflectionConstraint", "Norm": [0., -1.], "StartPoint": [0., 0.], "EndPoint": [1., 0.]},
        {"BoundaryType": "ReflectionConstraint", "Norm": [0., 1.],  "StartPoint": [0., 1.], "EndPoint": [1., 1.]}
    ])

    # 8) Output
    mpm.select_save_data(grid=True)

    # Run
    mpm.run()
    mpm.postprocessing()


if __name__ == "__main__":
    main()
