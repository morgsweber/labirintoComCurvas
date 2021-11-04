class ConnectionForeward:
  def __init__(self, current, next, inverted=False):
    self.road = next
    self.bias = -1 if inverted else 1
    if(all([self.road != connection.road for connection in current.connectedForeward])):
      current.connectedForeward += [self]

class ConnectionBackward:
  def __init__(self, current, next, inverted=False):
    self.road = next
    self.bias = -1 if inverted else 1
    if(all([self.road != connection.road for connection in current.connectedBackward])):
      current.connectedBackward += [self]