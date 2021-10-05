from obj import Obj
from collections import namedtuple
import math
import struct
import numpy

# Funciones Matematicas y Utilidades
class V3(object):
    def __init__(self, x, y=None, z=None):
        if (type(x) == numpy.matrix):
            self.x, self.y, self.z = x.tolist()[0]
        else:
            self.x = x
            self.y = y
            self.z = z

    def __repr__(self):
        return "V3(%s, %s, %s)" % (self.x, self.y, self.z)


class V2(object):
    def __init__(self, x, y=None):
        if (type(x) == numpy.matrix):
            self.x, self.y = x.tolist()[0]
        else:
            self.x = x
            self.y = y

    def __repr__(self):
        return "V2(%s, %s)" % (self.x, self.y)


def char(c):
    return struct.pack('=c', c.encode('ascii'))


def word(w):
    return struct.pack('=h', w)


def dword(d):
    return struct.pack('=l', d)


def color(r, g, b):
    return bytes([b, g, r])


def sum(v0, v1):
    return V3(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)


def sub(v0, v1):
    return V3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)


def mul(v0, k):
    return V3(v0.x * k, v0.y * k, v0.z * k)


def dot(v0, v1):
    return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

def length(v0):
    return (v0.x**2 + v0.y**2 + v0.z**2)**0.5


def norm(v0):
    v0length = length(v0)

    if not v0length:
        return V3(0, 0, 0)

    return V3(v0.x/v0length, v0.y/v0length, v0.z/v0length)

def cross(v1, v2):
    return V3(
        v1.y * v2.z - v1.z * v2.y,
        v1.z * v2.x - v1.x * v2.z,
        v1.x * v2.y - v1.y * v2.x,
    )

def barycentric(A, B, C, P):
    bc = cross(
        V3(B.x - A.x, C.x - A.x, A.x - P.x),
        V3(B.y - A.y, C.y - A.y, A.y - P.y)
    )

    if abs(bc.z) < 1:
        return -1, -1, -1

    u = bc.x/bc.z
    v = bc.y/bc.z
    w = 1 - (bc.x + bc.y)/bc.z

    return w, v, u

def bbox(*vertices):
    xs = [vertex.x for vertex in vertices]
    ys = [vertex.y for vertex in vertices]

    return (max(xs), max(ys), min(xs), min(ys))

def MultMatriz(a, b):
    c = []
    for i in range(0, len(a)):
        temp = []
        for j in range(0, len(b[0])):
            s = 0
            for k in range(0, len(a[0])):
                s += a[i][k]*b[k][j]
            temp.append(s)
        c.append(temp)
    return c

BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)
#############################################################################
# Shaders y Utilidades

def textures(render, **kwargs):
    w, v, u = kwargs['bar']
    tx, ty = kwargs['texture_coords']
    tcolor = render.active_texture.get_color(tx, ty)
    nA, nB, nC = kwargs['varying_normals']

    iA, iB, iC = [dot(n, render.light) for n in (nA, nB, nC)]
    intensity = w*iA + u*iB + v*iC
    r, g, b = tcolor[2] * intensity, tcolor[1] * \
         intensity, tcolor[0] * intensity
    if r < 0:
        r = 0
    if r > 256:
        r = 255
    if b < 0:
        b = 0
    if b > 256:
        b = 255
    if g < 0:
        g = 0
    if g > 256:
        g = 255

    return color(int(r), int(g), int(b))

#############################################################################

