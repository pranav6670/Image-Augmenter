import cv2
from PyQt5 import QtGui, QtCore, QtWidgets
import gui
import os
import sys
import aughelper


class Stream(QtCore.QObject):
    newText = QtCore.pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))


class MainApp(QtWidgets.QMainWindow, gui.Ui_MainWindow):

    def __init__(self, parent=None):

        super(MainApp, self).__init__(parent)
        self.setupUi(self)
        self.msgbox = QtWidgets.QMessageBox()
        self.msgbox.setText("The application may remain unresponsive. Do not close the main window.")
        self.msgbox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.msgbox.setIcon(QtWidgets.QMessageBox.Warning)
        self.msgbox.setWindowTitle("Important!!")

        self.extension = '.jpg'

        self.dirName = 'Augmented'
        self.setWindowTitle("Image Augmenter")
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        if not os.path.exists(self.dirName):
            os.mkdir(self.dirName)
            print("Directory", self.dirName, "Created")
        else:
            print("Directory", self.dirName, " already exists")

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
        self.fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()",
                                                                 "", "All Files (*);;Python Files (*.py)",
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
        self.msgbox.exec_()
        aughelper.callall(self.dirName, self.extension, self.image)

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
