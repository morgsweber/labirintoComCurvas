import math

class Vector:   
	def __init__(self, x=0,y=0):
		self.x = float(x)
		self.y = float(y)
	
	def __str__(self): 
		return f"({self.x}, {self.y})"

	def __eq__(self, obj):
		return self.x == obj.x and self.y == obj.y

	def sub(self, point):
		return Vector(self.x - point.x, self.y - point.y)

	def normalize(self):
		distance = math.hypot(self.x, self.y)
		return Vector(self.x/distance, self.y/distance)

	def distance(self, point):
		return math.sqrt((self.x - point.x)**2 + (self.y - point.y)**2)

