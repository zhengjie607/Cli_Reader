
# coding: utf-8

# In[42]:


import struct
import numpy as np
from line import Line,Point,LineBykd
import math
path=r"F:\艾德威尔\软件\上位机\选区\喷杆cli\yp.cli"
class CLI():
    def __init__(self,path):
        self.UsePoint=[]
        self.UseLine=[]
        self.fillpoint=[]
        self.read(path)
    def read(self,path):
        with open(path,'rb') as f:
            file=f.read()
            head=str(file).split('$$HEADEREND')
            head=head[0].split('\\n')
            #print(head)
            for line in head:
                if '$$UNITS' in line:
                    self.unit=float(line.split('/')[1])
                if '$$DIMENSION' in line:
                    bound=line.split('/')[1]
                    Xmin,Ymin,Zmin,Xmax,Ymax,Zmax=bound.split(',')
                    self.Xmin=float(Xmin)
                    self.Ymin=float(Ymin)
                    self.Zmin=float(Zmin)
                    self.Xmax=float(Xmax)
                    self.Ymax=float(Ymax)
                    self.Zmax=float(Zmax)
                if '$$LAYERS' in line:
                    self.layer=int(line.split('/')[1])
            #print(head[0])
            f.seek(226,0)
            ty=struct.unpack('<H',f.read(2))
            #print("type:",ty)
            try:
                while True:
                    layer=struct.unpack('<H',f.read(2))
                    #print("layer:",layer)
                    Mypoint=[]
                    while True:
                        mypoint=[]
                        readtpye=struct.unpack('<H',f.read(2))
                        #print("readtype:",readtpye)
                        if readtpye[0]==128:
                            break
                        ID,Direction,Point_Num=struct.unpack('<HHH',f.read(6))
                        '''print("ID:",ID)
                        print("Direction:",Direction)
                        print("Point_Num:",Point_Num)'''
                        for i in range(Point_Num):
                            x,y=struct.unpack('<HH',f.read(4))
                            mypoint.append(Point(x*self.unit,y*self.unit))
                        Mypoint.append(mypoint)
                    self.UsePoint.append(Mypoint)
            except:
                self.UsePoint.append(Mypoint)
                #print('Finish!')
    def optimizer(self):
        pass
    def fill(self,angle,distance,layer_num):
        self.getline()
        data=self.UseLine[layer_num]
        if angle==90:
            start_d=self.Xmin
            step=distance
            totallen=self.Xmax-self.Xmin
        else:
            start_d=min((self.Ymin-self.Xmin*math.tan(angle*math.pi/180)),(self.Ymin-self.Xmax*math.tan(angle*math.pi/180)))
            step=distance/math.cos(angle*math.pi/180)
            totallen=math.sqrt((self.Ymax-self.Ymin)*(self.Ymax-self.Ymin)+(self.Xmax-self.Xmin)*(self.Xmax-self.Xmin))
        circle_num=int(totallen/step)+1
        for i in range(circle_num):
            filline=LineBykd(angle,start_d)
            point_list=[]
            for j in range(len(data)):
                for w in range(len(data[j])):
                    p=filline.intersection_point(data[j][w])
                    if p is not None:
                        point_list.append(filline.intersection_point(data[j][w]))
            if len(point_list)%2==0:
                self.fillpoint.append(point_list)
            start_d=start_d+step
    def getline(self):
        for i in range(len(self.UsePoint)):
            line1=[]
            for j in range(len(self.UsePoint[i])):
                line=[]
                for w in range(len(self.UsePoint[i][j])-1):
                    l=Line(self.UsePoint[i][j][w],self.UsePoint[i][j][w+1])
                    if l.isline:
                        line.append(l)
                line1.append(line)
            self.UseLine.append(line1)
if __name__=='__main__':
    w=CLI(path)
    print(len(w.UsePoint))
    print(w.layer)
    print(w.Xmin)
