
# coding: utf-8

# In[1]:


from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from gl_widget import GLWidget
from CLI_Reader import CLI
class Ui_Read_cli(QtWidgets.QWidget):
    def __init__(self):
        super(Ui_Read_cli,self).__init__()
        
        self.setObjectName("Form")
        self.resize(950, 700)
        self.setWindowTitle(QtCore.QCoreApplication.translate("Form", "Form"))
        
        self.widget = GLWidget(self)
        self.widget.setGeometry(QtCore.QRect(0, 0, 650, 650))
        self.widget.setObjectName("widget")
        self.widget.setWindowTitle(QtCore.QCoreApplication.translate("Read_cli", "Form"))
        
        self.verticalSlider = QtWidgets.QSlider(self)
        self.verticalSlider.setGeometry(QtCore.QRect(680, 40, 19, 601))
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setObjectName("verticalSlider")
        
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(750, 40, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText(QtCore.QCoreApplication.translate("Read_cli", "导入"))
        
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(750, 80, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText(QtCore.QCoreApplication.translate("Read_cli", "删除"))
        
        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.setGeometry(QtCore.QRect(720, 120, 190, 192))
        self.listWidget.setObjectName("listWidget")
        
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(670, 10, 41, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setText('0')
        
        self.pushButton.clicked.connect(self.inputfile)
        self.pushButton_2.clicked.connect(self.delete)
        self.verticalSlider.valueChanged['int'].connect(self.redraw)
        self.verticalSlider_Max=0
    def inputfile(self):
        dialog=QtWidgets.QFileDialog()
        f=dialog.getOpenFileNames(self,'Open File','./喷杆cli','CLI File (*.cli)')[0]
        for fi in f:
            file=CLI(fi)
            self.widget.data.append(file.UsePoint)
            
            if self.verticalSlider_Max<file.layer:
                self.verticalSlider_Max=file.layer-1
            self.verticalSlider.setMaximum(self.verticalSlider_Max)
            #print((f[0].split('/'))[-1].split('.')[0])
            self.listWidget.addItem((fi.split('/'))[-1].split('.')[0])
        self.widget.update()
        '''file=CLI(f[0])
        self.widget.data.append(file.UsePoint)
        self.widget.update()
        if self.verticalSlider_Max<file.layer:
            self.verticalSlider_Max=file.layer-1
        self.verticalSlider.setMaximum(self.verticalSlider_Max)
        self.listWidget.addItem((f[0].split('/'))[-1].split('.')[0])'''
        
        
    def redraw(self):
        self.lineEdit.setText(str(self.verticalSlider.value()))
        self.widget.layerindex=self.verticalSlider.value()
        self.widget.update()
    def delete(self):
        self.listWidget.clear()
        self.widget.data.clear()
        self.widget.update()
app=QtWidgets.QApplication(sys.argv)
mywindow=Ui_Read_cli()
mywindow.show()
app.exec_()
sys.exit()
