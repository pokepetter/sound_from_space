from ursina import *
Texture.default_filtering = 'bilinear'
app = Ursina(vsync=30)
window.color = color.black

random.seed(0)
stars = []
star_parent = Entity()
for i in range(1000):
    star = Entity(model='icosphere', position=Vec3(random.uniform(-80,80), random.uniform(-30,30), random.uniform(-10,10)), origin_z=.5, scale=.1, parent=star_parent, color=hsv(random.uniform(0,360),.3,.9), rotation=[random.uniform(0,360) for _ in range(3)])
    duplicate(star, parent=star, scale=1.1, alpha=.5)
    stars.append(star)
star_parent.combine()
# duplicate(star_parent, parent=star_parent, z=30)


bloom = Entity(model='quad', parent=camera.ui, texture='radial_gradient', scale=0)
bg = Entity(parent=camera, z=200, model='quad', scale=Vec2(16,9)*50, texture='stars', color=color.white)

camera.fov = 120
from ursina.shaders import fxaa_shader
camera.shader = fxaa_shader

# def input(key):
def skip_time(dt=1/60):
    for seq in application.sequences:
        seq.t += dt
        seq.started = True
        seq.update()
        seq.started = False

class Helper(Entity):
    def __init__(self):
        super().__init__(ignore_paused=True)

    def input(self, key):
        if key == 'right arrow' or key == 'right arrow hold':
            skip_time(1/30)
        # if key == 'left arrow' or key == 'left arrow hold':
        #     skip_time(-1/60)

        if key == 'space':
            print('start')
            camera.animate('fov', 200, duration=3, curve=curve.linear)

            star_parent.animate_z(-1, duration=2)
            star_parent.animate_scale_z(1000, duration=2, curve=curve.linear)
            star_parent.animate('rotation_z', 1000, duration=1, delay=2)
            
            bloom.animate_scale((20,6), duration=3, delay=1, curve=curve.out_expo)
            invoke(bloom.animate_scale, 1500, delay=2.5)
            bloom.animate('alpha', 1, delay=2.5)

            star_clone = duplicate(star_parent, parent=star_parent, rotation_z=90, scale_z=1)
            star_clone.animate('rotation_z', 1000, duration=1, delay=2)
            bg.fade_out(duration=.1)

            from ursina.prefabs.video_recorder import VideoRecorder
            vr = VideoRecorder(max_duration=2, fps=30, name='hyperjump')
            window.editor_ui.enabled = False
            window.fullscreen = True
            vr.start_recording()

Helper()
# application.time_scale = 0

app.run()