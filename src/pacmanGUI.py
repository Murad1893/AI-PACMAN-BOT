from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QBasicTimer
import os
import time
import sys

# TIMER
timer = QtCore.QTime()

#PACMAN AGENT TYPE
REFLEX = "reflex_agent"
MINIMAX = "minimax_agent"
ALPHA = "alpha_beta_agent"
EXPECTIMAX = "expecti_max_agent"

#MAZE
CAPSULE = "capsuleClassic"
CONTEST = "contestClassic"
MEDIUM = "mediumClassic"
MINI = "minimaxClassic"
OPEN = "openClassic"
ORIGINAL = "originalClassic"
SMALL = "smallClassic"
TEST = "testClassic"
TRAPPED = "trappedClassic"
TRICKY = "trickyClassic"

#Enemy
SMART = "directional_ghost"

class Ui_MainWindow(object):

    def __init__(self):
        self.agent_type = ''
        self.ghost_type = ''
        self.title = "Pacman"
        self.maze = ''
        self.depth = ''
        self.iteration = ''
        self.ghost_num = ''
        self.show_display = ''
        self.arr = ['pacman.py']
        self.process = None
        self.click = 0
        self.procTime = 0

    def stopped(self):
        if(self.click == 1):
            self.plainTextEdit.hide()
            self.label_2.hide()
            self.click = 0
        else:
            self.click += 1
        self.process.kill() #stopping the process manually

    def clicked(self):
        timer.start()
        if(self.depthin.text() == '' or self.comboBox.currentText() == 'No Agent' or self.comboBox.currentText() == 'Reflex Agent'):
            self.depth = ''
        else:
            self.depth = 'depth=' + self.depthin.text()
        if(self.iterationin.text() == '' or self.comboBox.currentText() == 'No Agent'):
            self.iteration = ''
        else:
            self.iteration = self.iterationin.text()
        if(self.NoGin.text() == ''):
            self.ghost_num = ''
        else:
            self.ghost_num = self.NoGin.text()

        #PACMAN AGENT

        if(self.comboBox.currentText() == "Reflex Agent"):
            self.agent_type = REFLEX
        elif(self.comboBox.currentText() == "Alpha Beta Agent"):
            self.agent_type = ALPHA
        elif(self.comboBox.currentText() == "ExpectiMax Agent"):
            self.agent_type = EXPECTIMAX
        elif(self.comboBox.currentText() == "MiniMax Agent"):
            self.agent_type = MINIMAX

        #GHOST agent_type

        if(self.comboBox_2.currentText() == "Smart Agent"):
            self.ghost_type = SMART
        else:
            self.ghost_type = ''

        #maze
        if(self.comboBox_3.currentText() == "Contest Classic"):
            self.maze = CONTEST
        elif(self.comboBox_3.currentText() == "Medium Classic"):
            self.maze = MEDIUM
        elif(self.comboBox_3.currentText() == "Minimax Classic"):
            self.maze = MINI
        elif(self.comboBox_3.currentText() == "Open Classic"):
            self.maze = OPEN
        elif(self.comboBox_3.currentText() == "Capsule Classic"):
            self.maze = CAPSULE
        elif(self.comboBox_3.currentText() == "Small Classic"):
            self.maze = SMALL
        elif(self.comboBox_3.currentText() == "Test Classic"):
            self.maze = TEST
        elif(self.comboBox_3.currentText() == "Trapped Classic"):
            self.maze = TRAPPED
        elif(self.comboBox_3.currentText() == "Tricky Classic"):
            self.maze = TRICKY
        else:
            self.maze = ORIGINAL

        if (self.Displaycheck.isChecked()):
            self.show_display = ''
        else:
            self.show_display = '-q'

        if(self.maze!=''):
            self.arr.append('-l')
            self.arr.append(self.maze)
        if(self.agent_type!=''):
            self.arr.append('-p')
            self.arr.append(self.agent_type)
        if(self.ghost_type!=''):
            self.arr.append('-g')
            self.arr.append(self.ghost_type)
        if(self.depth!=''):
            self.arr.append('-a')
            self.arr.append(self.depth)
        if(self.ghost_num!=''):
            self.arr.append('-k')
            self.arr.append(self.ghost_num)
        if(self.show_display!=''):
            self.arr.append(self.show_display)
        if(self.iteration!=''):
            self.arr.append('-n')
            self.arr.append(self.iteration)

        # print(self.arr)
        #
        # print('Starting process')
        self.process.start('python', self.arr)

        self.plainTextEdit.show()
        self.label_2.show()

    def quitclicked(self):
        app.quit()

    def append(self, text):
        self.plainTextEdit.clear()
        self.plainTextEdit.insertPlainText(text)

    def stdoutReady(self):
        text = bytearray(self.process.readAllStandardOutput())
        text = text.decode('mbcs')
        self.procTime = timer.elapsed() / 1000
        str = "\nProcess took {} seconds".format(self.procTime)
        text += str
        self.append(text)

    def show_processing(self):
        self.plainTextEdit.clear()
        self.plainTextEdit.insertPlainText("Processing..................................")

    def finished(self):
        # print('Finished!')
        self.arr.clear()
        self.arr.append('pacman.py')
        if(self.plainTextEdit.toPlainText() == "Processing.................................."):
            self.plainTextEdit.clear()


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(837, 848)
        MainWindow.setStyleSheet("#MainWindow { border-image: url(../images/pacman_frontpage.jpg) 0 0 0 0 stretch stretch; }")
        MainWindow.setWindowIcon(QtGui.QIcon('../images/window_pacicon.png'))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.picture1 = QtWidgets.QLabel(self.centralwidget)
        self.picture1.setGeometry(QtCore.QRect(-330, -170, 1531, 1021))
        self.picture1.setStyleSheet(".playbutton{\n"
                                    "background:#FDE402;\n"
                                    "}")
        self.picture1.setText("")
        self.picture1.setScaledContents(False)
        self.picture1.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.picture1.setObjectName("picture1")
        self.playbutton = QtWidgets.QPushButton(self.centralwidget)
        self.playbutton.setGeometry(QtCore.QRect(670, 770, 151, 61))
        self.playbutton.setStyleSheet("background:#FDE402;\n"
"font: 87 18pt \"Source Sans Pro Black\";\n"
"color: #0C1735;")
        self.playbutton.setAutoDefault(False)
        self.playbutton.setDefault(False)
        self.playbutton.setFlat(False)
        self.playbutton.setObjectName("playbutton")
        self.closebutton = QtWidgets.QPushButton(self.centralwidget)
        self.closebutton.setGeometry(QtCore.QRect(500, 770, 151, 61))
        self.closebutton.setStyleSheet("background:#FDE402;\n"
"font: 87 18pt \"Source Sans Pro Black\";\n"
"color: #0C1735;")
        self.closebutton.setAutoDefault(False)
        self.closebutton.setDefault(False)
        self.closebutton.setFlat(False)
        self.closebutton.setObjectName("closebutton")

        self.QUIT = QtWidgets.QPushButton(self.centralwidget)
        self.QUIT.setGeometry(QtCore.QRect(20, 770, 151, 61))
        self.QUIT.setStyleSheet("background:#FDE402;\n"
"font: 87 18pt \"Source Sans Pro Black\";\n"
"color: #0C1735;")
        self.QUIT.setAutoDefault(False)
        self.QUIT.setDefault(False)
        self.QUIT.setFlat(False)
        self.QUIT.setObjectName("QUIT")
        self.paclabel = QtWidgets.QLabel(self.centralwidget)
        self.paclabel.setGeometry(QtCore.QRect(20, 120, 251, 41))
        self.paclabel.setStyleSheet("font: 87 18pt \"Source Sans Pro Black\";\n"
"color: white;")
        self.paclabel.setObjectName("paclabel")
        self.ghostlabel = QtWidgets.QLabel(self.centralwidget)
        self.ghostlabel.setGeometry(QtCore.QRect(20, 220, 231, 41))
        self.ghostlabel.setStyleSheet("font: 87 18pt \"Source Sans Pro Black\";\n"
"color: white;")
        self.ghostlabel.setObjectName("ghostlabel")
        self.maplabel = QtWidgets.QLabel(self.centralwidget)
        self.maplabel.setGeometry(QtCore.QRect(20, 310, 131, 41))
        self.maplabel.setStyleSheet("font: 87 18pt \"Source Sans Pro Black\";\n"
"color: white;")
        self.maplabel.setObjectName("maplabel")
        self.DepthLabel = QtWidgets.QLabel(self.centralwidget)
        self.DepthLabel.setGeometry(QtCore.QRect(20, 400, 181, 41))
        self.DepthLabel.setStyleSheet("font: 87 18pt \"Source Sans Pro Black\";\n"
"color: white;")
        self.DepthLabel.setObjectName("DepthLabel")
        self.IterationLabel = QtWidgets.QLabel(self.centralwidget)
        self.IterationLabel.setGeometry(QtCore.QRect(20, 490, 181, 41))
        self.IterationLabel.setStyleSheet("font: 87 18pt \"Source Sans Pro Black\";\n"
"color: white;")
        self.IterationLabel.setObjectName("IterationLabel")
        self.NoOfGhostLabel = QtWidgets.QLabel(self.centralwidget)
        self.NoOfGhostLabel.setGeometry(QtCore.QRect(20, 580, 221, 41))
        self.NoOfGhostLabel.setStyleSheet("font: 87 18pt \"Source Sans Pro Black\";\n"
"color: white;")
        self.NoOfGhostLabel.setObjectName("NoOfGhostLabel")
        self.Displaycheck = QtWidgets.QCheckBox(self.centralwidget)
        self.Displaycheck.setGeometry(QtCore.QRect(20, 670, 221, 41))
        self.Displaycheck.setStyleSheet("font: 87 18pt \"Source Sans Pro Black\";\n"
"color: white;")
        self.Displaycheck.setObjectName("Displaycheck")
        self.Displaycheck.setChecked(True)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(20, 200, 191, 31))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(20, 170, 191, 41))
        self.comboBox.setStyleSheet("background:transparent;\n"
"color:#FFE400;\n"
"font: 87 14pt \"Source Sans Pro Black\";")
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(20, 260, 191, 41))
        self.comboBox_2.setStyleSheet("background:transparent;\n"
"color:#FFE400;\n"
"font: 87 14pt \"Source Sans Pro Black\";")
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_3 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_3.setGeometry(QtCore.QRect(20, 350, 191, 41))
        self.comboBox_3.setStyleSheet("background:transparent;\n"
"color:#FFE400;\n"
"font: 87 14pt \"Source Sans Pro Black\";")
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(20, 290, 191, 31))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(20, 370, 191, 41))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.depthin = QtWidgets.QLineEdit(self.centralwidget)
        self.depthin.setGeometry(QtCore.QRect(20, 430, 191, 31))
        self.depthin.setStyleSheet("background:transparent;\n"
"color:#FFE400;\n"
"border:none;\n"
"font: 87 16pt \"Source Sans Pro Black\";\n"
"")
        self.depthin.setObjectName("depthin")
        self.NoGin = QtWidgets.QLineEdit(self.centralwidget)
        self.NoGin.setGeometry(QtCore.QRect(20, 610, 191, 31))
        self.NoGin.setStyleSheet("background:transparent;\n"
"color:#FFE400;\n"
"border:none;\n"
"font: 87 16pt \"Source Sans Pro Black\";")
        self.NoGin.setObjectName("NoGin")
        self.iterationin = QtWidgets.QLineEdit(self.centralwidget)
        self.iterationin.setGeometry(QtCore.QRect(20, 520, 191, 31))
        self.iterationin.setStyleSheet("background:transparent;\n"
"color:#FFE400;\n"
"border:none;\n"
"font: 87 16pt \"Source Sans Pro Black\";")
        self.iterationin.setObjectName("iterationin")
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setGeometry(QtCore.QRect(20, 460, 191, 16))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.line_5 = QtWidgets.QFrame(self.centralwidget)
        self.line_5.setGeometry(QtCore.QRect(20, 550, 191, 16))
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.line_6 = QtWidgets.QFrame(self.centralwidget)
        self.line_6.setGeometry(QtCore.QRect(20, 640, 191, 16))
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 30, 131, 71))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../images/pacman_icon.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)

        # self.process = QtCore.QProcess(MainWindow)
        self.process = QtCore.QProcess(self.plainTextEdit)
        self.process.readyReadStandardOutput.connect(self.stdoutReady)
        self.process.started.connect(self.show_processing)
        self.process.finished.connect(self.finished)

        self.plainTextEdit.setGeometry(QtCore.QRect(320, 180, 521, 530))
        self.plainTextEdit.hide()
        self.plainTextEdit.setStyleSheet("background-color: rgba(34,36,38,230);\n"
"border:2px solid #FFE400;\n"
"color:white;\n"
"font: 87 12pt \"Consolas\";\n"
"")
        self.plainTextEdit.setDocumentTitle("")
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setBackgroundVisible(False)
        self.plainTextEdit.setCenterOnScroll(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(320, 150, 201, 21))
        self.label_2.hide()
        self.label_2.setStyleSheet("font: 87 14pt \"Source Sans Pro Black\";\n"
"color: white;")
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Pacman"))
        self.playbutton.setText(_translate("MainWindow", "P L A Y"))
        self.closebutton.setText(_translate("MainWindow", "S T O P"))
        self.QUIT.setText(_translate("MainWindow", "Q U I T"))
        self.paclabel.setText(_translate("MainWindow", "Choose Pacman Agent"))
        self.ghostlabel.setText(_translate("MainWindow", "Choose Ghost Agent"))
        self.maplabel.setText(_translate("MainWindow", "Maps"))
        self.DepthLabel.setText(_translate("MainWindow", "Depth"))
        self.IterationLabel.setText(_translate("MainWindow", "Iteration"))
        self.NoOfGhostLabel.setText(_translate("MainWindow", "Number Of Ghost"))
        self.Displaycheck.setText(_translate("MainWindow", "Show Display"))
        self.comboBox.setItemText(0, _translate("MainWindow", "No Agent"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Reflex Agent"))
        self.comboBox.setItemText(2, _translate("MainWindow", "Alpha Beta Agent"))
        self.comboBox.setItemText(3, _translate("MainWindow", "ExpectiMax Agent"))
        self.comboBox.setItemText(4, _translate("MainWindow", "MiniMax Agent"))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "Random Agent"))
        self.comboBox_2.setItemText(1, _translate("MainWindow", "Smart Agent"))
        self.comboBox_3.setItemText(0, _translate("MainWindow", "Original Classic"))
        self.comboBox_3.setItemText(1, _translate("MainWindow", "Contest Classic"))
        self.comboBox_3.setItemText(2, _translate("MainWindow", "Medium Classic"))
        self.comboBox_3.setItemText(3, _translate("MainWindow", "Minimax Classic"))
        self.comboBox_3.setItemText(4, _translate("MainWindow", "Open Classic"))
        self.comboBox_3.setItemText(5, _translate("MainWindow", "Capsule Classic"))
        self.comboBox_3.setItemText(6, _translate("MainWindow", "Small Classic"))
        self.comboBox_3.setItemText(7, _translate("MainWindow", "Test Classic"))
        self.comboBox_3.setItemText(8, _translate("MainWindow", "Trapped Classic"))
        self.comboBox_3.setItemText(9, _translate("MainWindow", "Tricky Classic"))
        self.label_2.setText(_translate("MainWindow", "Terminal Output"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.playbutton.clicked.connect(ui.clicked)
    ui.closebutton.clicked.connect(ui.stopped)
    ui.QUIT.clicked.connect(ui.quitclicked)
    MainWindow.show()
    sys.exit(app.exec_())
