import omni.replicator.core as rep # type: ignore

# Create a new USD layer to build on
with rep.new_layer():
    CRATE = "omniverse://localhost/NVIDIA/Samples/Marbles/assets/standalone/SM_room_crate_3/SM_room_crate_3.usd"

    # Add Default Light
    distance_light = rep.create.light(rotation=(315,0,0), intensity=3000, light_type="distant")

    # Create and register a randomizer function for sphere lights
    def sphere_lights(num):
        lights = rep.create.light(
            light_type="Sphere",
            temperature=rep.distribution.normal(6500, 500),
            intensity=rep.distribution.normal(35000, 5000),
            position=rep.distribution.uniform((-10, -10, 5), (10, 10, 10)),
            scale=rep.distribution.uniform(50, 100),
            count=num
        )
        return lights.node
    rep.randomizer.register(sphere_lights)

    # Create and register a prop randomizer function
    def get_props(size):
        instances = rep.randomizer.instantiate(rep.utils.get_usd_files(CRATE, recursive=True), size=size, mode='point_instance')
        with instances:
            rep.modify.pose(
                position=(0, 0, 20),
                # position=rep.distribution.uniform((-500, 0, -500), (500, 0, 500)),
                rotation=rep.distribution.uniform((-90, -90, 0), (90, -90, 0)),
            )
        return instances.node
    rep.randomizer.register(get_props)

    # Create a camera and render product, what creates the image
    camera = rep.create.camera(
        # Dont define these if we want to move the camera
        # position=(50, 0, 2), 
        # rotation=(0, 0, 0)
    )
    render_product = rep.create.render_product(camera, (1024, 1024))

    # torus = rep.create.torus(semantics=[('class', 'torus')] , position=(0, 0 , 0))
    # sphere = rep.create.sphere(semantics=[('class', 'sphere')], position=(0, 0, 0))
    # cube = rep.create.cube(semantics=[('class', 'cube')],  position=(0, 0, 0) )
    plane = rep.create.plane(scale=10, visible=True)

    with rep.trigger.on_frame(max_execs=500):
        # with rep.create.group([torus, sphere, cube]):
        #     rep.modify.pose(
        #         position=rep.distribution.uniform((-5, -5, 2), (5, 5, 2)),
        #         scale=rep.distribution.uniform(0.1, 2)
        #     )
        rep.randomizer.sphere_lights(10)
        with camera:
            rep.modify.pose(
                position=rep.distribution.uniform((200, -10, 2), (300, 10, 50)),
                look_at=rep.distribution.uniform((-5, -5, -5), (5, 5, 5))
            )
        rep.randomizer.get_props(1)

    # Initialize and attach writer
    writer = rep.WriterRegistry.get("BasicWriter")
    writer.initialize(output_dir="crate_500_output", rgb=True, bounding_box_2d_tight=True)
    writer.attach([render_product])
    rep.orchestrator.preview()