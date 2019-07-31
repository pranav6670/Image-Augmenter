import cv2
from PyQt5 import QtGui, QtCore, QtWidgets
import gui
import os
import numpy as np
import sys
import random

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
        # cv2.namedWindow("Loaded Image", cv2.WINDOW_NORMAL)
        # cv2.resizeWindow("Loaded Image", 600, 600)
        print("Done Displaying")
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def resizeimage(self, image, w, h):
        resized_image = cv2.resize(self.image, (w, h))
        cv2.imwrite(self.dirName+"/Resized-"+str(w)+"*"+str(h)+self.extention, resized_image)
        print("Resizing done with "+ str(w) +" * "+ str(h) +" resolution")

    def padimage(self, image, top, bottom, left, right, padcolor=[0, 0, 0]):
        paddedimage = cv2.copyMakeBorder(self.image, top, bottom, left, right,
                                         cv2.BORDER_CONSTANT, value=padcolor)
        cv2.imwrite(self.dirName+"/Padded-"+ "("+str(top)+","+str(bottom)+")"+"*"+"("+str(left)+","+str(right)+")"+
                    self.extention, paddedimage)
        print("Padding done with "+" ("+str(top)+","+str(bottom)+")"+" * "+"("+str(left)+","+str(right)+")")

    def cropimage(self, image, y1, y2, x1, x2):
        croppedimage = self.image[y1:y2, x1:x2]
        cv2.imwrite(self.dirName+"/Cropped-"+"["+str(y1)+", "+str(y2)+"]"+" * "+"["+str(x1)+", "+str(x2)+"]"+self.extention,
                    croppedimage)
        print("Cropping done with "+ "["+str(y1)+", "+str(y2)+"]"+" * "+"["+str(x1)+", "+str(x2)+"]")

    def flipimage(self, image, dir):
        flippedimage = cv2.flip(self.image, dir)
        cv2.imwrite(self.dirName+"/Flipped-"+str(dir)+self.extention, flippedimage)
        print("Flipping done with "+ str(dir))

    def onaugment(self):

        # Customize your resolutions
        for i in range(random.randrange(50, 500), random.randrange(100, 800)):
            for j in range(random.randrange(50, 600), random.randrange(300, 500)):
                self.resizeimage(self.image, i, j)

        # Customize padding here
        self.padimage(self.image,100, 0, 0, 0)
        self.padimage(self.image, 0, 100, 0, 0)
        self.padimage(self.image, 0, 0, 100, 0)
        self.padimage(self.image, 0, 0, 0, 100)
        self.padimage(self.image, 100, 100, 0, 0)
        self.padimage(self.image, 0, 100, 100, 0)
        self.padimage(self.image, 0, 0, 100, 100)
        self.padimage(self.image, 100, 0, 100, 0)
        self.padimage(self.image, 0, 100, 0, 100)
        self.padimage(self.image, 200, 0, 0, 0)
        self.padimage(self.image, 0, 200, 0, 0)
        self.padimage(self.image, 0, 0, 200, 0)
        self.padimage(self.image, 0, 0, 0, 200)
        self.padimage(self.image, 200, 200, 0, 0)
        self.padimage(self.image, 0, 200, 200, 0)
        self.padimage(self.image, 0, 0, 200, 200)
        self.padimage(self.image, 200, 0, 200, 0)
        self.padimage(self.image, 0, 200, 0, 200)

        # Customize cropping here
        self.cropimage(self.image, 100, 400, 0, 350)
        self.cropimage(self.image, 100, 400, 100, 450)
        self.cropimage(self.image, 0, 300, 0, 350)
        self.cropimage(self.image, 0, 300, 100, 450)
        self.cropimage(self.image, 100, 300, 100 ,350)

        self.flipimage(self.image, 0) # horizontal
        self.flipimage(self.image, 1) # vertical
        self.flipimage(self.image, -1) # both

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





