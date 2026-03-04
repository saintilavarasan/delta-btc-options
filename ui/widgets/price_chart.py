import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from pyqtgraph import PlotWidget, plot
import numpy as np

class PriceChart(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Interactive Option Price Chart'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 800, 600)

        # Create plot widget
        self.plotWidget = PlotWidget()
        self.setCentralWidget(self.plotWidget)

        # Generate some sample data
        x = np.linspace(0, 10, 100)
        y = np.sin(x)

        # Plot data
        self.plotWidget.plot(x, y)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = PriceChart()
    mainWin.show()
    sys.exit(app.exec_())