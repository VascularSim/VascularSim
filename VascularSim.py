import sqlite3 as sql
import subprocess
from functools import partial
import itertools
from collections import deque

import numpy as np
import scipy.signal as signal
import pyqtgraph as pg
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import queries

speed = 20
data1 = np.empty(2000)
data2 = np.empty(2000)
data3 = np.empty(2000)
data4 = np.empty(2000)
ptr1 = 0
hr_index = [1, 1]
index = [1, 1]

graph_optn = ["twelve","one","seven","nine"]

rd_btn_val = 0

class Window(object):

    def __init__(self, MainWindow):
        super().__init__()
        self.MainWindow = MainWindow
        self.centralwidget = QWidget(MainWindow)
        
        self.menubar = QMenuBar(self.MainWindow)

        # LAYOUTSs
        self.mainlayout = QGridLayout(self.centralwidget)
        self.graph_optn_layout = QGridLayout()
        self.grlayout = QGridLayout()

        # LABEL
        self.hrlabel = QLabel(self.centralwidget)
        self.sbplabel = QLabel(self.centralwidget)
        self.dbplabel = QLabel(self.centralwidget)
        self.flowlabel = QLabel(self.centralwidget)

        # RADIO BUTTONS
        self.graph1_optn = QRadioButton(self.centralwidget)
        self.graph2_optn = QRadioButton(self.centralwidget)
        self.graph3_optn = QRadioButton(self.centralwidget)
        self.graph4_optn = QRadioButton(self.centralwidget)



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

        self.xdata =  deque(maxlen=2000)
        
        self.setupUi()

    def setupUi(self):
        
        self.btn_list = [ self.btn, self.btn1, self.btn2, self.btn3, self.btn4, self.btn5, self.btn6, self.btn7, self.btn8, self.btn9 ] 

        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.setWindowTitle("VascularSim")
        self.MainWindow.setWindowIcon(QIcon('./VascularSim.ico'))
        self.MainWindow.resize(1200,650)
        self.MainWindow.setMaximumHeight(650)
        self.MainWindow.setMaximumWidth(1200)
        
        #CENTRAL WIDGET
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.MainWindow.setCentralWidget(self.centralwidget)

        # LEFT SIDE BUTTONS
        def gup(btn_name):
            global graph_optn
            
            if rd_btn_val == 1:
                for i in self.btn_list:
                    if i.styleSheet().split(" ")[1] == "rgb(0,150,255)":
                        i.setStyleSheet("background-color: rgb(60,60,60)")
                                       
                
                if btn_name == 0:
                    self.btn.setStyleSheet("background-color: rgb(0,150,255)"   )
                    graph_optn[1] = "one"

                elif btn_name == 1:
                    self.btn1.setStyleSheet("background-color: rgb(0,150,255)"   )
                    graph_optn[1] = "two"

                elif btn_name == 2:
                    self.btn2.setStyleSheet("background-color: rgb(0,150,255)"   )
                    graph_optn[1] = "three"

                elif btn_name == 3:
                    self.btn3.setStyleSheet("background-color: rgb(0,150,255)"   )
                    graph_optn[1] = "four"

                elif btn_name == 4:
                    self.btn4.setStyleSheet("background-color: rgb(0,150,255)"   )
                    graph_optn[1] = "five"

                elif btn_name == 5:
                    self.btn5.setStyleSheet("background-color: rgb(0,150,255)"   )
                    graph_optn[1] = "six"

                elif btn_name == 6:
                    self.btn6.setStyleSheet("background-color: rgb(0,150,255)"   )
                    graph_optn[1] = "seven"

                elif btn_name == 7:
                    self.btn7.setStyleSheet("background-color: rgb(0,150,255)"   )
                    graph_optn[1] = "eight"

                elif btn_name == 8:
                    self.btn8.setStyleSheet("background-color: rgb(0,150,255)"   )
                    graph_optn[1] = "nine"

                elif btn_name == 9:
                    self.btn9.setStyleSheet("background-color: rgb(0,150,255)"   )
                    graph_optn[1] = "ten"

            elif rd_btn_val == 2:
                
                for i in self.btn_list:
                    if i.styleSheet().split(" ")[1] == "rgb(252,2,248)":
                        i.setStyleSheet("background-color: rgb(60,60,60)")
                
                if btn_name == 0:
                    self.btn.setStyleSheet("background-color: rgb(252,2,248)"   )
                    graph_optn[rd_btn_val] = "one"

                elif btn_name == 1:
                    self.btn1.setStyleSheet("background-color: rgb(252,2,248)"   )
                    graph_optn[rd_btn_val] = "two"

                elif btn_name == 2:
                    self.btn2.setStyleSheet("background-color: rgb(252,2,248)"   )
                    graph_optn[rd_btn_val] = "three"
                
                elif btn_name == 3:
                    self.btn3.setStyleSheet("background-color: rgb(252,2,248)"   )
                    graph_optn[rd_btn_val] = "four"

                elif btn_name == 4:
                    self.btn4.setStyleSheet("background-color: rgb(252,2,248)"   )
                    graph_optn[rd_btn_val] = "five"

                elif btn_name == 5:
                    self.btn5.setStyleSheet("background-color: rgb(252,2,248)"   )
                    graph_optn[rd_btn_val] = "six"

                elif btn_name == 6:
                    self.btn6.setStyleSheet("background-color: rgb(252,2,248)"   )
                    graph_optn[rd_btn_val] = "seven"

                elif btn_name == 7:
                    self.btn7.setStyleSheet("background-color: rgb(252,2,248)"   )
                    graph_optn[rd_btn_val] = "eight"

                elif btn_name == 8:
                    self.btn8.setStyleSheet("background-color: rgb(252,2,248)"   )
                    graph_optn[rd_btn_val] = "nine"

                elif btn_name == 9:
                    self.btn9.setStyleSheet("background-color: rgb(252,2,248)"   )
                    graph_optn[rd_btn_val] = "ten"

            elif rd_btn_val == 3:

                for i in self.btn_list:
                    if i.styleSheet().split(" ")[1] == "rgb(200,200,0)":
                        i.setStyleSheet("background-color: rgb(60,60,60)")

                if btn_name == 0:
                    self.btn.setStyleSheet("background-color: rgb(200,200,0)" )
                    graph_optn[rd_btn_val] = "one"

                elif btn_name == 1:
                    self.btn1.setStyleSheet("background-color: rgb(200,200,0)" )
                    graph_optn[rd_btn_val] = "two"

                elif btn_name == 2:
                    self.btn2.setStyleSheet("background-color: rgb(200,200,0)" )
                    graph_optn[rd_btn_val] = "three"

                elif btn_name == 3:
                    self.btn3.setStyleSheet("background-color: rgb(200,200,0)" )
                    graph_optn[rd_btn_val] = "four"

                elif btn_name == 4:
                    self.btn4.setStyleSheet("background-color: rgb(200,200,0)" )
                    graph_optn[rd_btn_val] = "five"

                elif btn_name == 5:
                    self.btn5.setStyleSheet("background-color: rgb(200,200,0)" )
                    graph_optn[rd_btn_val] = "six"

                elif btn_name == 6:
                    self.btn6.setStyleSheet("background-color: rgb(200,200,0)" )
                    graph_optn[rd_btn_val] = "seven"

                elif btn_name == 7:
                    self.btn7.setStyleSheet("background-color: rgb(200,200,0)" )
                    graph_optn[rd_btn_val] = "eight"

                elif btn_name == 8:
                    self.btn8.setStyleSheet("background-color: rgb(200,200,0)" )
                    graph_optn[rd_btn_val] = "nine"

                elif btn_name == 9:
                    self.btn9.setStyleSheet("background-color: rgb(200,200,0)" )
                    graph_optn[rd_btn_val] = "ten"

        def sizepolicy(obj):
            sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(obj.sizePolicy().hasHeightForWidth())
            obj.setSizePolicy(sizePolicy)
            obj.setMaximumSize(QSize(207, 1677))

        sizepolicy(self.btn)
        self.btn.clicked.connect( partial(gup, 0) ) 
        self.mainlayout.addWidget(self.btn, 2, 0, 1, 1)
        
        sizepolicy(self.btn1)
        self.btn1.clicked.connect( partial(gup, 1) )         
        self.mainlayout.addWidget(self.btn1, 3, 0, 1, 1)

        sizepolicy(self.btn2)
        self.btn2.clicked.connect( partial(gup, 2) ) 
        self.mainlayout.addWidget(self.btn2, 4, 0, 1, 1)

        sizepolicy(self.btn3)
        self.btn3.clicked.connect( partial(gup, 3) ) 
        self.mainlayout.addWidget(self.btn3, 5, 0, 1, 1)

        sizepolicy(self.btn4)
        self.btn4.clicked.connect( partial(gup, 4) ) 
        self.mainlayout.addWidget(self.btn4, 6, 0, 1, 1)

        sizepolicy(self.btn5)
        self.btn5.clicked.connect( partial(gup, 5) ) 
        self.mainlayout.addWidget(self.btn5, 7, 0, 1, 1)

        sizepolicy(self.btn6)
        self.btn6.clicked.connect( partial(gup, 6) ) 
        self.mainlayout.addWidget(self.btn6, 8, 0, 1, 1)
        
        sizepolicy(self.btn7)
        self.btn7.clicked.connect( partial(gup, 7) ) 
        self.mainlayout.addWidget(self.btn7, 9, 0, 1, 1)

        sizepolicy(self.btn8)
        self.btn8.clicked.connect( partial(gup, 8) )
        self.mainlayout.addWidget(self.btn8, 10, 0, 1, 1)

        sizepolicy(self.btn9)
        self.btn9.clicked.connect( partial(gup, 9) ) 
        self.mainlayout.addWidget(self.btn9, 11, 0, 1, 1)

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
        def set_Graph_optn(obj):
            obj.setLabel('bottom', text='(ms)')
            obj.setDownsampling(mode='peak')
            obj.setClipToView(True)
            obj.getAxis('bottom').setScale(2)
            obj.getAxis('bottom').setTickSpacing(1000, 10)
            obj.showGrid(x=True, y=True, alpha=0.3)
            obj.setRange(xRange=[0, 3000])
        
        pg.setConfigOptions(antialias= True, background=QColor(30,30,30,255))
        plotwin = pg.GraphicsLayoutWidget(show=True)
        plotwin.setContentsMargins(0, 0, 0, 0)

        self.p1 = plotwin.addPlot()
        set_Graph_optn(self.p1)
        self.curve1 = self.p1.plot()
        self.curve1.setPen('g')  ## Green pen

        plotwin.nextRow()
        self.p2 = plotwin.addPlot()
        set_Graph_optn(self.p2)
        self.curve2 = self.p2.plot()
        self.curve2.setPen('#0096ff')  ## Blue pen

        plotwin.nextRow()
        self.p3 = plotwin.addPlot()
        set_Graph_optn(self.p3)
        self.curve3 = self.p3.plot()
        self.curve3.setPen('#fc02f8')  ## Pink pen

        plotwin.nextRow()
        self.p4 = plotwin.addPlot()
        set_Graph_optn(self.p4)
        self.curve4 = self.p4.plot()
        self.curve4.setPen('y')  ## Yellow pen
        
        self.p1.hideAxis('bottom')
        self.p3.hideAxis('bottom')
        self.p4.hideAxis('bottom')
        
        self.mainlayout.addWidget(plotwin, 2, 1, 10, 2)  

        def radiobtnval(type):
            global rd_btn_val
            if type == "r1":
                rd_btn_val = 0
            elif type == "r2":
                rd_btn_val = 1
            elif type == "r3":
                rd_btn_val = 2
            else:
                rd_btn_val = 3
        
        self.graph1_optn.setText("GRAPH 1")
        self.graph_optn_layout.addWidget(self.graph1_optn, 1, 1 )
        self.graph1_optn.clicked.connect(partial(radiobtnval, "r1" ))

        self.graph2_optn.setText("GRAPH 2")
        self.graph_optn_layout.addWidget(self.graph2_optn, 1, 2)
        self.graph2_optn.clicked.connect(partial(radiobtnval, "r2" ))

        self.graph3_optn.setText("GRAPH 3")
        self.graph_optn_layout.addWidget(self.graph3_optn, 1, 3)
        self.graph3_optn.clicked.connect(partial(radiobtnval, "r3" ))

        self.graph4_optn.setText("GRAPH 4")
        self.graph_optn_layout.addWidget(self.graph4_optn, 1, 4)
        self.graph4_optn.clicked.connect(partial(radiobtnval, "r4" ))

        self.mainlayout.addLayout(self.graph_optn_layout, 1, 1, 1, 2)
        

        # ---------------------GRLAYOUT
        inner_glayout = QGridLayout()
        self.grlayout.addLayout(inner_glayout, 1, 0, 1, 1)

        def HR_update():
            global index
            connection = sql.connect("vascularsim.db")
            cursor = connection.cursor()
            cursor.execute('UPDATE HPN SET HR = ' + self.hrbox.text() + ', PF = ' +  self.flowbox.text() + ' WHERE id = 1')

            if self.process_exists('main.exe'):
                os.system('taskkill /f /im main.exe')
            
            subprocess.Popen("./main/main.exe",shell=False,close_fds=False)
            index = [1, 1]
                        
            connection.commit()
            connection.close()
            self.alert(" UPDATED     ")

        self.hrlabel.setMaximumHeight(50)
        self.hrbox.setMaxLength(3)
        self.hrbox.setMaximumWidth(150)
        self.hrbox.setText("60")
        
        self.hrbox.returnPressed.connect(HR_update)
        inner_glayout.addWidget(self.hrlabel, 0, 0)
        inner_glayout.addWidget(self.hrbox, 1, 0)

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
        self.flowbox.returnPressed.connect(HR_update)
        self.grlayout.addWidget(self.flowbox, 5, 0, 1, 1)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setSizeConstraint(QLayout.SetDefaultConstraint)

        dummy = QLabel(self.centralwidget)
        self.gridLayout_3.addWidget(dummy, 0, 0, 1, 1)

        dt_layout = QGridLayout()
        dt_hlayout = QVBoxLayout()
        
        self.dt_label =QLabel(self.centralwidget)
        self.dt_label.setText("Pre-Ejection Period")
        self.dt_label_1 =QLabel(self.centralwidget)
        self.dt_label_1.setText("DT_1")
        self.dt_label_2 =QLabel(self.centralwidget)
        self.dt_label_2.setText("DT_2")
        self.dt_label_3 =QLabel(self.centralwidget)
        self.dt_label_3.setText("DT_3")

        dt_layout.addWidget(self.dt_label, 0, 0)
        dt_layout.addLayout(dt_hlayout, 1, 0)
        dt_hlayout.addWidget(self.dt_label_1)
        dt_hlayout.addWidget(self.dt_label_2)
        dt_hlayout.addWidget(self.dt_label_3)

        
        self.gridLayout_3.addLayout(dt_layout, 1, 0, 1, 1)

        pwv_layout = QGridLayout()
        pwv_hlayout = QVBoxLayout()

        self.pwv_label = QLabel(self.centralwidget)
        self.pwv_label.setText("Pulse Wave Velocity")
        self.pwv_label_1 = QLabel(self.centralwidget)
        self.pwv_label_1.setText("PWV_1")
        self.pwv_label_2 = QLabel(self.centralwidget)
        self.pwv_label_2.setText("PWV_2")
        self.pwv_label_3 = QLabel(self.centralwidget)
        self.pwv_label_3.setText("PWV_3")

        pwv_layout.addWidget(self.pwv_label, 0, 0)
        pwv_layout.addLayout(pwv_hlayout, 1, 0)
        pwv_hlayout.addWidget(self.pwv_label_1)
        pwv_hlayout.addWidget(self.pwv_label_2)
        pwv_hlayout.addWidget(self.pwv_label_3)
        
        self.gridLayout_3.addLayout(pwv_layout, 1, 1, 1, 1)

        self.label_8 = QLabel(self.centralwidget)
        self.gridLayout_3.addWidget(self.label_8, 2, 0, 1, 1)

        self.label_9 = QLabel(self.centralwidget)
        self.gridLayout_3.addWidget(self.label_9, 3, 0, 1, 1)

        self.label_10 = QLabel(self.centralwidget)
        self.gridLayout_3.addWidget(self.label_10, 4, 0, 1, 1)

        self.grlayout.addLayout(self.gridLayout_3, 6, 0, 1, 2)
        
        self.grid_patient_profile = QGridLayout()
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sbplabel.sizePolicy().hasHeightForWidth())

        self.patprof = QLabel(self.centralwidget)
        self.grid_patient_profile.addWidget(self.patprof, 1, 0, 1, 1)

        self.stenosis_lbl_top = QLabel(self.centralwidget)
        self.grid_patient_profile.addWidget(self.stenosis_lbl_top, 2, 0, 1, 1)

        self.experimentlbl = QLabel(self.centralwidget)
        self.grid_patient_profile.addWidget(self.experimentlbl, 3, 0, 1, 1)
        
        self.valpatprof = QLabel(self.centralwidget)
        self.grid_patient_profile.addWidget(self.valpatprof, 1, 1, 1, 1)

        self.Valstenosis_lbl_top = QLabel(self.centralwidget)
        self.grid_patient_profile.addWidget(self.Valstenosis_lbl_top, 2, 1, 1, 1)
        
        self.Valexperimentlbl = QLabel(self.centralwidget)
        self.grid_patient_profile.addWidget(self.Valexperimentlbl, 3, 1, 1, 1)
        self.grlayout.addLayout(self.grid_patient_profile, 1, 1, 1, 1)

        self.patprof.setSizePolicy(sizePolicy)
        self.stenosis_lbl_top.setSizePolicy(sizePolicy)
        self.experimentlbl.setSizePolicy(sizePolicy)
        self.valpatprof.setSizePolicy(sizePolicy)
        self.Valstenosis_lbl_top.setSizePolicy(sizePolicy)
        self.Valexperimentlbl.setSizePolicy(sizePolicy)

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

        
        for i in range(2000):
            self.xdata.append(i+1)
        
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

        self.sbpbox.setText("120")
        self.dbpbox.setText("80")
        self.flowbox.setText("450.0")

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
            QRadioButton{ color: rgb(240,240,240);  font: bold 13px; }  
            """)

        self.dt_label_1.setStyleSheet("color: rgb(0,150,255)")
        self.dt_label_2.setStyleSheet("color: rgb(252,2,248)")
        self.dt_label_3.setStyleSheet("color: rgb(200,200,0)")

        self.pwv_label_1.setStyleSheet("color: rgb(0,150,255)")
        self.pwv_label_2.setStyleSheet("color: rgb(252,2,248)")
        self.pwv_label_3.setStyleSheet("color: rgb(200,200,0)")

        self.btn.setStyleSheet("background-color: rgb(0,150,255)")
        self.btn1.setStyleSheet("background-color: rgb(60,60,60)")
        self.btn2.setStyleSheet("background-color: rgb(60,60,60)")
        self.btn3.setStyleSheet("background-color: rgb(60,60,60)")
        self.btn4.setStyleSheet("background-color: rgb(60,60,60)")
        self.btn5.setStyleSheet("background-color: rgb(60,60,60)")
        self.btn6.setStyleSheet("background-color: rgb(252,2,248)")
        self.btn7.setStyleSheet("background-color: rgb(60,60,60)")
        self.btn8.setStyleSheet("background-color: rgb(200,200,0)")
        self.btn9.setStyleSheet("background-color: rgb(60,60,60)")

        self.hrlabel.setStyleSheet("background-color: rgb(30,30,30); ")
        self.hrbox.setStyleSheet("background-color: rgb(30,30,30); border: 0px solid white ; color: rgb(6, 247, 0); font: 50px;")
        
        self.sbplabel.setStyleSheet("background-color: rgb(30,30,30); height: 10")
        self.sbpbox.setStyleSheet("background-color: rgb(30,30,30); border: 0px ; color: rgb(252, 2, 248); height: 50; font: 50px;")

        self.dbplabel.setStyleSheet("background-color: rgb(30,30,30); height: 10")
        self.dbpbox.setStyleSheet("background-color: rgb(30,30,30); border: 0px ; color: rgb(252, 2, 248); height: 50; font: 50px;")

        self.flowlabel.setStyleSheet("background-color: rgb(30,30,30); height: 10")
        self.flowbox.setStyleSheet("background-color: rgb(30,30,30); border: 0px ; color: rgb(255, 255, 255); height: 50; font: 49px;")

        self.patprof.setStyleSheet("background-color: rgb(30,30,30); height: 10; color: rgb(6, 247, 0);")
        self.valpatprof.setStyleSheet("image:url(./img/off.png);")

        self.experimentlbl.setStyleSheet("background-color: rgb(30,30,30); height: 10; color: rgb(6, 247, 0);")
        self.Valexperimentlbl.setStyleSheet("image:url(./img/off.png);")

        self.stenosis_lbl_top.setStyleSheet("background-color: rgb(30,30,30); height: 10; color: rgb(6, 247, 0);")
        self.Valstenosis_lbl_top.setStyleSheet("image:url(./img/off.png);")

    def update(self):
        global data1, data2, data3, data4, ptr1, index, graph_optn

         
        
        def retrieve():
            connection = sql.connect("vascularsim.db")
            cursor = connection.cursor()
            
            cursor.execute(' SELECT ' + graph_optn[0] + ' FROM BUFFER WHERE ID BETWEEN ' + str(index[0]) + ' AND ' + str(index[1] * 5 ) )
            rows = cursor.fetchall()
            zero = [item for t in rows for item in t]
            
            cursor.execute(' SELECT ' + graph_optn[1] + ' FROM BUFFER WHERE ID BETWEEN ' + str(index[0]) + ' AND ' + str(index[1] * 5 ) )
            rows = cursor.fetchall()
            one = [item for t in rows for item in t]
            
            cursor.execute(' SELECT ' + graph_optn[2] + ' FROM BUFFER WHERE ID BETWEEN ' + str(index[0]) + ' AND ' + str(index[1] * 5 ) )
            rows = cursor.fetchall()
            two = [item for t in rows for item in t]

            cursor.execute(' SELECT ' + graph_optn[3] + ' FROM BUFFER WHERE ID BETWEEN ' + str(index[0]) + ' AND ' + str(index[1] * 5 ) )
            rows = cursor.fetchall()
            three = [item for t in rows for item in t]

            connection.close()
            index[0] = index[0] + 5
        
            return one, zero, two, three
        
        connection = sql.connect("vascularsim.db")
        cursor = connection.cursor()
        cursor.execute("SELECT FLAG FROM HPN WHERE ID = 1")
        flag = cursor.fetchone()
        cursor.execute("SELECT N FROM HPN WHERE ID = 1")
        dt_flag = cursor.fetchone()
        connection.close()
        
        if flag[0] == 1:
            
            if index[1] == 2000:
                index[0] = 1
                index[1] = 1

            if ptr1 >= data1.shape[0]:
                self.p1.enableAutoRange()
                self.p2.enableAutoRange()
                self.p3.enableAutoRange()
                self.p4.enableAutoRange()
                temp = data1[5:]
                temp1 = data2[5:]
                temp2 = data3[5:]
                temp3 = data4[5:]

                val, val1, val2, val3 = retrieve()

                data1 = np.append(temp, val)
                data2 = np.append(temp1, val1)
                data3 = np.append(temp2, val2)
                data4 = np.append(temp3, val3)

                for t in range(5):
                    self.xdata.append(self.xdata[1999]+(1) )

                self.curve1.setData(data2)
                self.curve2.setData(x = self.xdata, y = data1)
                self.curve3.setData(data3)
                self.curve4.setData(x = self.xdata, y = data4)

                ptr1 += 5
                index[1] += 1

            else:
                val, val1, val2, val3 = retrieve()

                data1[ptr1 : index[1]*5] = val[0:5]
                data2[ptr1 : index[1]*5] = val1[0:5]
                data3[ptr1 : index[1]*5] = val2[0:5]
                data4[ptr1 : index[1]*5] = val3[0:5]
                try :
                    self.curve1.setData(data2[: index[1]*5])
                    self.curve2.setData(x = list(itertools.islice(self.xdata, 0, int(index[1]*5) )) , y = data1[: index[1]*5])
                    self.curve3.setData(data3[: index[1]*5])
                    self.curve4.setData(x = list(itertools.islice(self.xdata, 0, int(index[1]*5) )) , y = data4[: index[1]*5])
                #self.curve1.setPos(-ptr1+3050, 0)
                except Exception as e:
                    self.alert(str(e))
                ptr1 += 5
                index[1] += 1

        if dt_flag[0] == 0:
            print('Happy')
            connection = sql.connect("vascularsim.db")
            cursor = connection.cursor()
            cursor.execute(' SELECT ' + graph_optn[0] + ' FROM BUFFER WHERE ID BETWEEN ' + str(index[0]) + ' AND ' + str(index[1] * 5 ) )
            rows = cursor.fetchall()
            zero = [item for t in rows for item in t]
            connection.close()
        else:
            print('sad')

    def process_exists(self, process_name):
            call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
            output = subprocess.check_output(call).decode()
            last_line = output.strip().split('\r\n')[-1]
            return last_line.lower().startswith(process_name.lower())

    def run(self):
        global speed

        try:
            if self.process_exists('main.exe'):
                self.timer.start(speed)
                self.alert(" SIMULATING...    ")
            else:
                subprocess.Popen("./main/main.exe",shell=False,close_fds=False)
                self.timer.timeout.connect(self.update)
                self.timer.start(speed)
                self.alert(" SIMULATING...    ")
        except Exception as e:
            print(str(e))

    def stop(self):
        self.timer.stop()

    def alert(self, msg):
        alert = QMessageBox()
        alert.setWindowTitle("Alert!!")
        alert.setWindowFlag(Qt.AA_EnableHighDpiScaling | Qt.FramelessWindowHint)
        alert.setStyleSheet("background-color: rgb(60, 60, 60);\n" "color: rgb(240, 240, 240);\n")
        alert.setText(msg)
        alert.exec_()

if __name__ == "__main__":
    import os
    import sys

    def process_exists(process_name):
        call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
        output = subprocess.check_output(call).decode()
        last_line = output.strip().split('\r\n')[-1]
        return last_line.lower().startswith(process_name.lower())

    def exit():
        if process_exists('main.exe'):
            os.system('taskkill /f /im main.exe')
    
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(exit)
    wid = QMainWindow()
    ui = Window(wid)
    wid.show()
    sys.exit(app.exec())    


