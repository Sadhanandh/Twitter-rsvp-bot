import sys
import os
import re
import opener
from PySide import QtGui
from PySide import QtCore

mins = 10
us_name = "."
settingsfile = os.path.join("images","settings.ini")
if os.path.exists(settingsfile):
    fr = open(settingsfile)
    data = fr.read()
    ma = re.findall("Loop\s*Timer\s*:\s*(\S*)",data,re.IGNORECASE)
    if ma != []:
        mins = float(ma[0])
	ma = re.findall("XML\s*Location\s*:\s*(.*)",data,re.IGNORECASE)
    if ma != []:
        us_name = ma[0]

class SystemTrayIcon(QtGui.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtGui.QMenu(parent)
        exitAction = menu.addAction("Exit")
        exitAction.triggered.connect(sys.exit)
        self.setContextMenu(menu)
        self.ctimer = QtCore.QTimer()
        self.ctimer.start(1000*60*mins)
        self.ctimer.timeout.connect(self.runner)

    def runner(self,us_name):
		opener.mainer(us_name)
        

def main():
    app = QtGui.QApplication(sys.argv)

    w = QtGui.QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon(os.path.join("images","fb.ico")), w)
    trayIcon.show()
    trayIcon.showMessage(u'Xmlrunner',u'Searching for XML files... ',Icon="Information",msecs=10)
    trayIcon.runner(us_name)
		
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
