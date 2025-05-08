import turtle as T
import math


T.delay(0)
T.speed(0)

#vars
gridAmount = 50 #this num but squared is how many dots
k = 8.99e9 #constant
q = 2 #charge of dipoles
d = 0.5 #distance between dipoles
dotList = []
DipoleX = gridAmount // 2
DipoleY = gridAmount // 2


T.setworldcoordinates(0, 0, gridAmount, gridAmount)

class Dot(T.Turtle):
    def __init__(self,x,y):
        T.Turtle.__init__(self)
        self.pu()
        self.x = x
        self.y = y
        self.shape('square')
        self.goto(x,y)
    def ChangeColors(self, E):
        if E > (1e9):
            self.color('red')
        elif E > (1e8):
            self.color('orange')
        elif E > (1e7):
            self.color('yellow')
        elif E > (1e6):
            self.color('green')
        elif E > 1e5:
            self.color('lightblue')
        elif E > 1e4:
            self.color('blue')
        elif E > 1e3:
            self.color('darkblue')
        elif E > 1e2:
            self.color('purple')
        else:
            self.color('white')
        
def CreateDot(x,y):
    dot = Dot(x,y)
    dotList.append(dot)
    
def CreateGrid():
    for i in range(gridAmount):
        for j in range(gridAmount):
            CreateDot(i,j)

def FindValues():
    for dot in dotList:
        if (dot.x != DipoleX) or (dot.y != DipoleY):
            r = math.sqrt(((dot.x - DipoleX)**2) + ((dot.y - DipoleY)**2))
            cosAngle = (dot.x-DipoleX)/(math.sqrt((dot.x-DipoleX)**2 + (dot.y-DipoleY)**2))
            p = q*d
            E = k*((p)/(r*r*r)*(math.sqrt((3*(cosAngle*cosAngle))+1)))    
        else:
            E = 0
        dot.ChangeColors(E)
        
CreateGrid()
FindValues()
T.mainloop()