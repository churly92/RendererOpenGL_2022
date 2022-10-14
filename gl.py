import glm #pip install PyGLM

from numpy import array, float32

# pip install PyOpenGL
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader


class Buffer(object):
    def __init__(self, data):
        self.data = data

        self.createVertexBuffer()

    def createVertexBuffer(self):
        self.vertBuffer = array(self.data, dtype = float32)

        # Vertex Buffer Object
        self.VBO = glGenBuffers(1)

        # Vertex Array Object
        self.VAO = glGenVertexArrays(1)

    def render(self):

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBindVertexArray(self.VAO)

        # Mandar la informacion de vertices
        glBufferData(GL_ARRAY_BUFFER,           # Buffer ID
                     self.vertBuffer.nbytes,    # Buffer size in bytes
                     self.vertBuffer,           # Buffer data
                     GL_STATIC_DRAW)            # Usage

        # Atributos

        # Atributo de posiciones
        glVertexAttribPointer(0,                # Attribute number
                              3,                # Size
                              GL_FLOAT,         # Type
                              GL_FALSE,         # Is it normalized
                              4 * 6,            # Stride
                              ctypes.c_void_p(0))# Offset

        glEnableVertexAttribArray(0)

        # Atributo de color
        glVertexAttribPointer(1,                # Attribute number
                              3,                # Size
                              GL_FLOAT,         # Type
                              GL_FALSE,         # Is it normalized
                              4 * 6,            # Stride
                              ctypes.c_void_p(4*3))# Offset

        glEnableVertexAttribArray(1)

        glDrawArrays(GL_TRIANGLES, 0, int(len(self.vertBuffer) / 6) )


class Renderer(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        glEnable(GL_DEPTH_TEST)
        glViewport(0,0, self.width, self.height)

        self.scene = []
        self.active_shader = None

    def setShaders(self, vertexShader, fragmentShader):
        if vertexShader is not None and fragmentShader is not None:
            self.active_shader = compileProgram( compileShader(vertexShader, GL_VERTEX_SHADER),
                                                 compileShader(fragmentShader, GL_FRAGMENT_SHADER))
        else:
            self.active_shader = None

    def render(self):
        glClearColor(0.2,0.2,0.2, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if self.active_shader is not None:
            glUseProgram(self.active_shader)

        for obj in self.scene:
            obj.render()
