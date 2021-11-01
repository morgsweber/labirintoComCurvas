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
from Connection import Connection
from Poligonos import *
from Road import *
from Car import *
import re
import random

# Limites da Janela de Seleção
Min = Vector(-50, -50)
Max = Vector(50, 50)

# Setup do jogo
FPS = math.floor(1000/60)
ENEMIES = 2
Player = Car(AIType.PLAYER)
Enemies = [Car() for x in range(ENEMIES)]
Roads = []
colisions = 0

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
            if(road != next):
                nextForeward = next.lastPoint()
                nextBackward = next.firstPoint()
                # if found --> O --> (saída de um para entrada de outro)
                # addiciona conexões convencionais para ambas ruas
                if(foreward == nextBackward):
                    Connection(road).addToBackward(next)
                    Connection(next).addToForeward(road)

                # if found --> O <-- (saída de um para saída de outro)
                # addiciona conexões invertidas para ambas ruas
                if(foreward == nextForeward):
                    Connection(road, True).addToBackward(next)
                    Connection(next, True).addToBackward(road)
                    
                # if found <-- O <-- (entrada de um para saída de outro)
                # addiciona conexões convencionais para ambas ruas
                if(backward == nextForeward):
                    Connection(road).addToForeward(next)
                    Connection(next).addToBackward(road)

                # if found <-- O --> (entrada de um para entrada de outro)
                # addiciona conexões invertidas para ambas ruas
                if(backward == nextBackward):
                    Connection(road, True).addToForeward(next)
                    Connection(next, True).addToForeward(road)

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
    for enemy in Enemies: enemy.render()
    glutSwapBuffers()

def checkCollision():
    if(any([abs(car.length - Player.length) < 1 for car in Player.road.cars])):
        global colisions
        colisions += 1
        print(f"colision {colisions}")

ESCAPE = b'\x1b'
def keyboard(*args):
    print(args[0])
    c = args[0]
    if c == ESCAPE:
        os._exit(0)
    elif c == b' ':
        Player.setSpeed()
    elif c == b'w':
        Player.setSpeed(Speeds.FOREWARD)
    elif c == b's':
        Player.setSpeed(Speeds.BACKWARD)
    elif c == b'a':
        Player.cicleRoads(False)
    elif c == b'd':
        Player.cicleRoads(True)

def idle(value):
    Player.move()
    for enemy in Enemies: enemy.move()
    checkCollision()
    glutPostRedisplay()
    glutTimerFunc(FPS, idle, value)

readRoads()
connectRoads()
print("Ruas")
[print(x) for x in Roads]
print("-----")

pool = random.sample(range(len(Roads)), ENEMIES + 1)
random.shuffle(pool)

Player.setStart(Roads[pool.pop()], 0.5)
print("Player")
print(Player)
print("-----")

for enemy in Enemies:
    enemy.setStart(Roads[pool.pop()], 0.5, random.random() > 0.5)
print("Enemies")
[print(x) for x in Enemies]
print("-----")

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