class Render(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.glClear()
        self.active_texture = None
        self.active_shader = None
        self.active_vertex_array = []

    def glClear(self):
        self.buffer = [
            [WHITE for x in range(self.width)]
            for y in range(self.height)
        ]
        self.zbuffer = [
            [-float('inf') for x in range(self.width)]
            for y in range(self.height)
        ]

    def point(self, x, y):
        try:
            self.buffer[y][x] = self.current_color
        except:
            pass

    def triangle(self):
        A = next(self.active_vertex_array)
        B = next(self.active_vertex_array)
        C = next(self.active_vertex_array)

        if self.active_texture:
            tA = next(self.active_vertex_array)
            tB = next(self.active_vertex_array)
            tC = next(self.active_vertex_array)

            nA = next(self.active_vertex_array)
            nB = next(self.active_vertex_array)
            nC = next(self.active_vertex_array)

        xmax, ymax, xmin, ymin = bbox(A, B, C)

        normal = norm(cross(sub(B, A), sub(C, A)))
        intensity = dot(normal, self.light)
        if intensity < 0:
            return

        for x in range(round(xmin), round(xmax) + 1):
            for y in range(round(ymin), round(ymax) + 1):
                P = V2(x, y)
                w, v, u = barycentric(A, B, C, P)
                if w < 0 or v < 0 or u < 0:
                    continue

                if self.active_texture:
                    tx = tA.x * w + tB.x * u + tC.x * v
                    ty = tA.y * w + tB.y * u + tC.y * v

                    self.current_color = self.active_shader(
                        self,
                        triangle=(A, B, C),
                        bar=(w, v, u),
                        texture_coords=(tx, ty),
                        varying_normals=(nA, nB, nC)
                    )
                else:
                    self.current_color = color(round(255 * intensity), 0, 0)

                z = A.z * w + B.z * u + C.z * v
                if x < 0 or y < 0:
                    continue

                if x < len(self.zbuffer) and y < len(self.zbuffer[x]) and z > self.zbuffer[y][x]:
                    self.point(x, y)
                    self.zbuffer[y][x] = z

    def transform(self, vertex):
        augmented_vertex = [
            [vertex.x],
            [vertex.y],
            [vertex.z],
            [1]
        ]
        tranformed_vertex = MultMatriz(self.Viewport, self.Projection)
        tranformed_vertex = MultMatriz(tranformed_vertex, self.View)
        tranformed_vertex = MultMatriz(tranformed_vertex, self.Model)
        tranformed_vertex = MultMatriz(tranformed_vertex, augmented_vertex)

        tranformed_vertex = [
            (tranformed_vertex[0][0]),
            (tranformed_vertex[1][0]),
            (tranformed_vertex[2][0])
        ]
        return V3(*tranformed_vertex)

    def load(self, filename, translate=(0, 0, 0), scale=(1, 1, 1), rotate=(0, 0, 0)):
        self.loadModelMatrix(translate, scale, rotate)
        model = Obj(filename)
        vertex_buffer_object = []

        for face in model.faces:
            vcount = len(face)
            if vcount == 3:
                for facepart in face:
                    vertex = self.transform(V3(*model.vertices[facepart[0]-1]))
                    vertex_buffer_object.append(vertex)

                if self.active_texture:
                    for facepart in face:
                        tvertex = V2(*model.tvertices[facepart[1]-1])
                        vertex_buffer_object.append(tvertex)

                    for facepart in face:
                        nvertex = V3(*model.normals[facepart[2]-1])
                        vertex_buffer_object.append(nvertex)

            elif vcount == 4:
                for faceindex in [0, 1, 2]:
                    facepart = face[faceindex]
                    vertex = self.transform(V3(*model.vertices[facepart[0]-1]))
                    vertex_buffer_object.append(vertex)
                try:
                    if self.active_texture:
                        for faceindex in range(0, 3):
                            facepart = face[faceindex]
                            tvertex = V2(*model.tvertices[facepart[1]-1])
                            vertex_buffer_object.append(tvertex)

                        for faceindex in range(0, 3):
                            facepart = face[faceindex]
                            nvertex = V3(*model.normals[facepart[2]-1])
                            vertex_buffer_object.append(nvertex)

                    for faceindex in [3, 0, 2]:
                        facepart = face[faceindex]
                        vertex = self.transform(
                            V3(*model.vertices[facepart[0]-1]))
                        vertex_buffer_object.append(vertex)

                    if self.active_texture:
                        for faceindex in [3, 0, 2]:
                            facepart = face[faceindex]
                            tvertex = V2(*model.tvertices[facepart[1]-1])
                            vertex_buffer_object.append(tvertex)

                        for faceindex in [3, 0, 2]:
                            facepart = face[faceindex]
                            nvertex = V3(*model.normals[facepart[2]-1])
                            vertex_buffer_object.append(nvertex)
                except:
                    pass
        self.active_vertex_array = iter(vertex_buffer_object)

    def draw_arrays(self, polygon):
        if polygon == 'TRIANGLES':
            try:
                while True:
                    self.triangle()
            except StopIteration:
                pass

    def loadModelMatrix(self, translate=(0, 0, 0), scale=(1, 1, 1), rotate=(0, 0, 0)):
        translate = V3(*translate)
        scale = V3(*scale)
        rotate = V3(*rotate)

        translation_matrix = [
            [1, 0, 0, translate.x],
            [0, 1, 0, translate.y],
            [0, 0, 1, translate.z],
            [0, 0, 0, 1],
        ]

        a = rotate.x
        rotation_matrix_x = [
            [1, 0, 0, 0],
            [0, math.cos(a), -math.sin(a), 0],
            [0, math.sin(a),  math.cos(a), 0],
            [0, 0, 0, 1]
        ]

        a = rotate.y
        rotation_matrix_y = [
            [math.cos(a), 0,  math.sin(a), 0],
            [0, 1,       0, 0],
            [-math.sin(a), 0,  math.cos(a), 0],
            [0, 0,       0, 1]
        ]

        a = rotate.z
        rotation_matrix_z = [
            [math.cos(a), -math.sin(a), 0, 0],
            [math.sin(a),  math.cos(a), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]

        rotation_matrix = MultMatriz(rotation_matrix_x, rotation_matrix_y)
        rotation_matrix = MultMatriz(rotation_matrix, rotation_matrix_z)

        scale_matrix = [
            [scale.x, 0, 0, 0],
            [0, scale.y, 0, 0],
            [0, 0, scale.z, 0],
            [0, 0, 0, 1],
        ]

        MultMatrizodelo = MultMatriz(translation_matrix, rotation_matrix)
        self.Model = MultMatriz(MultMatrizodelo, scale_matrix)

    def loadViewMatrix(self, x, y, z, center):
        M = [
            [x.x, x.y, x.z,  0],
            [y.x, y.y, y.z, 0],
            [z.x, z.y, z.z, 0],
            [0,     0,   0, 1]
        ]

        O = [
            [1, 0, 0, -center.x],
            [0, 1, 0, -center.y],
            [0, 0, 1, -center.z],
            [0, 0, 0, 1]
        ]

        self.View = MultMatriz(M, O)

    def loadProjectionMatrix(self, coeff):
        self.Projection = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, coeff, 1]
        ]

    def loadViewportMatrix(self, x=0, y=0):
        self.Viewport = [
            [self.width/2, 0, 0, x + self.width/2],
            [0, self.height/2, 0, y + self.height/2],
            [0, 0, 128, 128],
            [0, 0, 0, 1]
        ]

    def lookAt(self, eye, center, up):
        z = norm(sub(eye, center))
        x = norm(cross(up, z))
        y = norm(cross(z, x))
        self.loadViewMatrix(x, y, z, center)
        self.loadProjectionMatrix(-1 / length(sub(eye, center)))
        self.loadViewportMatrix()

    def glFinish(self, filename):
        f = open(filename, 'wb')

        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        for x in range(self.height):
            for y in range(self.width):
                f.write(self.buffer[x][y])

        f.close()
