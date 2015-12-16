import functions
import os
import threading
import sys

from PyQt4 import QtCore, QtGui, uic

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

ui = uic.loadUiType(__location__ + "/OBD2/mainwindow.ui")[0]


def refresh():



	def jank():
		functions.scan()
		window.update_values()
		threading.Timer(0.1, jank).start()

	jank()

class gui(QtGui.QMainWindow, ui):
	
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.setupUi(self)
		self.pushButton_13.clicked.connect(refresh)
		self.pushButton_14.clicked.connect(self.read_fault_codes)
		self.pushButton_10.clicked.connect(functions.clear_fault_codes)
		
	
	def update_values(self):
		self.rpm.setText(str(fucntions.data.rpm))
		self.rpm2.setText(str(fucntions.data.rpm))
		self.speed.setText(str(fucntions.data.speed))
		self.speed2.setText(str(fucntions.data.speed))
		self.intake_temp.setText(str(fucntions.data.intake_temp))
		self.oil_temp.setText(str(fucntions.data.oil_temp))
		self.coolant_temp.setText(str(fucntions.data.coolant_temp))
		self.current_torque.setText(str(fucntions.data.torque))
		self.current_power.setText(str(fucntions.data.power))
		self.max_torque.setText(str(fucntions.data.max_torque))
		self.max_power.setText(str(fucntions.data.max_power))
	
	def read_fault_codes(self):
		self.codes.setText(functions.get_fault_codes())
	
	
		
app = QtGui.QApplication(sys.argv)
window = gui(None)
window.show()
app.exec_()




 
