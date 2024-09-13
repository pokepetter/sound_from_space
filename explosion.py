from ursina import *
from ursina.prefabs.particle_system import ParticleSystem
from ursina.shaders import unlit_shader

def random_point_in_sphere(radius=0.5):
    theta = random.uniform(0, 2 * math.pi)  # Random angle between 0 and 2*pi
    phi = random.uniform(0, math.pi)        # Random angle between 0 and pi
    r = radius * (random.uniform(0, 1) ** (1/3))  # Cube root for uniform distribution in volume
    x = r * math.sin(phi) * math.cos(theta)
    y = r * math.sin(phi) * math.sin(theta)
    z = r * math.cos(phi)
    return Vec3(x,y,z)


Texture.default_filtering = 'bilinear'
app = Ursina(vsync=30)
window.color = color.black

far_bg = Sprite(texture='stars_small', z=200, shader=unlit_shader, scale=50, texture_scale=Vec2(2))
bloom = Entity(model='quad', parent=camera.ui, texture='radial_gradient', scale=0)
bg = Entity(parent=scene, z=100, model='quad', y=0, scale=Vec2(16,9)/9*231, texture='mixolydia_centauri', color=color.white)

# camera.orthographic = True
camera.fov = 80
from ursina.shaders import camera_vertical_blur_shader
camera.shader = camera_vertical_blur_shader
camera.clip_plane_near = .01
camera.set_shader_input('blur_size', 0)

random.seed(1)
moon_parent = Entity(rotation_z=-10, position=bg.position, scale=10, enabled=False)
moon_parent.z += 50
def moon_parent_update():
    moon_parent.rotate(Vec3(0,1,-1) * time.dt)
    moon_parent.position = bg.position
    # bg.y = 20
moon_parent.update = moon_parent_update

center_star = Entity(parent=moon_parent, model='quad', world_scale=35, color=hsv(30,.2,.8), texture='yellow_star', billboard=True, always_on_top=True)
blink_animation = center_star.blink(center_star.color.tint(.2), loop=True, duration=1, curve=curve.linear_boomerang)
scale_animation = center_star.animate_scale(center_star.scale*.8, curve=curve.in_out_sine_boomerang, duration=2, loop=True)

moons = []
for i in range(200):
    moon = Entity(parent=moon_parent, model='quad', scale=random.uniform(.5,1)*.7*.2, texture='small_moon', color='#a192a2', position=random_point_in_sphere(radius=15))
    moons.append(moon)
    def moon_update(moon=moon):
        moon.look_at(camera, 'back', up=Vec3.up)
    moon.update = moon_update

    sparkle = Entity(parent=moon, model='quad', world_scale=random.uniform(.5,1)*.7*10, texture='yellow_star', position=(.25,.25,0), billboard=True)
    target_color = hsv(random.uniform(0,50), .3, 1)
    sparkle.color = target_color.tint(-.3)
    blink_animation = sparkle.blink(target_color, loop=True, duration=.5, delay=random.uniform(0,.2), curve=curve.out_expo_boomerang)
    blink_animation.loop = True
    scale_animation = sparkle.animate_scale(sparkle.scale*.5, curve=curve.out_expo_boomerang, duration=2, delay=random.random())
    scale_animation.loop = True


# EditorCamera(position=bg.position)
scene.fog_density = (250, 400)
camera.z = -100
scene.fog_color=color.black
# camera.blur_size = 0

# def input(key):
def skip_time(dt=1/60):
    for seq in application.sequences:
        seq.t += dt
        seq.started = True
        seq.update()
        seq.started = False

explosion = dict(scale=12,
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
    # num_particles=1,
    spawn_type = 'burst',
    name='explosion', seed=0,
    # delay=4,
    enabled=False
    )

t = time.perf_counter()
explosion_particles = ParticleSystem(**explosion)
print('tttttttttttt', time.perf_counter() - t)

# explosion_particles.bake()

red_star = Entity(parent=bg, z=-1, model='quad', texture='red_star', scale_y=.1*16/9, scale_x=.1, always_on_top=True)
red_star.animate_scale(red_star.scale*.8, duration=.2, curve=curve.linear_boomerang, loop=True)


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
            invoke(Func(camera.animate, 'blur_size', .05, curve=curve.in_expo, duration=4), delay=4)
            camera.animate('z', 20-100, duration=3.9, curve=curve.linear)
            camera.animate('fov', 70, duration=1, delay=3.5, curve=curve.in_expo_boomerang)
            # camera.set_shader_input('blur_size', .05)
            @after(3.5)
            def _():
                bloom.animate_scale((200,200), duration=.5, delay=0)
                # invoke(bloom.animate_scale, 1500, delay=2.5)
                bloom.animate('alpha', 1, duration=.5)
                invoke(Func(bloom.animate, 'alpha', 0, duration=8, curve=curve.out_expo), delay=1)
                camera.animate('z', -10-100, duration=.5, curve=curve.in_expo)

                @after(.5)
                def _():
                    explosion_particles.enable()
                    explosion_particles.play()
                    moon_parent.enable()
                    red_star.enabled = False
                    bg.animate('y', bg.y+2, loop=True, duration=8, curve=curve.in_out_sine_boomerang)

                # explosion_particles.play()
                # explosion_particles = ParticleSystem(**explosion)


            window.borderless = True
            window.size = Vec2(1920,1080)

    def update(self):
        if hasattr(camera, 'blur_size'):
            camera.set_shader_input('blur_size', camera.blur_size)

# from ursina.shaders import fxaa_shader
# camera.shader = fxaa_shader
Helper()
window.borderless = True
# window.monitor_index = 1
window.size = Vec2(1920,1080)
window.position = Vec2(0, 0)
# application.time_scale = 0



app.run()

