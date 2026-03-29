from geotaichi import *


def main():
    init(dim=2, device_memory_GB=3.7)
    mpm = MPM()

    # constants
    GRAVITY_ACCELERATION = 9.8
    h = 0.005
    water_depth = 1.0
    sound_speed_multiplier = 10  # weakly-compressible SPH guideline: c0 = 10*sqrt(g*H); currently H=water_depth=1 m
    c0 = sound_speed_multiplier * (GRAVITY_ACCELERATION * water_depth) ** 0.5
    dt_c = 0.3 * h / c0

    rho_f = 1000.  # fluid density (kg/m^3)
    fluid_bulk = (c0 ** 2) * rho_f  # rho_f * c0^2
    background_water_solid_density = 1.0  # kg/m^3, intentionally << 2650 to mimic water; keeps two-phase mass terms non-zero/stable
    mud_area = 0.05  # m^2; change to 0.10 if using the larger initial mud patch described in the reference
    mud_region_side_length = mud_area ** 0.5

    # 1) configuration
    mpm.set_configuration(domain=[1., 1.],
                          background_damping=0.0,
                          alphaPIC=1.0,
                          mapping="USL",               # MUSL is also supported
                          shape_function="QuadBSpline",
                          gravity=[0., -GRAVITY_ACCELERATION],
                          material_type="TwoPhaseSingleLayer",
                          velocity_projection="Affine")

    # 2) solver
    mpm.set_solver({"Timestep": dt_c,
                    "SimulationTime": 4.0,
                    "SaveInterval": 0.05,
                    "SavePath": "line_source_mud_output"})

    # 3) memory allocation
    mpm.memory_allocate(memory={
        "max_material_number": 2,
        "max_particle_number": 120000,  # 1 m x 1 m domain, 0.005 m cells, water + mud + boundary padding
        "verlet_distance_multiplier": 1.,
        "max_constraint_number": {"max_reflection_constraint": 20000}
    })

    # 4) materials
    mpm.add_material(model="LinearElastic", material={  # background water surrogate
        "MaterialID": 1,
        "Young": 1e3,                 # 1e3 Pa (1 kPa); use 1e2~1e4 Pa to keep flow-like behaviour
        "Poisson": 0.495,
        "SolidDensity": background_water_solid_density,
        "FluidDensity": rho_f,
        "Porosity": 0.999,
        "FluidBulkModulus": fluid_bulk,
        "Permeability": 1e-6          # m^2; large permeability to mimic free water flow
    })

    mpm.add_material(model="LinearElastic", material={  # mud cloud, alpha_s0 = 0.606 => porosity 0.394
        "MaterialID": 2,
        "Young": 5e4,                 # increasing stiffens skeleton, reducing cloud spread; lowering increases spread
        "Poisson": 0.3,
        "SolidDensity": 2650.,
        "FluidDensity": rho_f,
        "Porosity": 0.394,
        "FluidBulkModulus": fluid_bulk,
        "Permeability": 1e-7          # m^2; smaller permeability strengthens mud-water drag
    })

    # 5) elements and regions
    mpm.add_element({"ElementType": "Q4N2D", "ElementSize": [h, h]})
    mpm.add_region([
        {"Name": "tank", "Type": "Rectangle2D", "BoundingBoxPoint": [0., 0.],
         "BoundingBoxSize": [1., 1.], "ydirection": [0., 1.]},
        {"Name": "mud", "Type": "Rectangle2D", "BoundingBoxPoint": [0.45, 0.7],
         "BoundingBoxSize": [mud_region_side_length, mud_region_side_length],
         "ydirection": [0., 1.]}
    ])

    # 6) bodies
    mpm.add_body({"Template": [
        {"RegionName": "tank", "nParticlesPerCell": 2, "BodyID": 0, "MaterialID": 1,
         "InitialVelocity": [0., 0.], "FixVelocity": ["Free", "Free"]},
        {"RegionName": "mud", "nParticlesPerCell": 2, "BodyID": 1, "MaterialID": 2,
         "InitialVelocity": [0., 0.], "FixVelocity": ["Free", "Free"]}
    ]})

    # 7) boundaries: four reflective walls
    mpm.add_boundary_condition(boundary=[
        {"BoundaryType": "ReflectionConstraint", "Norm": [-1., 0.], "StartPoint": [0., 0.], "EndPoint": [0., 1.]},
        {"BoundaryType": "ReflectionConstraint", "Norm": [1., 0.],  "StartPoint": [1., 0.], "EndPoint": [1., 1.]},
        {"BoundaryType": "ReflectionConstraint", "Norm": [0., -1.], "StartPoint": [0., 0.], "EndPoint": [1., 0.]},
        {"BoundaryType": "ReflectionConstraint", "Norm": [0., 1.],  "StartPoint": [0., 1.], "EndPoint": [1., 1.]}
    ])

    # 8) outputs
    mpm.select_save_data(grid=True)

    # run
    mpm.run()
    mpm.postprocessing()


if __name__ == "__main__":
    main()
