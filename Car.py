from re import S
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Point import *
from enum import Enum
import copy
import random
class AIType(Enum):
  PLAYER = 1
  ENEMY = 2

CAR_BODY = [Point(-1, -1), Point(-1, 1), Point(2, 0)]
SPEED = 0.001

class Car:
  def __init__(self, type = AIType.ENEMY):
    self.type = type
    self.Road = None
    self.next = None
    self.Vertices = copy.deepcopy(CAR_BODY)
    self.position = 0
    self.direction = 1
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
    glBegin(GL_POLYGON)
    [glVertex3f(p.x, p.y, 0) for p in self.Vertices]
    glEnd()
    glPopMatrix()

  def move(self):
    self.position += SPEED * self.direction / self.Road.length
    if(self.position > 0.5 and self.next == None): 
      self.chooseNext()
    elif(self.position > 1):
      self.Road = self.next
      self.position = self.direction + 1 / 2
      self.next = None


  def chooseNext(self):
    return
    if(self.direction == 1):
      size = len(self.Road.connectedForeward)
      next = random.randint(0, size-1)
      self.next = self.Road.connectedForeward[next]
    else:
      size = len(self.Road.connectedBackward)
      next = random.randint(0, size-1)
      self.next = self.Road.connectedBackward[next]

  def __str__(self):
    return f"Road: {self.Road}\nNext: {self.next}\nPosition:{self.position}\nMoving: {self.moving}\nDirection {self.direction}\nType {self.type}"
