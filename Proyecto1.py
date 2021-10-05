from gl import *
from obj import *

r = Render(1024, 768)
r.light = V3(0, 1, 1)

t = Texture('./texturas/background.bmp')
r.buffer = t.pixels
r.active_texture = t
r.active_shader = textures
r. glFinish('out.bmp')

print('****************************************************')
print('************************DONE************************')
print('****************************************************')
