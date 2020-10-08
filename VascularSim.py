import sqlite3 as sql

import numpy as np
import pyqtgraph as pg
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Artery_Model import main


data1 = np.empty(5000)
ptr1 = 0


class Window(object):

    def __init__(self, MainWindow):
        super().__init__()
        self.MainWindow = MainWindow
        self.centralwidget = QWidget(MainWindow)
        self.mainlayout = QGridLayout(self.centralwidget)
        self.menubar = QMenuBar(self.MainWindow)
        
        self.playbtn = QPushButton(self.centralwidget) 
        self.stopbtn = QPushButton(self.centralwidget)

        self.hlayout = QVBoxLayout()
        self.btn = QPushButton(self.centralwidget)
        self.btn1 = QPushButton(self.centralwidget)
        self.btn2 = QPushButton(self.centralwidget)
        self.btn3 = QPushButton(self.centralwidget)
        self.btn4 = QPushButton(self.centralwidget)
        self.btn5 = QPushButton(self.centralwidget)
        self.btn6 = QPushButton(self.centralwidget)
        self.btn7 = QPushButton(self.centralwidget)
        self.btn8 = QPushButton(self.centralwidget)
        self.btn9 = QPushButton(self.centralwidget)

        self.timer = QTimer()
        self.setupUi()

    def setupUi(self):
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.setWindowTitle("VascularSim")
        self.MainWindow.setWindowIcon(QIcon('./VascularSim.ico'))
        self.MainWindow.resize(1200,800)
        self.MainWindow.setCentralWidget(self.centralwidget)
        self.MainWindow.setStyleSheet("background-color:rgb(30,30,30);")
        self.MainWindow.setCentralWidget(self.centralwidget)

        self.playbtn.clicked.connect(self.run)
        self.mainlayout.addWidget(self.playbtn, 0,1,1,1)
        self.stopbtn.clicked.connect(self.stop)
        self.mainlayout.addWidget(self.stopbtn, 0,3,1,1)

        self.hlayout.addWidget(self.btn)
        self.hlayout.addWidget(self.btn1)
        self.hlayout.addWidget(self.btn2)
        self.hlayout.addWidget(self.btn3)
        self.hlayout.addWidget(self.btn4)
        self.hlayout.addWidget(self.btn5)
        self.hlayout.addWidget(self.btn6)
        self.hlayout.addWidget(self.btn7)
        self.hlayout.addWidget(self.btn8)
        self.hlayout.addWidget(self.btn9)

        self.mainlayout.addLayout(self.hlayout, 1,0,1,1)
        
        # ______________________________GRAPH_WIDGET - 1 _____________________________
        # ============GRAPH -1
        pg.setConfigOptions(antialias= True, background=QColor(30,30,30,255))
        plotwin = pg.GraphicsLayoutWidget(show=True)
        p1 = plotwin.addPlot()
        p1.setDownsampling(mode='peak')
        p1.setClipToView(True)
        p1.setRange(xRange=[0, 3000])
        p1.setLimits(xMax=0)
        p1.setLabel('left', text='x axis')
        p1.setLabel('bottom', text='y axis')
        self.curve1 = p1.plot()
        self.curve1.setPen('g')  ## white pen
        self.curve1.setShadowPen(pg.mkPen((70,70,30), width=6, cosmetic=True))
        
        #self.plotWidget_1.setLabel('left', text='x axis', **self.labelStyle )
        #self.plotWidget_1.setLabel('bottom', text='y axis', **self.labelStyle )

        self.mainlayout.addWidget(plotwin, 1, 1, 1, 4)

        # -------------------------------MENUBAR
        self.menubar.setObjectName("menubar")

        # ============File Menu
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName("menuMenu")

        # ============View
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName("menuOptions")

        # ============Run
        self.menuRun = QMenu(self.menubar)
        self.menuRun.setObjectName("menuHelp")

        # ============Help
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp_2")

        self.MainWindow.setMenuBar(self.menubar)
        
        # _____________________________Action_Declaration________________________________

        self.actionClear =  QAction(self.MainWindow)
        self.actionClear.setObjectName("actionQuit")

        self.actionQuit =  QAction(self.MainWindow)
        self.actionQuit.setObjectName("actionQuit")

        # ________________________________Action_Adding_________________________________
        self.menuFile.addAction(self.actionClear)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.stylesheet()
        self.text()  

    def text(self):
        self.btn.setText("Ascending Aorta")
        self.btn1.setText("Aortic arch")
        self.btn2.setText("Subclavian")
        self.btn3.setText("Carotid")
        self.btn4.setText("Thoracic")
        self.btn5.setText("Cereberal")
        self.btn6.setText("Abdominal")
        self.btn7.setText("Brachial")
        self.btn8.setText("Ulnar")
        self.btn9.setText("Radial")

        self.playbtn.setText("Play")
        self.stopbtn.setText("Stop")

        self.menuFile.setTitle("File")
        self.menuView.setTitle( "View")
        self.menuRun.setTitle( "Run")
        self.menuHelp.setTitle( "Help")
        
        self.actionClear.setText( "Clear")
        self.actionQuit.setText("Quit")

    def stylesheet(self):
        self.centralwidget.setStyleSheet(""" 
            QPushButton{  background-color: rgb(60,60,60); color: rgb(240,240,240); } """)
        self.menubar.setStyleSheet("background-color: rgb(60,60,60); color: rgb(240,240,240); ")
        #self.centralwidget.setStyleSheet()

    def update(self):
        global data1, ptr1

        def retrieve():
            i = str(ptr1 + 1)
            connection = sql.connect("vascularsim.db")
            cursor = connection.cursor()
            cursor.execute('SELECT "one" FROM BUFFER WHERE ID =' + i )
            rows = cursor.fetchone()
            connection.close()
            return rows[0]

        data1[ptr1] = retrieve()
        ptr1 += 1

        if ptr1 >= data1.shape[0]:
            tmp = data1
            data1 = np.empty(data1.shape[0] * 2)
            data1[:tmp.shape[0]] = tmp

        self.curve1.setData(data1[:ptr1])
        self.curve1.setPos(-ptr1+3050, 0)
        #curve4.setData(data3[:ptr3])


    def run(self):
        #main.main()

        connection = sql.connect("vascularsim.db")
        cursor = connection.cursor()
        cursor.execute("SELECT FLAG FROM HPN WHERE ID = 1")
        rows = cursor.fetchone()
        connection.close()
        
        print(rows)

        if rows[0] == 1:
            self.timer.timeout.connect(self.update)
            self.timer.start(1)

    def stop(self):
        self.timer.stop()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    wid = QMainWindow()
    ui = Window(wid)
    wid.show()
    sys.exit(app.exec())    

