from gl import *
from obj import *

r = Render(1024, 768)
r.light = V3(0.2, 0.6, 0.6)

#Background
t = Texture('./assests/background.bmp')
r.buffer = t.pixels
r.texture = t
r.lookAt(V3(1, 0, 100), V3(0, 0, 0), V3(0, 1, 0))
r.glFinish('out.bmp')

#item 1
t = Texture('./assests/white.bmp')
r.texture = t
r.shader = shades
r.lookAt(V3(1, 0, 5), V3(0, 0, 0), V3(0, 1, 0))
r.load('./models/planet.obj', translate=(0.3, 0.5, 0), scale=(0.2,0.3,0.3), rotate=(0, 0, 0))
r.draw_arrays('TRIANGLES')
r.glFinish('out.bmp')

#item 2
t = Texture('./assests/lobo.bmp')
r.texture = t
r.lookAt(V3(2, 0, 1), V3(0, 1, 0), V3(0, 1, 0))
r.load('./models/lobo2.obj',  translate=(0.7, 0.2, 0), scale=(0.8,0.8,0.8), rotate=(0, 1, 0))
r.draw_arrays('TRIANGLES')
r.glFinish('out.bmp')

#item 3
t = Texture('./assests/ojo.bmp')
r.texture = t
r.shader = textures
r.lookAt(V3(2, 1, 1), V3(0, 1, 0), V3(0, 1, 0))
r.load('./models/ojo.obj', translate=(0.3, 1, 0), scale=(0.08,0.08,0.08), rotate=(-0.5, 1.3, 0))
r.draw_arrays('TRIANGLES')
r.glFinish('out.bmp')

#item 4
t = Texture('./assests/white.bmp')
r.texture = t
r.shader = shades
r.lookAt(V3(-0.5, 0, 0.3), V3(0, 1, 0), V3(0, 0.5, 0))
r.load('./models/car.obj', translate=(-0.7, 1, 0), scale=(0.03,0.03,0.03), rotate=(0.3, 0, 0))
r.draw_arrays('TRIANGLES')
r.glFinish('out.bmp')

#item 5
t = Texture('./assests/luna.bmp')
r.texture = t
r.shader = textures
r.lookAt(V3(1, 1, 1), V3(-0.5, 0, -1), V3(0, 1, 0))
r.load('./models/luna.obj', translate=(0, 0, 0), scale=(0.08,0.08,0.08), rotate=(0, 0, 0))
r.draw_arrays('TRIANGLES')
r.glFinish('out.bmp')

print('****************************************************')
print('************************DONE************************')
print('****************************************************')
