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

CAR_BODY = [Vector(-1, -1), Vector(1, -1), Vector(0, 2)]
SPEED = 0.1
SIZE = 1.5

class Speeds(Enum):
  STOP = 0
  FOREWARD = 1
  BACKWARD = 2

class Car:
  def __init__(self, type = AIType.ENEMY):
    self.type = type
    self.road = None
    self.next = None
    self.vertices = copy.deepcopy(CAR_BODY)
    self.position = 0
    self.speed = SPEED
    self.angle = 0

  def setStart(self, road=None, position=0):
    self.road = road
    self.position = position

  def setSpeed(self, speed=Speeds.STOP):
    if(speed == Speeds.STOP):
      self.speed = 0
      if(self.next):
        self.next.selected = False
        self.next = None
    elif(speed == Speeds.FOREWARD and self.speed == 0):
      self.speed = SPEED
    elif(speed == Speeds.BACKWARD and self.speed == 0):
      self.speed = -SPEED

  def render(self):
    if(self.type == AIType.PLAYER): glColor3d(0, 1, 0)
    else: glColor3d(1, 0, 0)
    glPushMatrix()
    point = self.road.getPoint(self.position)
    glTranslate(point.x, point.y, 0)

    glScale(SIZE, SIZE, 1)

    if(self.speed != 0):
      direction = self.road.tangent(self.position)
      self.angle = -math.degrees(math.atan2(direction.x, direction.y)) + (0 if (self.speed > 0) else 180)
    glRotate(self.angle, 0, 0, 1)

    glBegin(GL_POLYGON)
    [glVertex3f(p.x, p.y, 0) for p in self.vertices]
    glEnd()
    glPopMatrix()

  def move(self):
    if(self.speed == 0): 
      return

    self.position += self.speed / self.road.length

    if(self.speed > 0):
      if(self.position > 0.5 and self.next == None): 
        self.chooseNext()
      elif(self.position > 1):
        self.road = self.next.road
        self.speed *= self.next.bias
        self.position = 0 if self.next.bias == 1 else 1
        self.next = None
        if(self.type == AIType.PLAYER): self.road.selected = False
    else:
      if(self.position < 0.5 and self.next == None): 
        self.chooseNext()
      elif(self.position < 0):
        self.road = self.next.road
        self.speed *= self.next.bias
        self.position = 1 if self.next.bias == 1 else 0
        self.next = None
        if(self.type == AIType.PLAYER): self.road.selected = False

  def chooseNext(self):
    if(self.speed > 0):
      size = len(self.road.connectedForeward)
      next = random.randint(0, size-1)
      self.next = self.road.connectedForeward[next]
    else:
      size = len(self.road.connectedBackward)
      next = random.randint(0, size-1)
      self.next = self.road.connectedBackward[next]
    
    if(self.type == AIType.PLAYER): self.next.road.selected = True

  def cicleRoads(self, clockwise=True):
    if(self.next):
      current = 0
      size = 0
      if(self.speed > 0):
        size = len(self.road.connectedForeward)
        current = self.road.connectedForeward.index(self.next)

      else:
        size = len(self.road.connectedBackward)
        current = self.road.connectedBackward.index(self.next)
      
      current += 1 if clockwise else -1
      if(current >= size):
        current = 0
      elif(current < 0):
        current = size - 1

      self.next.road.selected = False
      if(self.speed > 0):
        self.next = self.road.connectedForeward[current]
      else:
        self.next = self.road.connectedBackward[current]
      self.next.road.selected = True

  def __str__(self):
    return f"Road: {self.road}\nNext: {self.next}\nPosition: {self.position}\nSpeed: {self.speed}\nType: {self.type}"
