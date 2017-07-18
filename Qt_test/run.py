class QtConnector:
	'''
	Use this class to add logic and functionalities to a Qt widget template.
	It provides a standard __init__() and run() methods and a dummy connect().

	How to use:
		1) Define a child class inheriting from QtConnector

		2) Add an __init__ method with "QtConnector.__init__(self, template)"
		   to link the connector to the template

		3) Write your own connect() method and extra functions.


	Example:

		import sys
		import random
		from PyQt5 import QtCore, QtGui, QtWidgets

		#import the template generated using pyuic5
		from mywidget import MyWidget  

		#define your app
		class StartPage(QtConnector):

			def __init__(self):
				#link the connector to the template
				QtConnector.__init__(self, MyWidget) 

			#connect the gui
			def connect(self):
				self.ui.pushButton.clicked.connect(self.f)
			
			#add custom funcs and logic
			def f(self):
				print('clicked')
				self.ui.textBrowser.append(str(random.random()))
				if random.random() > 0.5:
					self.ui.textBrowser.setText('')
					print('cleaned')


		StartPage().run()
	'''

	def __init__(self, Widget):
		self.app = QtWidgets.QApplication(sys.argv)
		self.window = QtWidgets.QDialog()
		self.ui = Widget()
		self.ui.setupUi(self.window)

	def connect(self):
		pass

	def run(self):
		self.connect()
		self.window.show()
		sys.exit(self.app.exec_())