from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class KindForMind(object):
    def THINK(self, PLEASE):
        self.table = QtWidgets.QTableWidget()
        self.table.setRowCount(2)
        pic = QtGui.QPixmap("Data/pokemon_images/pokemon/pokemon/1.png")
        self.label = QtWidgets.QLabel(PLEASE)
        self.label.setPixmap(pic)
        self.table.setCellWidget(0,0, self.label)
        self.table.setCellWidget(1,0, self.label)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    PLEASE = QtWidgets.QWidget()
    ui = KindForMind()
    ui.THINK(PLEASE)
    PLEASE.show()
    sys.exit(app.exec_())