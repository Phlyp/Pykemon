import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Pokemon List'
        self.left = 900
        self.top = 300
        self.width = 686
        self.height = 430
        self.df_pokemon = pd.read_csv('Data/pokemon.csv')
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.createTable()

        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget) 
        self.setLayout(self.layout) 

        # Show widget
        self.show()

    def createTable(self):
       # Create table
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(len(self.df_pokemon.name))
        self.tableWidget.setColumnCount(2)
        for idx, name in enumerate(self.df_pokemon.name):
            imagePath = f'Data/pokemon_images/pokemon/pokemon/{idx+1}.png'
            pic = QtGui.QPixmap(imagePath)
            label = QtWidgets.QLabel()
            label.setPixmap(pic)
            self.tableWidget.setItem(idx, 0, QTableWidgetItem(name))
            self.tableWidget.setCellWidget(idx, 1, label)
            self.tableWidget.setRowHeight(idx, 256)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_()) 