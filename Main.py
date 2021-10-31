# ***********************************************************************************
#   ExibePoligonos.py
#       Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
#   Este programa exibe um polígono em OpenGL
#   Para construir este programa, foi utilizada a biblioteca PyOpenGL, disponível em
#   http://pyopengl.sourceforge.net/documentation/index.html
#
#   Sugere-se consultar também as páginas listadas
#   a seguir:
#   http://bazaar.launchpad.net/~mcfletch/pyopengl-demo/trunk/view/head:/PyOpenGL-Demo/NeHe/lesson1.py
#   http://pyopengl.sourceforge.net/documentation/manual-3.0/index.html#GLUT
#
#   No caso de usar no MacOS, pode ser necessário alterar o arquivo ctypesloader.py,
#   conforme a descrição que está nestes links:
#   https://stackoverflow.com/questions/63475461/unable-to-import-opengl-gl-in-python-on-macos
#   https://stackoverflow.com/questions/6819661/python-location-on-mac-osx
#   Veja o arquivo Patch.rtf, armazenado na mesma pasta deste fonte.
# ***********************************************************************************

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Poligonos import *
from Road import *
from Car import *
import re

# Limites da Janela de Seleção
Min = Vector(-50, -50)
Max = Vector(50, 50)

# Setup do jogo
FPS = math.floor(1000/60)
Player = Car(AIType.PLAYER)
Roads = []


def readRoads():
    infile = open("curvas.txt")

    for line in infile.readlines():
        points = [Vector(x[1], x[2]) for x in [x.groups() for x in re.finditer('((-*\d+)\,(-*\d+))', line)]]
        rua = Road(points)
        global Roads
        Roads += [rua]

    infile.close()

def connectRoads():
    for road in Roads:
        foreward = road.lastPoint()
        backward = road.firstPoint()
        for next in Roads:
            nextForeward = next.lastPoint()
            nextBackward = next.firstPoint()
            if(foreward == nextBackward):
                road.connectedForeward.add(next)
                next.connectedBackward.add(road)
            if(backward == nextForeward):
                road.connectedBackward.add(next)
                next.connectedForeward.add(road)

readRoads()
connectRoads()
print("Ruas")
[print(x) for x in Roads]

Player.setStart(Roads[0], 0)
print("Player")
print(Player)

def reshape(w,h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    BordaX = abs(Max.x-Min.x)*0.1
    BordaY = abs(Max.y-Min.y)*0.1
    glOrtho(Min.x-BordaX, Max.x+BordaX, Min.y-BordaY, Max.y+BordaY, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glColor3f(1.0, 1.0, 0.0)
    for road in Roads: road.render()
    Player.render()
    glutSwapBuffers()

ESCAPE = b'\x1b'
def keyboard(*args):
    print(args[0])
    c = args[0]
    if c == b'q':
        os._exit(0)
    elif c == ESCAPE:
        os._exit(0)
    elif c == b' ':
        Player.setSpeed()
    elif c == b'w':
        Player.setSpeed(Speeds.FOREWARD)
    elif c == b's':
        Player.setSpeed(Speeds.BACKWARD)


def idle(value):
    Player.move()
    glutPostRedisplay()
    glutTimerFunc(FPS, idle, value)

glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500)
glutInitWindowPosition(100, 100)
wind = glutCreateWindow("Exibe Polignos")
glutDisplayFunc(display)
glutReshapeFunc(reshape)
glutKeyboardFunc(keyboard)
glutTimerFunc(FPS, idle, 0)

try:
    glutMainLoop()
except SystemExit:
    pass
