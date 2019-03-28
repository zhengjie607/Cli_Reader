import math
import sympy
class Point (object):
  # constructor with default values
    def __init__ (self, x = 0, y = 0):
        self.x = x
        self.y = y

  # get distance to another Point object
    def dist (self, other):
        return (math.sqrt(abs(self.x - other.x)**2 + abs(self.y - other.y)**2))

  # create a string representation of a Point (x, y)
    def __str__ (self):
        return ('(' + str(self.x) + ', ' + str(self.y) + ')')

  # test for equality between two points
    def __eq__ (self, other):
        tol = 1.0e-18
        return (abs(self.x - other.x) < tol) and (abs(self.y - other.y) < tol)
class Line:
    def __init__(self,p1,p2,tol=1e-18):
        self.tol=tol
        if (abs(p1.x-p2.x)<self.tol) and (abs(p1.y-p2.y)<self.tol):
            self.isline=False
        else:
            self.isline=True
        if self.isline:
            self.p1=p1
            self.p2=p2
            self.A,self.B,self.C=self._getABC()
            self.Xmin,self.Xmax,self.Ymin,self.Ymax=self._max_min()
    def is_parallel_x (self):
        return (abs(self.p1.y - self.p2.y) < self.tol) 
    #return xmin,xmax,ymin,ymax
    def _max_min(self):
        return min(self.p1.x,self.p2.x),max(self.p1.x,self.p2.x),min(self.p1.y,self.p2.y),max(self.p1.y,self.p2.y)
  # determine if line is parallel to y axis
    def is_parallel_y (self):
        return (abs(self.p1.x - self.p2.x) < self.tol)
    def _getABC(self):
        A = self.p2.y - self.p1.y
        B = self.p1.x - self.p2.x
        C = self.p2.x * self.p1.y - self.p1.x * self.p2.y
        return A,B,C
    def on_same_side(self,p1,p2):
        if abs(self.B)<self.tol:
            return (p1.x>-self.C/self.A and p2.x>-self.C/self.A) or (p1.x<-self.C/self.A and p2.x<-self.C/self.A)
        else:
            y1=-(self.A*p1.x+self.C)/self.B
            y2=-(self.A*p2.x+self.C)/self.B
            return (p1.y > y1 and p2.y > y2) or (p1.y < y1 and p2.y < y2)
    def intersection_point(self, other):
        if not self.on_same_side(other.p1,other.p2):
            x,y=sympy.symbols('x y')
            w=sympy.solve([self.A*x+self.B*y+self.C,other.A*x+other.B*y+other.C],[x,y])
            return Point(w[x],w[y])
class LineBykd:
    def __init__(self,angle,intercept):
        self.tol=1.0e-18
        self.d=intercept   
        if abs(angle-90)<self.tol:
            self.k=float('inf')
        else:
            self.k=math.tan(angle*math.pi/180)
    def on_same_side(self,otherline):
        if self.k==float('inf'):
            return (otherline.p1.x<self.d and otherline.p2.x<self.d) or (otherline.p1.x>self.d and otherline.p2.x>self.d)
        else:
            y1=self.k*otherline.p1.x+self.d
            y2=self.k*otherline.p2.x+self.d
            return (otherline.p1.y-y1) * (otherline.p2.y-y2 )>self.tol
    def intersection_point(self,otherline):
        if not self.on_same_side(otherline):
            x,y=sympy.symbols('x y')
            if self.k==float('inf'):
                w=sympy.solve([x-self.d,otherline.A*x+otherline.B*y+otherline.C],[x,y])
            else:
                w=sympy.solve([self.k*x-y+self.d,otherline.A*x+otherline.B*y+otherline.C],[x,y])
            if type(w[x])==sympy.Add or type(w[x])==sympy.numbers.One:
                return otherline.p1,otherline.p2
            else:
                return Point(w[x],w[y])
        else:
            return None
