import pyqtgraph as pg
from PyQt5 import QtCore, QtGui
import numpy as np
import sys
import sqlite3 as sql
import time
import itertools

win = pg.GraphicsLayoutWidget(show=True)
win.setWindowTitle('pyqtgraph example: Scrolling Plots')

p3 = win.addPlot()
p3.setDownsampling(mode='peak')
p3.setClipToView(True)
p3.setRange(xRange=[0, 3000])
#p3.setLimits(xMax=0)

curve3 = p3.plot()
curve3.setPen('g')
data3 = np.empty(3000)
ptr3 = 0
i = [1,1]

def update2():
    global data3, ptr3, i

    def retrieve():
        connection = sql.connect("vascularsim.db")
        cursor = connection.cursor()
        cursor.execute('SELECT "one" FROM BUFFER WHERE ID BETWEEN ' + str(i[0]) + ' AND ' + str(i[1] * 10 ) )
        rows = cursor.fetchall()
        connection.close()
        i[0] = i[0] + 10
        out = [item for t in rows for item in t]
        
        return out

    if ptr3 >= data3.shape[0]:
        temp = data3[10:]
        val = retrieve()
        data3 = np.append(temp, val)
             
        curve3.setData(data3)
        ptr3 += 10
        i[1] += 1
        
    else:
        val = retrieve()
        data3[ptr3 : i[1]*10] = val[0:10]
        curve3.setData(data3[: i[1]*10])
        ptr3 += 10
        i[1] += 1
        

def update():
    update2()

input()

timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(10)


if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
'''

start = time.time()
connection = sql.connect("vascularsim.db")
cursor = connection.cursor()

cursor.execute('SELECT "one" FROM BUFFER WHERE ID BETWEEN 1 AND 5' )
rows = cursor.fetchall()
out= [item for t in rows for item in t]
print("one: ",out)
#out = list(sum(rows, ()))

cursor.execute('SELECT "twelve" FROM BUFFER WHERE ID BETWEEN 1 AND 5' )
rows = cursor.fetchall()
out= [item for t in rows for item in t]
print("twelve: ",out)
#out = list(itertools.chain(*rows))

connection.close()
end = time.time()
print("time taken: ", end-start)
'''