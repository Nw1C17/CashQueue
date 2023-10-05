import sys
from PyQt5 import QtCore, QtWidgets, QtGui
import random
import os
class Cash():
    def __init__(self):
        self.number = None
        self.timer = None
        self.queue = [] #очередь в кассу
        self.IsActive = False
        self.intr = None
        self.mean = [] #список всех интервалов для таймера
        self.countofstart = None  # колличество перезапусков

class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.kassi = []
        self.its = []
        self.its2 = []
        self.box = []
        self.label1 = []
        self.label2 = []
        for i in range(3): # сначала создаем 5 касс
            cash = Cash()
            cash.number = i
            cash.timer = QtCore.QTimer(self)
            cash.timer.timeout.connect(lambda inter=i: self.minus(inter))
            self.it = QtWidgets.QSpinBox()
            self.it.setRange(0, 59)
            self.it.setValue(1)
            self.its.append(self.it)

            self.it2 = QtWidgets.QSpinBox()
            self.it2.setRange(0, 59)
            self.it2.setValue(2)
            self.its2.append(self.it2)

            self.b = QtWidgets.QLabel(self)
            pixmap = QtGui.QPixmap(os.path.join("kassa.png"))
            self.b.resize(150, 150)
            self.b.setPixmap(pixmap.scaled(self.b.size(), QtCore.Qt.KeepAspectRatio))
            self.box.append(self.b)

            self.l1 = QtWidgets.QLabel(self)
            self.l1.setText(''.join(["в очереди ", str(len(cash.queue))]))
            self.label1.append(self.l1)

            self.l2 = QtWidgets.QLabel(self)
            self.l2.setText("среднее ")
            self.label2.append(self.l2)

            cash.intr = random.uniform(self.its[i].value(), self.its2[i].value())
            cash.countofstart = 1
            cash.timer.setInterval((cash.intr+1) * 1000)
            cash.timer.start()
            self.kassi.append(cash)


        self.spinMins = QtWidgets.QSpinBox()
        self.spinMins.setRange(0, 59)
        self.spinMins.setValue(5)

        self.secsLabel = QtWidgets.QLabel('Люди приходят через', self)


        self.CountLabel = QtWidgets.QLabel('Кол-во людей', self)


        self.pep = QtWidgets.QSpinBox()
        self.pep.setRange(0, 59)
        self.pep.setValue(30)

        self.buttonstart = QtWidgets.QPushButton('Lets Fcking GOOOOO')
        self.buttonstart.clicked.connect(self.resume)

        self.buttonstop = QtWidgets.QPushButton('СТОП')
        self.buttonstop.clicked.connect(self.pause)

        self.button = QtWidgets.QPushButton('Обновить')
        self.button.clicked.connect(self.resetTimer)

        self.button1 = QtWidgets.QPushButton('Минус Касса')
        self.button1.clicked.connect(self.minus_kassa)

        self.button2 = QtWidgets.QPushButton('Плюс Касса')
        self.button2.clicked.connect(self.plus_kassa)

        self.edit = QtWidgets.QTextEdit()
        self.edit.setReadOnly(True)
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.addWidget(self.edit, 3, 0, 4, 2)
        self.layout.addWidget(self.spinMins, 1, 0)
        self.layout.addWidget(self.pep, 2, 0)


        self.layout.addWidget(self.secsLabel, 1, 1)
        self.layout.addWidget(self.CountLabel, 2, 1)
        self.layout.addWidget(self.buttonstop, 1, 5)
        self.layout.addWidget(self.buttonstart, 1, 6)
        self.layout.addWidget(self.button, 1, 2)
        self.layout.addWidget(self.button1, 1, 3)
        self.layout.addWidget(self.button2, 1, 4)

        for i in range(len(self.its)):
            self.layout.addWidget(self.its[i], 4, i+2) # для каждого таймера спинбокс
            self.layout.addWidget(self.its2[i], 5, i + 2)  # для каждого таймера спинбокс
        for i in range(len(self.box)):
            self.layout.addWidget(self.box[i], 3, i + 2)
            self.layout.addWidget(self.label1[i], 6, i+2)
            self.layout.addWidget(self.label2[i], 7, i + 2)

        self.mainTimer = QtCore.QTimer(self)
        self.mainTimer.timeout.connect(self.updateplot)


        self.startTimer = QtCore.QTimer(self)
        self.startTimer.setSingleShot(True)

        self.w = QtWidgets.QWidget()
        self.w.setLayout(self.layout)

        self.mw = QtWidgets.QScrollArea()
        self.mw.setWidgetResizable(True)
        self.mw.setWidget(self.w)
        #self.mw.resize(1500, 500)
        self.mw.show()

        def start_point():
            self.mainTimer.timeout.emit()
            self.mainTimer.start()
        self.startTimer.timeout.connect(start_point)
        self.resetTimer()


    def resetTimer(self): #перезапуск процесса(все данные остаются)
        #self.countofstart +=1

        self.mainTimer.stop()
        self.startTimer.stop()
        mins = self.spinMins.value()

        self.edit.append('restarting timer... (%dm)' % (mins))
        self.mainTimer.setInterval(mins * 1000)
        #for i in range(len(self.kassi)):
            #self.kassi[i].countofstart += 1
            #self.kassi[i].mean.append(self.kassi[i].intr)
            #self.kassi[i].intr = random.uniform(0.1, self.its[i].value())
            #self.kassi[i].timer.setInterval(self.kassi[i].intr*1000)
        self.startTimer.start()

    def updateplot(self): #для главного таймера(через сколько приходят  люди)
        people = ["человек"] * random.randint(0, self.pep.value())
        pixmap = QtGui.QPixmap(os.path.join("kassa.png"))
        pixmap2 = QtGui.QPixmap(os.path.join("free.png"))
        pixmap3 = QtGui.QPixmap(os.path.join("busy.png"))
        for i in people:
            self.edit.append(''.join(["человек идет в очередь кассы ", str(self.findMin().number)]))
            self.findMin().queue.append(i)
        for i in range(len(self.kassi)):
            self.label1[i].setText("кол-во людей " + str(len(self.kassi[i].queue)))
            self.label2[i].setText("среднее " + str(sum(self.kassi[i].mean)/self.kassi[i].countofstart))
            self.edit.append(''.join(["касса ", str(self.kassi[i].number)]))
            self.edit.append(''.join(["среднее время ", str(sum(self.kassi[i].mean)/self.kassi[i].countofstart)]))
            self.edit.append(''.join(["кол-во людей ", str(len(self.kassi[i].queue))]))
            if (len(self.kassi[i].queue) == 0):
                self.box[i].setPixmap(pixmap2.scaled(self.b.size(), QtCore.Qt.KeepAspectRatio))
            elif (len(self.kassi[i].queue) == len(self.findMax().queue)):
                self.box[i].setPixmap(pixmap3.scaled(self.b.size(), QtCore.Qt.KeepAspectRatio))
            else:
                self.box[i].setPixmap(pixmap.scaled(self.b.size(), QtCore.Qt.KeepAspectRatio))

        #self.edit.append(str(self.kassi[0].queue))

    def minus(self, inter): #для таймеров касс через сколько уходят люди (inter - номер кассы)
        if len(self.kassi[inter].queue) != 0:
            self.kassi[inter].queue.pop(0)
        self.kassi[inter].countofstart += 1
        self.kassi[inter].mean.append(self.kassi[inter].intr)
        self.kassi[inter].intr = random.uniform(self.its[inter].value(), self.its2[inter].value())
        self.kassi[inter].timer.setInterval(self.kassi[inter].intr * 1000)
        self.edit.append(''.join(["с кассы ", str(inter), " ушел человек"]))

        self.label1[inter].setText(''.join(["кол-во людей " + str(len(self.kassi[inter].queue))]))
        self.label2[inter].setText(''.join(["среднее " + str(sum(self.kassi[inter].mean) / self.kassi[inter].countofstart)]))

        pixmap = QtGui.QPixmap(os.path.join("kassa.png"))
        pixmap2 = QtGui.QPixmap(os.path.join("free.png"))
        pixmap3 = QtGui.QPixmap(os.path.join("busy.png"))
        if (len(self.kassi[inter].queue) == 0):
            self.box[inter].setPixmap(pixmap2.scaled(self.b.size(), QtCore.Qt.KeepAspectRatio))
        elif (len(self.kassi[inter].queue) == len(self.findMax().queue) and len(self.kassi[inter].queue)!=0):
            self.box[inter].setPixmap(pixmap3.scaled(self.b.size(), QtCore.Qt.KeepAspectRatio))
        else:
            self.box[inter].setPixmap(pixmap.scaled(self.b.size(), QtCore.Qt.KeepAspectRatio))


    def minus_kassa(self):
        self.kassi[len(self.kassi)-1].timer.stop()
        kas = self.kassi[len(self.kassi)-1].queue
        for i in kas:
            self.findMin().queue.append(i)
        self.kassi.pop(len(self.kassi)-1)
        self.layout.removeWidget(self.its[len(self.kassi)])
        self.its[len(self.kassi)].deleteLater()
        self.its[len(self.kassi)] = None
        self.its.pop(len(self.kassi))

        self.layout.removeWidget(self.its2[len(self.kassi)])
        self.its2[len(self.kassi)].deleteLater()
        self.its2[len(self.kassi)] = None
        self.its2.pop(len(self.kassi))

        self.layout.removeWidget(self.box[len(self.kassi)])
        self.box[len(self.kassi)].deleteLater()
        self.box[len(self.kassi)] = None
        self.box.pop(len(self.kassi))

        self.layout.removeWidget(self.label1[len(self.kassi)])
        self.label1[len(self.kassi)].deleteLater()
        self.label1[len(self.kassi)] = None
        self.label1.pop(len(self.kassi))

        self.layout.removeWidget(self.label2[len(self.kassi)])
        self.label2[len(self.kassi)].deleteLater()
        self.label2[len(self.kassi)] = None
        self.label2.pop(len(self.kassi))



    def plus_kassa(self):
        cash = Cash()
        cash.number = len(self.kassi)
        cash.timer = QtCore.QTimer(self)
        cash.timer.timeout.connect(lambda inter=len(self.kassi): self.minus(inter))
        b = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap(os.path.join("kassa.png"))
        b.resize(150, 150)
        b.setPixmap(pixmap.scaled(b.size(), QtCore.Qt.KeepAspectRatio))
        self.box.append(b)
        it = QtWidgets.QSpinBox()
        it.setRange(0, 59)
        it.setValue(len(self.kassi) + 1)
        self.its.append(it)
        it2 = QtWidgets.QSpinBox()
        it2.setRange(0, 59)
        it2.setValue(len(self.kassi) + 2)
        self.its2.append(it2)
        l1 = QtWidgets.QLabel(self)
        l1.setText(''.join(["в очереди " + str(len(cash.queue))]))
        self.label1.append(l1)

        l2 = QtWidgets.QLabel(self)
        l2.setText("среднее ")
        self.label2.append(l2)


        cash.intr = random.uniform(it.value(), it2.value())
        self.layout.addWidget(self.its[len(self.kassi)], 4, len(self.kassi) + 2)
        self.layout.addWidget(self.its2[len(self.kassi)], 5, len(self.kassi) + 2)
        self.layout.addWidget(self.box[len(self.kassi)], 3, len(self.kassi) + 2)
        self.layout.addWidget(self.label1[len(self.kassi)], 6, len(self.kassi) + 2)
        self.layout.addWidget(self.label2[len(self.kassi)], 7, len(self.kassi) + 2)
        cash.timer.setInterval((cash.intr + 1) * 1000)
        cash.mean.append(len(self.kassi) + 1)
        cash.countofstart = 1
        cash.timer.start()
        self.kassi.append(cash)

    def findMin(self):
        r = self.kassi[0]
        for i in self.kassi[1:]:
            if i.queue < r.queue:
                r = i
            if(i.queue==r.queue and len(i.queue) == 0):
                r=random.choice([i, r])
        return r

    def findMax(self):
        r = self.kassi[0]
        for i in self.kassi[1:]:
            if i.queue > r.queue:
                r = i
        return r

    def pause(self):
        self.mainTimer.stop()
        for i in range(len(self.kassi)):
            self.kassi[i].timer.stop()

    def resume(self):
        self.mainTimer.start()
        for i in range(len(self.kassi)):
            self.kassi[i].timer.start()


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.setWindowTitle('Timer Test')
    window.setGeometry(600, 100, 300, 200)
    #window.show()
    sys.exit(app.exec_())

