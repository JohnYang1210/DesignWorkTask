import sys
from PyQt5.QtWidgets import QApplication,QMainWindow
from kml import Ui_MainWindow
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
class MyMainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):

        super(MyMainWindow,self).__init__(parent)
        self.setupUi(self)

if __name__=='__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app=QApplication(sys.argv)
    myWin=MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())