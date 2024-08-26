from ursina import *
Texture.default_filtering = 'bilinear'
app = Ursina(vsync=30)
window.color = color.black

random.seed(0)
stars = []
star_parent = Entity()
for i in range(1000):
    star = Entity(model='icosphere', position=Vec3(random.uniform(-80,80), random.uniform(-30,30), random.uniform(-10,10)), origin_z=.5, scale=.15, parent=star_parent, color=hsv(random.uniform(0,360),.3,.9), rotation=[random.uniform(0,360) for _ in range(3)])
    stars.append(star)
star_parent.combine()
# duplicate(star_parent, parent=star_parent, z=30)


bloom = Entity(model='quad', parent=camera.ui, texture='radial_gradient', scale=0)
bg = Entity(parent=camera, z=200, model='quad', scale=Vec2(16,9)*50, texture='stars', color=color.white)

camera.fov = 120
def input(key):
    if key == 'space':
        camera.animate('fov', 200, duration=3)

        star_parent.animate_z(-1, duration=2)
        star_parent.animate_scale_z(1000, duration=2, curve=curve.linear)
        star_parent.animate('rotation_z', 1000, duration=1, delay=2)
        
        bloom.animate_scale((20,6), duration=3, delay=1, curve=curve.out_expo)
        invoke(bloom.animate_scale, 1500, delay=2.5)
        bloom.animate('alpha', 1, delay=2.5)

        star_clone = duplicate(star_parent, parent=star_parent, rotation_z=90, scale_z=1)
        star_clone.animate('rotation_z', 1000, duration=1, delay=2)
        bg.fade_out(duration=.1)


app.run()