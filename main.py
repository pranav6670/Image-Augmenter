import cv2
from PyQt5 import QtGui, QtCore, QtWidgets
import gui
import os
import numpy as np
import sys

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
        if not os.path.exists(self.dirName):
            os.mkdir(self.dirName)
            print("Directory " , self.dirName ,  " Created ")
        else:
            print("Directory " , self.dirName ,  " already exists")

        sys.stdout = Stream(newText=self.onUpdateText)

        # Function Calls
        self.onbrowse()
        self.onshow()
        self.onexit()
        self.onaugmentclicked()

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

    def resizeimage(self, image, w, h):
        self.resized_image = cv2.resize(self.image, (w, h))
        cv2.imwrite(self.dirName+"/Resized-"+str(w)+"*"+str(h)+self.extention, self.resized_image)
        print("Resizing done with "+ str(w) +" * "+ str(h) +" resolution")

    def onaugmentclicked(self):
        self.augment.clicked.connect(self.onaugment)

    def onaugment(self):
        # Customize your resolutions
        self.resizeimage(self.image, 450, 400)
        self.resizeimage(self.image, 200, 200)
        self.resizeimage(self.image, 500, 350)
        self.resizeimage(self.image, 600, 500)
        self.resizeimage(self.image, 250, 350)
        self.resizeimage(self.image, 550, 400)
        self.resizeimage(self.image, 150, 100)
        self.resizeimage(self.image, 150, 120)
        self.resizeimage(self.image, 700, 600)
        self.resizeimage(self.image, 550, 500)
        self.resizeimage(self.image, 200, 350)
        self.resizeimage(self.image, 500, 200)


    def onexit(self):
        self.quit.clicked.connect(sys.exit)

    def __del__(self):
        sys.stdout = sys.__stdout__

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainApp()
    w.show()
    sys.exit(app.exec_())





