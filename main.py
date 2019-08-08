import cv2
from PyQt5 import QtGui, QtCore, QtWidgets
import gui
import os
import sys
import itertools



class Stream(QtCore.QObject):
    newText = QtCore.pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))


class MainApp(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        self.setupUi(self)

        self.extention = '.jpg'

        self.dirName = 'Augmented'
        self.setWindowTitle("Image Augmenter")
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        if not os.path.exists(self.dirName):
            os.mkdir(self.dirName)
            print("Directory ", self.dirName, "Created")
        else:
            print("Directory ", self.dirName, " already exists")

        sys.stdout = Stream(newText=self.onUpdateText)

        # Function Calls
        self.onbrowse()
        self.onshow()
        self.onexit()
        self.onaugmentclicked()

    def seq(self, start, end, step):
        if step == 0:
            raise ValueError("step must not be 0")
        sample_count = int(abs(end - start) / step)
        return itertools.islice(itertools.count(start, step), sample_count)

    def onUpdateText(self, text):
        cursor = self.cmdop.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.cmdop.setTextCursor(cursor)
        self.cmdop.ensureCursorVisible()

    def onbrowse(self):
        self.browse.clicked.connect(self.openFileNameDialog)

    def onshow(self):
        self.showim.clicked.connect(self.showimage)

    def openFileNameDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        self.fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()",
                                                            "","All Files (*);;Python Files (*.py)",
                                                            options=options)
        if self.fileName:
            print(self.fileName)

    def showimage(self):
        print("Displaying...")
        self.image = cv2.imread(self.fileName)
        cv2.imshow("Loaded Image", self.image)
        print("Done Displaying")
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def onaugment(self):
        self.image = cv2.imread(self.fileName)

        # Customize your resolutions
        # self.resizeimage(self.image, 400, 400)
        # self.resizeimage(self.image, 350, 300)
        # self.resizeimage(self.image, 100, 150)
        # self.resizeimage(self.image, 350, 200)
        # self.resizeimage(self.image, 300, 100)
        # self.resizeimage(self.image, 250, 140)
        # self.resizeimage(self.image, 200, 200)
        # self.resizeimage(self.image, 100, 100)
        # self.resizeimage(self.image, 200, 160)
        # self.resizeimage(self.image, 350, 200)
        # self.resizeimage(self.image, 200, 450)
        # self.resizeimage(self.image, 500, 500)
        # self.resizeimage(self.image, 440, 420)
        # self.resizeimage(self.image, 200, 380)
        # self.resizeimage(self.image, 180, 200)
        # self.resizeimage(self.image, 380, 330)
        #
        # Customize padding here
        # self.padimage(self.image, 100, 0, 0, 0)
        # self.padimage(self.image, 0, 100, 0, 0)
        # self.padimage(self.image, 0, 0, 100, 0)
        # self.padimage(self.image, 0, 0, 0, 100)
        # self.padimage(self.image, 100, 100, 0, 0)
        # self.padimage(self.image, 0, 100, 100, 0)
        # self.padimage(self.image, 0, 0, 100, 100)
        # self.padimage(self.image, 100, 0, 100, 0)
        # self.padimage(self.image, 0, 100, 0, 100)
        # self.padimage(self.image, 200, 0, 0, 0)
        # self.padimage(self.image, 0, 200, 0, 0)
        # self.padimage(self.image, 0, 0, 200, 0)
        # self.padimage(self.image, 0, 0, 0, 200)
        # self.padimage(self.image, 200, 200, 0, 0)
        # self.padimage(self.image, 0, 200, 200, 0)
        # self.padimage(self.image, 0, 0, 200, 200)
        # self.padimage(self.image, 200, 0, 200, 0)
        # self.padimage(self.image, 0, 200, 0, 200)
        #
        # Customize cropping here
        # self.cropimage(self.image, 100, 400, 0, 350)
        # self.cropimage(self.image, 100, 400, 100, 450)
        # self.cropimage(self.image, 0, 300, 0, 350)
        # self.cropimage(self.image, 0, 300, 100, 450)
        # self.cropimage(self.image, 100, 300, 100 ,350)
        #
        # self.flipimage(self.image, 0) # horizontal
        # self.flipimage(self.image, 1) # vertical
        # self.flipimage(self.image, -1) # both
        #
        # for i in range(0, 255, 25):
        #     self.invertimage(self.image, i)
        #     self.saturateimage(self.image, i)
        #     self.hueimage(self.image, i)
        #
        # for i in self.seq(1, 6, 0.1):
        #     self.gammacorrection(self.image, i)
        #
        # for i in range(0, 255, 50):
        #     for j in self.seq(1, 5, 0.1):
        #         self.add_light_color(self.image, i, j)
        #
        # for x in self.seq(0.1, 1, 0.2):
        #     for y in self.seq(0.1, 1, 0.2):
        #         for z in self.seq(0.1, 1, 0.2):
        #             self.multiplywith(self.image, x, y, z)
        #
        # for t in self.seq(0, 5, 0.5):
        #     self.gaussianblur(self.image, t)
        #
        # for t in range(1, 12, 1):
        #     self.avgblur(self.image, t)
        #
        # for c in range(1, 13, 2):
        #     self.medblur(self.image, c)
        #
        # self.morphops(self.image, 2)
        # self.morphop2(self.image, 100)
        # self.morphops(self.image, 3)
        # self.morphop2(self.image, 150)
        # self.morphops(self.image, 4)
        # self.morphop2(self.image, 200)
        #
        # self.bilblur(self.image, 9, 75, 75)
        # self.bilblur(self.image, 12, 100, 100)
        # self.bilblur(self.image, 25, 100, 100)
        # self.bilblur(self.image, 40, 75, 75)
        # self.bilblur(self.image, 50, 100, 100)
        # self.bilblur(self.image, 50, 75, 75)
        #
        # self.sharpenimage(self.image)
        # self.embossimage(self.image)
        # self.edges(self.image)
        # self.colorconv(self.image)
    #
    def onaugmentclicked(self):
        self.augment.clicked.connect(self.onaugment)

    def onexit(self):
        self.quit.clicked.connect(sys.exit)

    def __del__(self):
        sys.stdout = sys.__stdout__

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainApp()
    w.show()
    sys.exit(app.exec_())
