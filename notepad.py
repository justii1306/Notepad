from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow,
                             QMenu, QMenuBar, QDockWidget,
                             QAction, QFileDialog, QStatusBar)
from PyQt5.QtGui import QIcon, QKeySequence
import os

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
 
    def initUI(self):
        self.setWindowIcon(QIcon('totalcmd.png'))
        self.setWindowTitle("Notatnik")

        self.filename = ""
        
        mainMenu = self.menuBar()
        plikMenu = mainMenu.addMenu('Plik')
        edycjaMenu = mainMenu.addMenu('Edycja')

        nowyAction = QAction(QIcon('nowy.png'), 'Nowy plik', self)
        nowyAction.setShortcut(QKeySequence('Ctrl+N'))
        nowyAction.triggered.connect(self.nowyFun)
        
        otworzAction = QAction(QIcon('otworz.png'), 'Otwórz plik', self)
        otworzAction.setShortcut(QKeySequence('Ctrl+O'))
        otworzAction.triggered.connect(self.otworzFun)
                                 
        zapiszAction = QAction(QIcon('zapisz.png'), 'Zapisz', self)
        #TODO

        zapiszJakoAction = QAction(QIcon('zapiszJako.png'), 'Zapisz jako', self)
        #TODO

        cofnijAction = QAction(QIcon('cofnij.png'), 'Cofnij', self)
        cofnijAction.setShortcut(QKeySequence('Ctrl+Z'))
        cofnijAction.triggered.connect(self.cofnijFun)

        ponowAction = QAction(QIcon('ponow.png'), 'Ponow', self)
        #TODO

        wytnijAction = QAction(QIcon('wytnij.png'), 'Wytnij', self)
        wytnijAction.setShortcut(QKeySequence('Ctrl+X'))
        wytnijAction.triggered.connect(self.wytnijFun)

        skopiujAction = QAction(QIcon('skopiuj.png'), 'Skopiuj', self)
        #TODO

        wklejAction = QAction(QIcon('wklej.png'), 'Wklej', self)
        #TODO
        
        self.toolbar = self.addToolBar('ToolBar')
        self.toolbar.addAction(nowyAction)
        self.toolbar.addAction(otworzAction)
        self.toolbar.addAction(zapiszAction)
        self.toolbar.addAction(zapiszJakoAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(cofnijAction)
        self.toolbar.addAction(ponowAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(wytnijAction)
        self.toolbar.addAction(skopiujAction)
        self.toolbar.addAction(wklejAction)
        self.toolbar.addSeparator()

        plikMenu.addAction(nowyAction)
        plikMenu.addAction(otworzAction)
        plikMenu.addAction(zapiszAction)
        plikMenu.addAction(zapiszJakoAction)

        edycjaMenu.addAction(cofnijAction)
        edycjaMenu.addAction(ponowAction)
        edycjaMenu.addSeparator()
        edycjaMenu.addAction(wytnijAction)
        edycjaMenu.addAction(skopiujAction)
        edycjaMenu.addAction(wklejAction)

        self.mid = Mid()
        self.setCentralWidget(self.mid)

        self.ostatniaAkcja = QtWidgets.QLabel()
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.addPermanentWidget(self.ostatniaAkcja)
        
        self.show()

    def nowyFun(self):
        nazwa = QFileDialog.getSaveFileName(self, 'Stworz nowy plik', os.getcwd(),"Text files (*.txt)")
        if (nazwa != ('', '')):
            s = open(nazwa[0],"wt")
            self.filename = nazwa
            self.ostatniaAkcja.setText("Stworzono plik")

    def otworzFun(self):
        nazwa = QFileDialog.getOpenFileName(self, 'Otwórz plik', os.getcwd(),"Text files (*.txt)")
        if (nazwa != ('', '')):
            s = open(nazwa[0],"rt").read()
            self.mid.text.setText(s)
            self.filename = nazwa
            self.ostatniaAkcja.setText("Otworzono plik")

    def zapiszFun(self):
        if (self.filename == ""):
            nazwa = QFileDialog.getSaveFileName(self, 'Zapisz plik', os.getcwd(),"Text files (*.txt)")
        else:
            nazwa = self.filename
        if (nazwa != ('', '')):
            s = open(nazwa[0],"wt")
            s.write(self.mid.text.toPlainText())
            self.filename = nazwa
            self.ostatniaAkcja.setText("Zapisano plik")

    def zapiszJakoFun(self):
        nazwa = QFileDialog.getSaveFileName(self, 'Zapisz plik jako', os.getcwd(),"Text files (*.txt)")
        if (nazwa != ('', '')):
            s = open(nazwa[0],"wt")
            s.write(self.mid.text.toPlainText())
            self.filename = nazwa
            self.ostatniaAkcja.setText("Zapisano plik jako")

    def cofnijFun(self):
        self.mid.text.undo()
        self.ostatniaAkcja.setText("Cofnięto akcję")

    def ponowFun(self):
        self.mid.text.redo()
        self.ostatniaAkcja.setText("Ponowiono akcję")

    def wytnijFun(self):
        self.mid.text.cut()
        self.ostatniaAkcja.setText("Wycięto tekst")

    def skopiujFun(self):
        self.mid.text.copy()
        self.ostatniaAkcja.setText("Skopiowano tekst")

    def wklejFun(self):
        self.mid.text.paste()
        self.ostatniaAkcja.setText("Wklejono tekst")
        
class Mid(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Mid, self).__init__(parent)
        mainLayout = QtWidgets.QHBoxLayout()

        #--Options - Left Panel
        self.optionsWidget = QWidget()
        self.options = QtWidgets.QVBoxLayout()

        #-FontSize - ComboBox
        self.sizeComboBox = QtWidgets.QComboBox()
        self.sizeComboBox.addItem("10")
        self.sizeComboBox.addItem("12")
        self.sizeComboBox.addItem("14")
        self.sizeComboBox.currentIndexChanged.connect(self.sizeselectionchange)
        self.options.addWidget(self.sizeComboBox)
        #-END FontSize - ComboBox

        #-FontFamily - RadioButton
        self.timesNewRoman = QtWidgets.QRadioButton("Times New Roman")
        self.timesNewRoman.setChecked(True)
        self.timesNewRoman.toggled.connect(lambda:self.buttonstate(self.timesNewRoman))
        self.arial = QtWidgets.QRadioButton("Arial")
        self.arial.toggled.connect(lambda:self.buttonstate(self.arial))
        self.courierNew = QtWidgets.QRadioButton("Courier New")
        self.courierNew.toggled.connect(lambda:self.buttonstate(self.courierNew))
        self.options.addWidget(self.timesNewRoman)
        self.options.addWidget(self.arial)
        self.options.addWidget(self.courierNew)
        #-END FontFamily - RadioButton

        #-BackgrounColour - GridLayout
        self.colorWidget = QWidget()
        self.colorGrid = QtWidgets.QGridLayout()
        
        self.black = QtWidgets.QPushButton()
        self.black.setStyleSheet("background-color: black")
        self.black.setMaximumSize(10, 10)
        self.black.clicked.connect(lambda: self.colorchange("black"))

        self.white = QtWidgets.QPushButton()
        self.white.setStyleSheet("background-color: white")
        self.white.setMaximumSize(10, 10)
        self.white.clicked.connect(lambda: self.colorchange("white"))

        self.red = QtWidgets.QPushButton()
        self.red.setStyleSheet("background-color: red")
        self.red.setMaximumSize(10, 10)
        self.red.clicked.connect(lambda: self.colorchange("red"))
        
        self.blue = QtWidgets.QPushButton()
        self.blue.setStyleSheet("background-color: blue")
        self.blue.setMaximumSize(10, 10)
        #TODO clicked.connect

        self.green = QtWidgets.QPushButton()
        self.green.setStyleSheet("background-color: green")
        self.green.setMaximumSize(10, 10)
        #TODO clicked.connect
        
        self.colorGrid.addWidget(self.black,0,0)
        self.colorGrid.addWidget(self.white,0,1)
        self.colorGrid.addWidget(self.red,0,2)
        self.colorGrid.addWidget(self.blue,0,3)
        self.colorGrid.addWidget(self.green,0,4)
        
        self.colorWidget.setLayout(self.colorGrid)
        self.options.addWidget(self.colorWidget)
        #-END BackgrounColour - GridLayout
        
        self.options.setAlignment(QtCore.Qt.AlignTop)
        self.optionsWidget.setLayout(self.options)
        mainLayout.addWidget(self.optionsWidget)
        #--Options - Left Panel END

        #Text - Right Panel
        self.text = QtWidgets.QTextEdit()
        
        self.text.setFontFamily("Times New Roman")
        self.text.setFontPointSize(10)
        
        mainLayout.addWidget(self.text)
        #Text - Right Panel END

        self.setLayout(mainLayout)

    def sizeselectionchange(self):
        size = int(self.sizeComboBox.currentText())
        self.text.setFontPointSize(size)

    def buttonstate(self,b):
        if b.text() == "Times New Roman":
            if b.isChecked() == True:
                self.text.setFontFamily("Times New Roman")
                
        if b.text() == "Arial":
            if b.isChecked() == True:
                self.text.setFontFamily("Arial")

        #TODO Courier New

    def colorchange(self,color):
        styleSheet = "background-color: " + color
        self.text.setStyleSheet(styleSheet)


        
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
