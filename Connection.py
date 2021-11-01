class Connection:
  def __init__(self, road, inverted=False):
    self.road = road
    self.bias = -1 if inverted else 1
    
  def addToForeward(self, road):
    if(all([self.road != connection.road for connection in road.connectedForeward])):
      road.connectedForeward += [self]

  def addToBackward(self, road):
    if(all([self.road != connection.road for connection in road.connectedBackward])):
      road.connectedBackward += [self]