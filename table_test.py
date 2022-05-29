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
        self.layout.addWidget(self.table_widget) 
        self.setLayout(self.layout) 

        # Show widget
        self.show()

    def createTable(self):
       # Create table
        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(len(self.df_pokemon.name))
        self.table_widget.setColumnCount(2)
        for idx, name in enumerate(self.df_pokemon.name):
            image_path = f'Data/pokemon_images/pokemon/pokemon/{idx+1}.png'
            pic = QtGui.QPixmap(image_path)
            label = QtWidgets.QLabel()
            label.setPixmap(pic)
            self.table_widget.setItem(idx, 0, QTableWidgetItem(name))
            self.table_widget.setCellWidget(idx, 1, label)
            self.table_widget.setRowHeight(idx, 256)
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_()) 