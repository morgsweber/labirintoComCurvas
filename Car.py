from re import S
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Vector import *
from enum import Enum
import copy
import random
import math
class AIType(Enum):
  PLAYER = 1
  ENEMY = 2

CAR_BODY = [Vector(-2, -2), Vector(2, -2), Vector(0, 4)]
SPEED = 0.1

class Car:
  def __init__(self, type = AIType.ENEMY):
    self.type = type
    self.Road = None
    self.next = None
    self.Vertices = copy.deepcopy(CAR_BODY)
    self.position = 0
    self.direction = -1
    self.moving = True

  def setStart(self, road=None, position=0):
    self.Road = road
    self.position = position
  
  def render(self):
    if(self.type == AIType.PLAYER): glColor3d(0, 1, 0)
    else: glColor3d(1, 0, 0)
    glPushMatrix()
    point = self.Road.getPoint(self.position)
    glTranslate(point.x, point.y, 0)

    direction = self.Road.tangent(self.position)
    rotation = math.degrees(math.atan2(direction.x, direction.y))
    glRotate(-rotation + (0 if (self.direction == 1) else 180), 0, 0, 1)

    glBegin(GL_POLYGON)
    [glVertex3f(p.x, p.y, 0) for p in self.Vertices]
    glEnd()
    glPopMatrix()

  def move(self):
    movement = SPEED * self.direction
    self.position += movement / self.Road.length
    if(self.direction == 1):
      if(self.position > 0.5 and self.next == None): 
        self.chooseNext()
      elif(self.position > 1):
        self.Road = self.next
        self.position = 0
        self.next = None
    else:
      if(self.position < 0.5 and self.next == None): 
        self.chooseNext()
      elif(self.position < 0):
        self.Road = self.next
        self.position = 1
        self.next = None
        self.Road.selected = False

  def chooseNext(self):
    if(self.direction == 1):
      size = len(self.Road.connectedForeward)
      next = random.randint(0, size-1)
      self.next = list(self.Road.connectedForeward)[next]
    else:
      size = len(self.Road.connectedBackward)
      next = random.randint(0, size-1)
      self.next = list(self.Road.connectedBackward)[next]
    self.next.selected = True

  def __str__(self):
    return f"Road: {self.Road}\nNext: {self.next}\nPosition: {self.position}\nMoving: {self.moving}\nDirection: {self.direction}\nType: {self.type}"
