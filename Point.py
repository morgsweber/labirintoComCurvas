# ************************************************
#   Point.py
#   Define a classe Ponto
#   Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
# ************************************************


class Point:   
    def __init__(self, x=0,y=0,z=0):
        self.x = x
        self.y = y
        self.z = z
        #print ("Objeto criado")
    
    def imprime(self):
        print (self.x, self.y, self.z)
    
    def set(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z


#P = Point()
#P.set(1,2)
#P.imprime()
#P.set(23,34,56)
#P.imprime()

