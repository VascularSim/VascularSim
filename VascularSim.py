import sqlite3 as sql

import numpy as np
import threading
import pyqtgraph as pg
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import subprocess

#from Artery_Model import main
from Artery_Model import queries

data1 = np.empty(3000)
data2 = np.empty(3000)
data3 = np.empty(3000)
data4 = np.empty(3000)
ptr1 = 0
index = [1, 1]

class Window(object):

    def __init__(self, MainWindow):
        super().__init__()
        self.MainWindow = MainWindow
        self.centralwidget = QWidget(MainWindow)
        
        self.menubar = QMenuBar(self.MainWindow)

        # LAYOUTSs
        self.mainlayout = QGridLayout(self.centralwidget)
        self.grlayout = QGridLayout()

        # LABEL
        self.hrlabel = QLabel(self.centralwidget)
        self.sbplabel = QLabel(self.centralwidget)
        self.dbplabel = QLabel(self.centralwidget)
        self.flowlabel = QLabel(self.centralwidget)

        # BUTTONS
        self.playbtn = QPushButton(self.centralwidget) 
        self.stopbtn = QPushButton(self.centralwidget)
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

        # TEXTBOX
        self.hrbox = QLineEdit(self.centralwidget)
        self.sbpbox = QLineEdit(self.centralwidget)
        self.dbpbox = QLineEdit(self.centralwidget)
        self.flowbox = QLineEdit(self.centralwidget)
        
        # TIMER
        self.timer = QTimer()

        queries.query()
        
        self.setupUi()

    def __del__(self):
        os.system('taskkill /f /im main.exe')
        #os.kill('main.exe')

    def setupUi(self):
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.setWindowTitle("VascularSim")
        self.MainWindow.setWindowIcon(QIcon('./VascularSim.ico'))
        self.MainWindow.resize(1200,800)

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.MainWindow.sizePolicy().hasHeightForWidth())
        self.MainWindow.setSizePolicy(sizePolicy)

        #CENTRAL WIDGET
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.MainWindow.setCentralWidget(self.centralwidget)

        # LEFT SIDE
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        sizePolicy.setHeightForWidth(self.btn.sizePolicy().hasHeightForWidth())
        self.btn.setSizePolicy(sizePolicy)
        self.btn.setMaximumSize(QSize(207, 1677))
        self.mainlayout.addWidget(self.btn, 1, 0, 1, 1)

        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn1.sizePolicy().hasHeightForWidth())
        self.btn1.setSizePolicy(sizePolicy)
        self.btn1.setMaximumSize(QSize(207, 1677))
        self.mainlayout.addWidget(self.btn1, 2, 0, 1, 1)

        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn2.sizePolicy().hasHeightForWidth())
        self.btn2.setSizePolicy(sizePolicy)
        self.btn2.setMaximumSize(QSize(207, 1677))
        self.mainlayout.addWidget(self.btn2, 3, 0, 1, 1)

        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn3.sizePolicy().hasHeightForWidth())
        self.btn3.setSizePolicy(sizePolicy)
        self.btn3.setMaximumSize(QSize(207, 1677))
        self.mainlayout.addWidget(self.btn3, 4, 0, 1, 1)
        
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn4.sizePolicy().hasHeightForWidth())
        self.btn4.setSizePolicy(sizePolicy)
        self.btn4.setMaximumSize(QSize(207, 1677))
        self.mainlayout.addWidget(self.btn4, 5, 0, 1, 1)

        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn5.sizePolicy().hasHeightForWidth())
        self.btn5.setSizePolicy(sizePolicy)
        self.btn5.setMaximumSize(QSize(207, 1677))
        self.mainlayout.addWidget(self.btn5, 6, 0, 1, 1)

        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn6.sizePolicy().hasHeightForWidth())
        self.btn6.setSizePolicy(sizePolicy)
        self.btn6.setMaximumSize(QSize(207, 1677))
        self.mainlayout.addWidget(self.btn6, 7, 0, 1, 1)

        sizePolicy.setHeightForWidth(self.btn7.sizePolicy().hasHeightForWidth())
        self.btn7.setSizePolicy(sizePolicy)
        self.btn7.setMaximumSize(QSize(207, 1677))
        self.mainlayout.addWidget(self.btn7, 8, 0, 1, 1)

        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn8.sizePolicy().hasHeightForWidth())
        self.btn8.setSizePolicy(sizePolicy)
        self.btn8.setMaximumSize(QSize(207, 1677))
        self.mainlayout.addWidget(self.btn8, 9, 0, 1, 1)

        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn9.sizePolicy().hasHeightForWidth())
        self.btn9.setSizePolicy(sizePolicy)
        self.btn9.setMaximumSize(QSize(207, 1677))
        self.mainlayout.addWidget(self.btn9, 10, 0, 1, 1)

        # CENTER
        # --------PLAY BUTTON
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.playbtn.sizePolicy().hasHeightForWidth())
        self.playbtn.setSizePolicy(sizePolicy)
        self.playbtn.clicked.connect(self.run)
        self.mainlayout.addWidget(self.playbtn, 0,1,1,1)

        # --------STOP BUTTON
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.stopbtn.sizePolicy().hasHeightForWidth())
        self.stopbtn.setSizePolicy(sizePolicy)
        self.stopbtn.clicked.connect(self.stop)
        self.mainlayout.addWidget(self.stopbtn, 0,2,1,1)

        # ______________________________GRAPH_WIDGET_____________________________
        # ============GRAPH
        pg.setConfigOptions(antialias= True, background=QColor(30,30,30,255))
        plotwin = pg.GraphicsLayoutWidget(show=True)

        p1 = plotwin.addPlot()
        p1.setDownsampling(mode='peak')
        p1.setClipToView(True)
        p1.setRange(xRange=[0, 3000])
        #p1.setLimits(xMax=0)
        p1.setLabel('left', text='y axis')
        p1.setLabel('bottom', text='x axis')
        self.curve1 = p1.plot()
        self.curve1.setPen('g')  ## white pen

        plotwin.nextRow()
        p2 = plotwin.addPlot()
        p2.setDownsampling(mode='peak')
        p2.setClipToView(True)
        p2.setRange(xRange=[0, 3000])
        p2.setLabel('left', text='y axis')
        p2.setLabel('bottom', text='x axis')
        self.curve2 = p2.plot()
        self.curve2.setPen('g')  ## white pen

        plotwin.nextRow()
        p3 = plotwin.addPlot()
        p3.setDownsampling(mode='peak')
        p3.setClipToView(True)
        p3.setRange(xRange=[0, 3000])
        p3.setLabel('left', text='y axis')
        p3.setLabel('bottom', text='x axis')
        self.curve3 = p3.plot()
        self.curve3.setPen('g')  ## white pen

        plotwin.nextRow()
        p4 = plotwin.addPlot()
        p4.setDownsampling(mode='peak')
        p4.setClipToView(True)
        p4.setRange(xRange=[0, 3000])
        p4.setLabel('left', text='y axis')
        p4.setLabel('bottom', text='x axis')
        self.curve4 = p4.plot()
        self.curve4.setPen('g')  ## white pen

        self.mainlayout.addWidget(plotwin, 1, 1, 10, 2)     

        # ---------------------GRLAYOUT
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hrlabel.sizePolicy().hasHeightForWidth())
        self.hrlabel.setSizePolicy(sizePolicy)
        self.hrlabel.setMaximumHeight(50)
        self.grlayout.addWidget(self.hrlabel, 0, 0, 1, 1 )

        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hrbox.sizePolicy().hasHeightForWidth())
        self.hrbox.setSizePolicy(sizePolicy)
        self.hrbox.setMaxLength(3)
        self.hrbox.setMaximumWidth(150)
        self.hrbox.setText("72")
        self.grlayout.addWidget(self.hrbox, 1, 0, 1, 1)

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sbplabel.sizePolicy().hasHeightForWidth())
        self.sbplabel.setSizePolicy(sizePolicy)
        self.sbplabel.setMaximumWidth(150)
        self.sbplabel.setMinimumHeight(30)
        self.grlayout.addWidget(self.sbplabel, 2, 0, 1, 1 )

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.sbpbox.setSizePolicy(sizePolicy)
        self.sbpbox.setMaximumWidth(150)
        self.sbpbox.setMaxLength(3)
        self.grlayout.addWidget(self.sbpbox, 3, 0, 1, 1)

        self.dbplabel.setMaximumWidth(150)
        self.dbplabel.setMaximumHeight(30)
        self.grlayout.addWidget(self.dbplabel, 2, 1, 1, 1)

        self.dbpbox.setMaximumWidth(150)
        self.dbpbox.setMaxLength(3)
        self.grlayout.addWidget(self.dbpbox, 3, 1, 1, 1)

        self.flowlabel.setMaximumHeight(30)
        self.flowlabel.setMaximumWidth(150)
        self.grlayout.addWidget(self.flowlabel, 4, 0, 1, 1)

        self.flowbox.setMaximumWidth(150)
        self.flowbox.setMaxLength(5)
        self.grlayout.addWidget(self.flowbox, 5, 0, 1, 1)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setSizeConstraint(QLayout.SetDefaultConstraint)

        self.label_5 = QLabel(self.centralwidget)
        self.grlayout.addWidget(self.label_5, 6, 0, 1, 1)

        self.label_7 = QLabel(self.centralwidget)
        self.gridLayout_3.addWidget(self.label_7, 1, 0, 1, 1)

        self.label_6 =QLabel(self.centralwidget)
        self.gridLayout_3.addWidget(self.label_6, 0, 0, 1, 1)

        self.label_8 = QLabel(self.centralwidget) 
        self.gridLayout_3.addWidget(self.label_8, 0, 1, 1, 1)

        self.label_9 = QLabel(self.centralwidget)
        self.gridLayout_3.addWidget(self.label_9, 1, 1, 1, 1)

        self.grlayout.addLayout(self.gridLayout_3, 8, 0, 2, 1)
        self.pushButton_13 = QPushButton(self.centralwidget)
        self.pushButton_13.setText('ok')
        self.grlayout.addWidget(self.pushButton_13, 8, 1, 2, 1)

        self.grid_patient_profile = QGridLayout()
        self.grid_patient_profile.setObjectName("grid_patient_profile")
        
        self.experimentlbl = QLabel(self.centralwidget)
        self.experimentlbl.setObjectName("experimentlbl")
        self.grid_patient_profile.addWidget(self.experimentlbl, 2, 0, 1, 1)
        
        self.patprof = QLabel(self.centralwidget)
        self.patprof.setObjectName("patprof")
        self.grid_patient_profile.addWidget(self.patprof, 0, 0, 1, 1)
        
        self.stenosis_lbl_top = QLabel(self.centralwidget)
        self.stenosis_lbl_top.setObjectName("stenosis_lbl_top")
        self.grid_patient_profile.addWidget(self.stenosis_lbl_top, 1, 0, 1, 1)
        
        self.valpatprof = QLabel(self.centralwidget)
        self.valpatprof.setObjectName("valpatprof")
        self.grid_patient_profile.addWidget(self.valpatprof, 0, 1, 1, 1)

        self.Valstenosis_lbl_top = QLabel(self.centralwidget)
        self.Valstenosis_lbl_top.setObjectName("Valstenosis_lbl_top")
        self.grid_patient_profile.addWidget(self.Valstenosis_lbl_top, 1, 1, 1, 1)
        
        self.Valexperimentlbl = QLabel(self.centralwidget)
        self.Valexperimentlbl.setObjectName("Valexperimentlbl")
        self.grid_patient_profile.addWidget(self.Valexperimentlbl, 2, 1, 1, 1)
        self.grlayout.addLayout(self.grid_patient_profile, 0, 1, 1, 1)

        self.sbpbox.setText("120")
        self.dbpbox.setText("80")
        self.flowbox.setText("450.0")

        self.mainlayout.addLayout(self.grlayout, 0,3,11,1)
        
        # ______________________________MENUBAR _____________________________
        # ============MENU BAR
        self.MainWindow.setMenuBar(self.menubar)

        # ============MENU FILE
        self.menuFile = QMenu(self.menubar)

        self.actionCreate_profile =QAction(self.MainWindow)
        self.actionSettings = QAction(self.MainWindow)
        self.actionQuit = QAction(self.MainWindow)

        self.menuFile.addAction(self.actionCreate_profile)
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addAction(self.actionQuit)
        
        # ============MENU SIMULATION
        self.menuSimulation = QMenu(self.menubar)      

        self.menuMedical_Experiments = QMenu(self.menuSimulation)
        self.actionEffect_of_POSTURE = QAction(self.MainWindow)
        self.actionEffect_of_muscular_exercise = QAction(self.MainWindow)
        self.menuMedical_Experiments.addAction(self.actionEffect_of_POSTURE)
        self.menuMedical_Experiments.addAction(self.actionEffect_of_muscular_exercise)

        self.actionHuman_arterial_tree = QAction(self.MainWindow)
        self.actionFoetal_Circulation = QAction(self.MainWindow)

        self.menuSimulation.addAction(self.actionHuman_arterial_tree)
        self.menuSimulation.addAction(self.actionFoetal_Circulation)
        self.menuSimulation.addAction(self.menuMedical_Experiments.menuAction())
        
        # ============MENU GRAPH
        self.menuGraph = QMenu(self.menubar)

        self.actionGraph_options = QAction(self.MainWindow)
        self.actionClear_all = QAction(self.MainWindow)
        self.actionReset_all = QAction(self.MainWindow)

        self.menuGraph.addAction(self.actionGraph_options)
        self.menuGraph.addAction(self.actionClear_all)
        self.menuGraph.addAction(self.actionReset_all)

        self.actionClear_graph = QAction(self.MainWindow)
        self.actionReset = QAction(self.MainWindow)
       
        self.actionGraph_5 = QAction(self.MainWindow)
        self.actionGraph_6 = QAction(self.MainWindow)
        self.actionGraph_7 = QAction(self.MainWindow)
        self.actionGraph_8 = QAction(self.MainWindow)

        self.menuClear = QMenu(self.menuGraph)
        self.actionGraph_1 = QAction(self.MainWindow)
        self.actionGraph_2 = QAction(self.MainWindow)
        self.actionGraph_3 = QAction(self.MainWindow)
        self.actionGraph_4 = QAction(self.MainWindow)

        self.menuClear.addAction(self.actionGraph_1)
        self.menuClear.addAction(self.actionGraph_2)
        self.menuClear.addAction(self.actionGraph_3)
        self.menuClear.addAction(self.actionGraph_4)

        self.menuGraph.addAction(self.menuClear.menuAction())

        # ============MENU ABOUT
        self.menuAbout = QMenu(self.menubar)

        self.actionHelp = QAction(self.MainWindow)
        self.actionUser_manual = QAction(self.MainWindow)
        self.actionAbout = QAction(self.MainWindow)
        self.actionDevelopers = QAction(self.MainWindow)

        self.menuAbout.addAction(self.actionHelp)
        self.menuAbout.addAction(self.actionUser_manual)
        self.menuAbout.addAction(self.actionAbout)
        self.menuAbout.addAction(self.actionDevelopers)
    
        self.menuFile.addSeparator()
        self.menuFile.addSeparator()
        self.menuSimulation.addSeparator()
        self.menuSimulation.addSeparator()
        self.menuGraph.addSeparator()
        self.menuGraph.addSeparator()
        self.menuAbout.addSeparator()
        self.menuAbout.addSeparator()

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSimulation.menuAction())
        self.menubar.addAction(self.menuGraph.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

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

        self.hrlabel.setText("Heart Rate")
        self.sbplabel.setText("SBP              mmHg")
        self.dbplabel.setText("DBP              mmHg")
        self.flowlabel.setText("Flow            ml/sec")

        self.patprof.setText("Patient Profile")
        self.stenosis_lbl_top.setText("stenosis")
        self.experimentlbl.setText("Experiment")

        self.menuFile.setTitle( "File")
        self.menuSimulation.setTitle( "Simulation")
        self.menuMedical_Experiments.setTitle( "Medical Experiments")
        self.menuGraph.setTitle( "Graph")
        self.menuClear.setTitle( "Clear")
        self.menuAbout.setTitle( "About")
        self.actionCreate_profile.setText( "Create profile")
        self.actionSettings.setText( "Settings")
        self.actionQuit.setText( "Quit")
        self.actionHuman_arterial_tree.setText( "Human arterial tree")
        self.actionFoetal_Circulation.setText( "Fetal Circulation")
        self.actionEffect_of_POSTURE.setText( "Effect of POSTURE")
        self.actionEffect_of_muscular_exercise.setText( "Effect of muscular exercise")
        self.actionClear_graph.setText( "Clear")
        self.actionReset.setText( "Reset")
        self.actionGraph_options.setText( "Graph options")
        self.actionClear_all.setText( "Clear all")
        self.actionReset_all.setText( "Reset")
        self.actionGraph_1.setText( "Graph - 1")
        self.actionGraph_2.setText( "Graph - 2")
        self.actionGraph_3.setText( "Graph - 3")
        self.actionGraph_4.setText( "Graph - 4")
        self.actionGraph_5.setText( "Graph - 1")
        self.actionGraph_6.setText( "Graph - 2")
        self.actionGraph_7.setText( "Graph - 3")
        self.actionGraph_8.setText( "Graph - 4")
        self.actionHelp.setText( "Help")
        self.actionUser_manual.setText( "User manual")
        self.actionAbout.setText( "About")
        self.actionDevelopers.setText( "Developers")

    def stylesheet(self):
        self.MainWindow.setStyleSheet(""" QMenuBar {  spacing: 4px;  } 
                                        QMainWindow{ background-color:rgb(30,30,30);   } """)

        self.menubar.setStyleSheet(" background-color: rgb(60,60,60); color: rgb(240,240,240); selection-color: white; selection-background-color: rgb(9,71,113); ")

        self.centralwidget.setStyleSheet(""" 
            QPushButton{  background-color: rgb(60,60,60); color: rgb(240,240,240);  font: bold 13px; }
            QLabel { color: rgb(240,240,240); font: bold 13px; } 
            """)

        self.hrlabel.setStyleSheet("background-color: rgb(30,30,30); height: 10")
        self.hrbox.setStyleSheet("background-color: rgb(30,30,30); border: 1px solid black; color: rgb(6, 247, 0); height: 90; font: 90px;")
        
        self.sbplabel.setStyleSheet("background-color: rgb(30,30,30); height: 10")
        self.sbpbox.setStyleSheet("background-color: rgb(30,30,30); border: 1px solid black; color: rgb(252, 2, 248); height: 90; font: 90px;")

        self.dbplabel.setStyleSheet("background-color: rgb(30,30,30); height: 10")
        self.dbpbox.setStyleSheet("background-color: rgb(30,30,30); border: 1px solid black; color: rgb(252, 2, 248); height: 90; font: 90px;")

        self.flowlabel.setStyleSheet("background-color: rgb(30,30,30); height: 10")
        self.flowbox.setStyleSheet("background-color: rgb(30,30,30); border: 1px solid black; color: rgb(255, 255, 255); height: 90; font: 59px;")

        self.patprof.setStyleSheet("background-color: rgb(30,30,30); height: 10; color: rgb(6, 247, 0);")
        self.valpatprof.setStyleSheet("image:url(C:/Users/arvin/Documents/GitHub/VascularSim/img/off.png);")

        self.experimentlbl.setStyleSheet("background-color: rgb(30,30,30); height: 10; color: rgb(6, 247, 0);")
        self.Valexperimentlbl.setStyleSheet("image:url(C:/Users/arvin/Documents/GitHub/VascularSim/img/off.png);")

        self.stenosis_lbl_top.setStyleSheet("background-color: rgb(30,30,30); height: 10; color: rgb(6, 247, 0);")
        self.Valstenosis_lbl_top.setStyleSheet("image:url(C:/Users/arvin/Documents/GitHub/VascularSim/img/off.png);")

    def update(self):
        global data1, data2, data3, data4, ptr1, index

        def retrieve():
            connection = sql.connect("vascularsim.db")
            cursor = connection.cursor()

            cursor.execute('SELECT "twelve" FROM BUFFER WHERE ID BETWEEN ' + str(index[0]) + ' AND ' + str(index[1] * 10 ) )
            rows = cursor.fetchall()
            ecg = [item for t in rows for item in t]

            cursor.execute('SELECT "one" FROM BUFFER WHERE ID BETWEEN ' + str(index[0]) + ' AND ' + str(index[1] * 10 ) )
            rows = cursor.fetchall()
            one = [item for t in rows for item in t]

            cursor.execute('SELECT "seven" FROM BUFFER WHERE ID BETWEEN ' + str(index[0]) + ' AND ' + str(index[1] * 10 ) )
            rows = cursor.fetchall()
            seven = [item for t in rows for item in t]

            cursor.execute('SELECT "nine" FROM BUFFER WHERE ID BETWEEN ' + str(index[0]) + ' AND ' + str(index[1] * 10 ) )
            rows = cursor.fetchall()
            nine = [item for t in rows for item in t]

            connection.close()
            index[0] = index[0] + 10
            
            return one, ecg, seven, nine

        connection = sql.connect("vascularsim.db")
        cursor = connection.cursor()
        cursor.execute("SELECT FLAG FROM HPN WHERE ID = 1")
        rows = cursor.fetchone()
        connection.close()

        if rows[0] == 1:
            
            if ptr1 >= data1.shape[0]:
                temp = data1[10:]
                temp1 = data2[10:]
                temp2 = data3[10:]
                temp3 = data4[10:]

                val, val1, val2, val3 = retrieve()
                data1 = np.append(temp, val)
                data2 = np.append(temp1, val1)
                data3 = np.append(temp2, val2)
                data4 = np.append(temp3, val3)

                self.curve1.setData(data2)
                self.curve2.setData(data1)
                self.curve3.setData(data3)
                self.curve4.setData(data4)
                ptr1 += 10
                index[1] += 1
            
            else:
                val, val1, val2, val3 = retrieve()
                data1[ptr1 : index[1]*10] = val[0:10]
                data2[ptr1 : index[1]*10] = val1[0:10]
                data3[ptr1 : index[1]*10] = val2[0:10]
                data4[ptr1 : index[1]*10] = val3[0:10]

                self.curve1.setData(data2[: index[1]*10])
                self.curve2.setData(data1[: index[1]*10])
                self.curve3.setData(data3[: index[1]*10])
                self.curve4.setData(data4[: index[1]*10])
                #self.curve1.setPos(-ptr1+3050, 0)
                ptr1 += 10
                index[1] += 1

    def arteryModel(self):
        try:
            path = os.path.join("Artery_Model", "main.exe")
            subprocess.Popen(path)
        except e as Exception:
            print(str(e))

    def plotMarker(self):
        self.timer.timeout.connect(self.update)
        self.timer.start(40)

    def run(self):
        self.arteryModel()
        self.plotMarker()

    def stop(self):
        self.timer.stop()

if __name__ == "__main__":
    import sys
    import os
    app = QApplication(sys.argv)
    wid = QMainWindow()
    ui = Window(wid)
    wid.show()
    sys.exit(app.exec())    


