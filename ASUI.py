#ASUI

# http://noobtuts.com/python/opengl-introduction
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import main
import settings

class sliderdemo(QWidget):
   def __init__(self, parent = None):
      super(sliderdemo, self).__init__(parent)

      self.button = QPushButton('Toggle Curve Split', self)
      self.button.clicked.connect(self.handleButton)

      self.clearButton = QPushButton('Clear', self)
      self.clearButton.clicked.connect(self.handleClearButton)

      layout = QVBoxLayout()
      self.l1 = QLabel("t = 0.5")
      self.l1.setAlignment(Qt.AlignCenter)
      layout.addWidget(self.l1)
      layout.addWidget(self.clearButton)
      layout.addWidget(self.button)

      self.sl = QSlider(Qt.Horizontal)
      self.sl.setMinimum(0)
      self.sl.setMaximum(1000)
      self.sl.setValue(500)
      self.sl.setTickPosition(QSlider.TicksBelow)
      self.sl.setTickInterval(5)
        
      layout.addWidget(self.sl)
      self.sl.valueChanged.connect(self.valuechange)

      self.ipSlider = QSlider(Qt.Horizontal)
      self.ipSlider.setMinimum(10)
      self.ipSlider.setMaximum(1000)
      self.ipSlider.setValue(50)
      self.ipSlider.setTickPosition(QSlider.TicksBelow)
      self.ipSlider.setTickInterval(5)
        
      layout.addWidget(self.ipSlider)
      self.ipSlider.valueChanged.connect(self.ipSliderValueChange)

      self.setLayout(layout)
      # self.setWindowTitle("SpinBox demo")

   def handleButton(self):
      settings.splitLine = not splitLine
      main.draw()

   def handleClearButton(self):
      settings.points = []
      main.draw()

   def valuechange(self):
      value = float(self.sl.value())/1000
      self.l1.setText("t = " + str(value))
      settings.selectedT = value
      main.draw()

   def ipSliderValueChange(self):
      settings.interpolationNumber = self.ipSlider.value()
      main.draw()
