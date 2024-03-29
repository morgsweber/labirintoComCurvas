# ***********************************************************************************
#   Main.py
#   Autores: Leonardo Scholler e Morgana Weber
# ***********************************************************************************

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Connection import ConnectionBackward, ConnectionForeward
from Poligonos import *
from Road import *
from Car import *
import re
import random

# Setup do jogo
FPS = math.floor(1000/60)
ENEMIES = 10
Player = Car(AIType.PLAYER)
Enemies = [Car() for x in range(ENEMIES)]
Points = []
Roads = []
MIN = Vector()
MAX = Vector()

# Limites da Janela de Seleção
def getLimits(points):
    for point in points:
        if point.x > MAX.x:
            MAX.x = point.x
        if point.y > MAX.y:
            MAX.y = point.y
        if point.x < MIN.x:
            MIN.x = point.x
        if point.y < MIN.y:
            MIN.y = point.y

def readRoads():
    infile = open("points.txt")

    for line in infile.readlines():
        global Points
        Points += [Vector(x[1], x[2]) for x in [x.groups() for x in re.finditer('((-*\d+)\s(-*\d+))', line)]]
    getLimits(Points)

    infile.close()

    infile = open("curves.txt")
    for line in infile.readlines():
        global Roads
        Roads += [Road([Points[int(x[0])] for x in [x.groups() for x in re.finditer('(\d+)', line)]])]

    infile.close()

def sortRoadForeward(connection):
    return connection.road.tangent(0).getAngle()

def sortRoadBackward(connection):
    return connection.road.tangent(1).getAngle()

def connectRoads():
    # Uma rua é definida como B -> F
    # Rua C
    for current in Roads:
        foreward = current.lastPoint()
        backward = current.firstPoint()
        # Rua N
        for next in Roads:
            nextForeward = next.lastPoint()
            nextBackward = next.firstPoint()
            # Caso C --> --> N: CF[N], NB[C]
            if(foreward == nextBackward):
                ConnectionForeward(current, next)
                ConnectionBackward(next, current)

            # Caso C <-- <-- N: CB[N], NF[C]
            if(backward == nextForeward):
                ConnectionBackward(current, next)
                ConnectionForeward(next, current)

            if(current != next):
                # Caso C --> <-- N: CF[-N], NF[-C]
                if(foreward == nextForeward):
                    ConnectionForeward(current, next, True)
                    ConnectionForeward(next, current, True)

                # Caso C <-- --> N: CB[-N], NB[-C]
                if(backward == nextBackward):
                    ConnectionBackward(current, next, True)
                    ConnectionBackward(next, current, True)

    for road in Roads:
        road.connectedForeward.sort(key=sortRoadForeward)
        road.connectedBackward.sort(key=sortRoadBackward)

def reshape(w,h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    BordaX = abs(MAX.x-MIN.x)*0.1
    BordaY = abs(MAX.y-MIN.y)*0.1
    glOrtho(MIN.x-BordaX, MAX.x+BordaX, MIN.y-BordaY, MAX.y+BordaY, 0.0, 1.0)
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
        print(f"Colisão detectada, game over")
        os._exit(0)

ESCAPE = b'\x1b'
def keyboard(*args):
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
print("Pontos")
[print(x) for x in Points]
print("Ruas")
[print(x) for x in Roads]
print("-----")
connectRoads()

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
