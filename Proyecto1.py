from gl import *
from obj import *

r = Render(1024, 768)
r.light = V3(0, 1, 1)

t = Texture('./assets/texturas/background.bmp')
r.buffer = t.pixels
r.active_texture = t
r.active_shader = textures

t = Texture('./assets/texturas/color.bmp')
r.active_texture = t
r.lookAt(V3(1, 0, 5), V3(0, 0, 0), V3(0, 1, 0))
r.load('./assets/modelos/gas.obj', translate=(-0.2, -0.5, 0.3),
       scale=(0.1, 0.1, 0.1), rotate=(0.5, 0.5, 0))
r.draw_arrays('TRIANGLES')

t = Texture('./assets/texturas/nave.bmp')
r.active_texture = t
r.lookAt(V3(1, 0, 5), V3(0, 1, 3), V3(0, 1, 0))
r.load('./assets/modelos/nave.obj', translate=(-0.2, -0.5, 0.3),
       scale=(1, 1, 1), rotate=(0.1, 0.2, 0.1))
r.draw_arrays('TRIANGLES')

t = Texture('./assets/texturas/color.bmp')
r.active_texture = t
r.lookAt(V3(0, 1, 0), V3(1, 0, 1), V3(0, 1, 1))
r.load('./assets/modelos/girl.obj', translate=(-0.2, -0.5, 0.3),
       scale=(0.1, 0.1, 0.1), rotate=(0, 0, 0))
r.draw_arrays('TRIANGLES')

r. glFinish('out.bmp')

print('****************************************************')
print('************************DONE************************')
print('****************************************************')
