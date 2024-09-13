from ursina import *
from ursina.prefabs.particle_system import ParticleSystem


Texture.default_filtering = 'bilinear'
app = Ursina(vsync=30)
window.color = color.black


bloom = Entity(model='quad', parent=camera.ui, texture='radial_gradient', scale=0)
bg = Entity(parent=scene, z=200, model='quad', scale=Vec2(16,9)/9*231, texture='mixolydia_centauri', color=color.white)

# camera.orthographic = True
camera.fov = 80
from ursina.shaders import camera_vertical_blur_shader
camera.shader = camera_vertical_blur_shader
camera.clip_plane_near = .01
camera.set_shader_input('blur_size', 0)
# camera.blur_size = 0

# def input(key):
def skip_time(dt=1/60):
    for seq in application.sequences:
        seq.t += dt
        seq.started = True
        seq.update()
        seq.started = False

explosion = dict(scale=4,
    # start_size=(Vec3(.05,.05,1), Vec3(.07,.07,.05)),
    start_size=Vec3(.05,.05,1),
    end_size=Vec3(.025,.025,.0),
    size_curve=curve.linear,
    speed=10,
    speed_curve=curve.out_circ,
    lifetime=6,
    auto_play=False,
    direction_randomness=Vec3(360,360,360),
    # spin=Vec3(0,15,0) * 10,
    # spin_curve=curve.linear,
    mesh='cube',
    start_color = (color.white,),
    end_color = (color.light_gray, color.magenta),
    color_curve=curve.out_expo,
    num_particles=50,
    spawn_type = 'burst',
    name='explosion', seed=0,
    # delay=4,
    enabled=False
    )
explosion_particles = ParticleSystem(**explosion)
# explosion_particles.bake()

class Helper(Entity):
    def __init__(self):
        super().__init__(ignore_paused=True, i=0)

    def input(self, key):
        if key == 'up arrow':
            base.screenshot(f'explosion_frames/_a_explosion_{str(self.i).zfill(4)}.png', False)

        if key == 'right arrow' or key == 'right arrow hold':
            skip_time(1/30)
            self.i += 1
        # if key == 'left arrow' or key == 'left arrow hold':
        #     skip_time(-1/60)

        if key == 'space':
            print('start')
           
            camera.shake(duration=5.8, magnitude=2, speed=.1)
            camera.blur_size = 0
            camera.animate('blur_size', .1, duration=4, curve=curve.in_bounce)
            invoke(Func(camera.animate, 'blur_size', 0, curve=curve.in_expo, duration=4), delay=4)
            camera.animate('z', 20, duration=3.9, curve=curve.linear)
            camera.animate('fov', 70, duration=1, delay=3.5, curve=curve.in_expo_boomerang)
            # camera.set_shader_input('blur_size', .05)
            def _():
                bloom.animate_scale((200,200), duration=.5, delay=0)
                # invoke(bloom.animate_scale, 1500, delay=2.5)
                bloom.animate('alpha', 1, duration=.5)
                invoke(Func(bloom.animate, 'alpha', 0, duration=8, curve=curve.out_expo), delay=1)
                camera.animate('z', -10, duration=.5, curve=curve.in_expo)

                invoke(explosion_particles.enable, delay=.5)
                invoke(explosion_particles.play, delay=.5)
                # explosion_particles.play()
                # explosion_particles = ParticleSystem(**explosion)

            invoke(_, delay=3.5)

            window.borderless = True
            window.size = Vec2(1920,1080)

    def update(self):
        if hasattr(camera, 'blur_size'):
            camera.set_shader_input('blur_size', camera.blur_size)

# from ursina.shaders import fxaa_shader
# camera.shader = fxaa_shader
Helper()
window.borderless = True
window.size = Vec2(1920,1080)
# application.time_scale = 0

app.run()

