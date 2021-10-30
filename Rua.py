from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Point import *
import copy
import math

class Rua:
    _RESOLUTION = 50
    
    def __init__(self):
        self.Points = []
    
    def distance(self, a, b):
        return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)

    def add(self, x, y):
        self.Points += [Point(x,y)]

    def getPoint(self, position):
        x, y = 0
        if(len(self.Points) == 3):
            x = (1 - position)**2 * self.Points[0].x + 2 * (1 - position) * position * self.Points[1].x + position**2 * self.Points[2].x
            y = (1 - position)**2 * self.Points[0].y + 2 * (1 - position) * position * self.Points[1].y + position**2 * self.Points[2].y
        
        else:
            x = (1 - position)**3 * self.Points[0].x + 3 * (1 - position)**2 * position * self.Points[1].x + 3 * (1 - position) * position**2 * self.Points[2].x + position**3 * self.Points[3].x
            y = (1 - position)**3 * self.Points[0].y + 3 * (1 - position)**2 * position * self.Points[1].y + 3 * (1 - position) * position**2 * self.Points[2].x + position**3 * self.Points[3].y

        point = Point(x,y)
        glVertex3f(point.x, point.y, 0)
        return point

    def render(self):
        delta = 1.0 / self._RESOLUTION
        position = delta
        length = 0
        glLineWidth(2)
        glColor3d(0, 1, 0)
        glBegin(GL_LINE_STRIP)
        P1 = self.getPoint(0.0)
        while(position < 1.0):
            P2 = self.getPoint(position)
            length += self.distance(P1,P2)
            P1 = P2
            position += delta

        P2 = self.getPoint(1.0)
        length += self.distance(P1,P2)
        glEnd()

    def getLimits(self):
        Min = copy.deepcopy(self.Points[0])
        Max = copy.deepcopy(self.Points[0])
        for V in self.Points:
            if V.x > Max.x:
                Max.x = V.x
            if V.y > Max.y:
                Max.y = V.y
            if V.z > Max.z:
                Max.z = V.z
            if V.x < Min.x:
                Min.x = V.x
            if V.y < Min.y:
                Min.y = V.y
            if V.z < Min.z:
                Min.z = V.z
        return Min, Max
