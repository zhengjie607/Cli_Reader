from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from OpenGL.GL import *
from OpenGL.arrays import vbo
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Camera import camera
from Vector3f import *
from numpy import array
import numpy
class GLWidget(QOpenGLWidget):
    def __init__(self, *args, **kwargs):
        super(GLWidget, self).__init__(*args, **kwargs)
        self.setGeometry(QtCore.QRect(10, 10,700, 700))#窗口位置和大小
        self.isMove=False
        self.data=[]
        self.layerindex=0
    def initdata(self,data):
        self.data=data
    def initializeGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        self.camera=camera()
        
    def paintGL(self):
        self.camera.Update()
        self.drawbase()
        #glutWireTeapot(0.5)
        if self.data!=[]:
            print("Load")
            self.drawline(self.data,self.layerindex)
            #self.VBO(self.data,0)
        else:
            print('mesh is none')
    def drawbase(self):
        glPushMatrix()
        glBegin(GL_LINE_LOOP)
        glColor(0,1,0)
        glVertex3f(0,0,0)
        glVertex3f(0,250,0)
        glVertex3f(250,250,0)
        glVertex3f(250,0,0)
        glEnd()
        glPopMatrix()
    def drawline(self,list_usepoint,layer_num):
        
        for i in range(0,len(list_usepoint)):
            
            #print("i:",i)
            if len(list_usepoint[i])>layer_num:
                point_num=len(list_usepoint[i][layer_num])
                #print("多段线数量:",point_num)
                for j in range(0,point_num):
                    glBegin(GL_LINE_LOOP)
                    glColor(1,0,0)
                    #print("第{0}个多段线".format(j))
                    for w in range(0,len(list_usepoint[i][layer_num][j])):
                        #print("第{0}个点".format(w))
                        glVertex3f(list_usepoint[i][layer_num][j][w][0],list_usepoint[i][layer_num][j][w][1],0)
                        #print("({0},{1},{2})".format(list_usepoint[i][layer_num][j][w][0],list_usepoint[i][layer_num][j][w][1],z))
                    glEnd()
        
    def VBO(self,list_usepoint,layer_num):
        #glPushMatrix()
        data=array(list_usepoint[0][layer_num][0])
        print(data)
        print(len(data))
        vb=vbo.VBO(data)
        vb.bind()
        #glEnableClientState(GL_NORMAL_ARRAY)
        glEnableClientState(GL_VERTEX_ARRAY)
        #glNormalPointer(GL_FLOAT, 24, vb+12)
        glVertexPointer(3, GL_FLOAT, 12, vb )#在每一个周期里，都有6个32-bit浮点数据，总共4*6=24     3代表数量
        glDrawArrays(GL_TRIANGLES, 0, len(data))
        vb.unbind()
        #glDisableClientState(GL_NORMAL_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)
        #glPopMatrix()
    def mousePressEvent(self,event):
        self.myMousePosition=event.pos()
        if event.button()==QtCore.Qt.LeftButton:
            self.isMove=True
        #self.update()
    def wheelEvent(self,event):
        if event.angleDelta().y()>0:
            self.camera.right*=0.95
            self.camera.top*=0.95
        if event.angleDelta().y()<0:
            self.camera.right/=0.95
            self.camera.top/=0.95
        self.update()
    def mouseReleaseEvent(self,event):
        if event.button()==QtCore.Qt.LeftButton:
            self.isMove=False
    def mouseMoveEvent(self,event):
        if self.isMove:
            moveX=event.pos().x()-self.myMousePosition.x()
            moveY=event.pos().y()-self.myMousePosition.y()
            self.camera.Move(moveX*self.camera.right/300,moveY*self.camera.right/300)
            self.myMousePosition=event.pos()
        self.update()
