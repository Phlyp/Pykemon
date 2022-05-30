import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
import teamManager as team

class App(QWidget):

    def __init__(self, player_id):
        super().__init__()
        self.title = 'Pokemon List'
        self.left = 900
        self.top = 300
        self.width = 686
        self.height = 430
        self.df_pokemon = pd.read_csv('Data/pokemon.csv')
        self.count = 1
        self.player_id = player_id
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
        self.table_widget.doubleClicked.connect(self.pokemon_double_clicked)

    def createTable(self):
       # Create table
        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(721)
        self.table_widget.setColumnCount(2)
        image_files = [f for f in os.listdir('Data/pokemon_images/pokemon/pokemon') if os.path.isfile(os.path.join('Data/pokemon_images/pokemon/pokemon', f))]
        for idx, name in enumerate(self.df_pokemon.name):
            image_name = str(idx+1) + '.png'
            if image_name not in image_files:
                image_name = next(x for x in image_files if (str(idx+1) + '-' in x))
            image_path = f'Data/pokemon_images/pokemon/pokemon/{image_name}'
            pic = QtGui.QPixmap(image_path)
            picture_label = QtWidgets.QLabel()
            picture_label.setPixmap(pic)
            self.table_widget.setItem(idx, 0, QTableWidgetItem(name))
            self.table_widget.setCellWidget(idx, 1, picture_label)
            self.table_widget.setRowHeight(idx, 256)
            if idx == 720:
                break
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def pokemon_double_clicked(self):
        self.poke_ID = self.table_widget.currentIndex().row()
        if self.count < 7:
            team.add_pokemon_to_team(self.player_id, self.poke_ID, self.count)
        else:
            print("You can only hold a maximum of 6 Pokemon!")
        self.count += 1

    
def start_selection(player_id):
    app = QApplication(sys.argv)
    ex = App(player_id)
    app.exec_()