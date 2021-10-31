from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Point import *

RESOLUTION = 20

class Road:
    def __init__(self, points = []):
        self.Points = points
        self.order = len(self.Points)
        self.length = 0
        # calcula as coordenadas de bounding box
        self.connectedForeward = set()
        self.connectedBackward = set()
        self.calculateLength()

    def firstPoint(self): return self.Points[0]
    def lastPoint(self): return self.Points[self.order - 1]

    # matemática do site https://javascript.info/bezier-curve
    def getPoint(self, position):
        x = 0
        y = 0
        if(self.order == 3):
            x = (1 - position)**2 * self.Points[0].x + 2 * (1 - position) * position * self.Points[1].x + position**2 * self.Points[2].x
            y = (1 - position)**2 * self.Points[0].y + 2 * (1 - position) * position * self.Points[1].y + position**2 * self.Points[2].y
        
        else:
            x = (1 - position)**3 * self.Points[0].x + 3 * (1 - position)**2 * position * self.Points[1].x + 3 * (1 - position) * position**2 * self.Points[2].x + position**3 * self.Points[3].x
            y = (1 - position)**3 * self.Points[0].y + 3 * (1 - position)**2 * position * self.Points[1].y + 3 * (1 - position) * position**2 * self.Points[2].y + position**3 * self.Points[3].y

        point = Point(x,y)
        return point

    def render(self):
        delta = 1.0 / RESOLUTION
        position = delta
        glLineWidth(2)
        glColor3d(0.7, 0.7, 0.7)
        glBegin(GL_LINE_STRIP)
        point = self.getPoint(0.0)
        glVertex3f(point.x, point.y, 0)

        while(position < 1.0):
            point = self.getPoint(position)
            glVertex3f(point.x, point.y, 0)
            position += delta

        point = self.getPoint(1.0)
        glVertex3f(point.x, point.y, 0)
        glEnd()

    def calculateLength(self):
        delta = 1.0 / RESOLUTION
        position = delta
        P1 = self.getPoint(0.0)
        while(position < 1.0):
            P2 = self.getPoint(position)
            self.length += P1.distance(P2)
            P1 = P2
            position += delta

        P2 = self.getPoint(1.0)
        self.length += P1.distance(P2)

    def __str__(self):
        return f"Points: {[str(x) for x in self.Points]}\nLength: {self.length}\nForeward: {len(self.connectedForeward)}\nBackward: {len(self.connectedBackward)}"
