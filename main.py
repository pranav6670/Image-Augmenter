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

        self.augment.setToolTip("Click me to augment the image using all operators")
        # self.augment.setToolTipDuration(15)
        self.tabWidget.setCurrentIndex(0)
        self.check = False
        self.extension = '.jpg'

        self.dirName = 'Augmented'
        self.setWindowTitle("Image Augmenter")
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.cmdop.setStyleSheet("QWidget{background-image: url(download.png);}")

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
        self.onresize()
        self.onpad()
        self.oncrop()
        self.onflip()
        self.onhsi()
        self.ongc()
        self.ongcc()
        self.onmul()
        self.ongb()
        self.onmb()
        self.onbb()
        self.onab()
        self.onmop1()
        self.onmop2()
        self.onsharp()
        self.onemboss()
        self.onagn()
        self.onsp()
        self.onpoi()
        self.onspec()
        self.oncontrast()
        self.onscale()
        self.onrotate()
        self.ontranslate()
        self.onsuper()
        self.onhist()
        self.onskel()
        self.onaffine()
        self.oncc()
        self.cleartext()
        if self.check == False:
            self.showim.setEnabled(False)

    def onUpdateText(self, text):
        cursor = self.cmdop.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.cmdop.setTextCursor(cursor)
        self.cmdop.ensureCursorVisible()

    def onbrowse(self):
        self.browse.clicked.connect(self.openFileNameDialog)
        self.browse.clicked.connect(self.browsecheck)

    def browsecheck(self):
        if self.check == True:
            self.showim.setEnabled(True)

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
        print("\nImage Loaded")
        self.check = True

    def showimage(self):
        print("Displaying...")
        self.image = cv2.imread(self.fileName)
        cv2.imshow("Loaded Image", self.image)
        print("Done Displaying")
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def onaugment(self):
        print("Augmenting...")
        self.image = cv2.imread(self.fileName)
        self.msgbox.exec_()
        aughelper.callall(self.dirName, self.extension, self.image)

    def onresize(self):
        self.resz.clicked.connect(lambda :aughelper.onlyresize(self.dirName, self.extension, self.image))

    def onpad(self):
        self.pad.clicked.connect(lambda :aughelper.onlypad(self.dirName, self.extension, self.image))

    def oncrop(self):
        self.crop.clicked.connect(lambda :aughelper.onlycrop(self.dirName, self.extension, self.image))

    def onflip(self):
        self.flip.clicked.connect(lambda :aughelper.onlyflip(self.dirName, self.extension, self.image))

    def onhsi(self):
        self.hsi.clicked.connect(lambda :aughelper.onlyhsi(self.dirName, self.extension, self.image))

    def ongc(self):
        self.gc.clicked.connect(lambda :aughelper.onlygc(self.dirName, self.extension, self.image))

    def ongcc(self):
        self.gcc.clicked.connect(lambda :aughelper.onlygcc(self.dirName, self.extension, self.image))

    def onmul(self):
        self.pchmul.clicked.connect(lambda :aughelper.onlymul(self.dirName, self.extension, self.image))

    def ongb(self):
        self.gb.clicked.connect(lambda :aughelper.onlygb(self.dirName, self.extension, self.image))

    def onab(self):
        self.ab.clicked.connect(lambda :aughelper.onlyab(self.dirName, self.extension, self.image))

    def onmb(self):
        self.mb.clicked.connect(lambda :aughelper.onlymb(self.dirName, self.extension, self.image))

    def onbb(self):
        self.bb.clicked.connect(lambda :aughelper.onlybb(self.dirName, self.extension, self.image))

    def oncc(self):
        self.cc.clicked.connect(lambda :aughelper.onlycc(self.dirName, self.extension, self.image))

    def onmop1(self):
        self.mor1.clicked.connect(lambda :aughelper.onlymo1(self.dirName, self.extension, self.image))

    def onmop2(self):
        self.mor2.clicked.connect(lambda :aughelper.onlymo2(self.dirName, self.extension, self.image))

    def onsharp(self):
        self.sharp.clicked.connect(lambda :aughelper.onlysharp(self.dirName, self.extension, self.image))

    def onemboss(self):
        self.emboss.clicked.connect(lambda :aughelper.onlyemboss(self.dirName, self.extension, self.image))

    def onedge(self):
        self.edge.clicked.connect(lambda :aughelper.onlyedges(self.dirName, self.extension, self.image))

    def onagn(self):
        self.agn.clicked.connect(lambda :aughelper.onlyagn(self.dirName, self.extension, self.image))

    def onsp(self):
        self.sp.clicked.connect(lambda :aughelper.onlysp(self.dirName, self.extension, self.image))

    def onpoi(self):
        self.pnoi.clicked.connect(lambda :aughelper.onlypoi(self.dirName, self.extension, self.image))

    def onspec(self):
        self.spnoi.clicked.connect(lambda :aughelper.onlyspec(self.dirName, self.extension, self.image))

    def oncontrast(self):
        self.contrast.clicked.connect(lambda :aughelper.onlycontrast(self.dirName, self.extension, self.image))

    def onscale(self):
        self.scale.clicked.connect(lambda :aughelper.onlyscale(self.dirName, self.extension, self.image))

    def onrotate(self):
        self.rot.clicked.connect(lambda :aughelper.onlyrotate(self.dirName, self.extension, self.image))

    def ontranslate(self):
        self.trans.clicked.connect(lambda :aughelper.onlytranslate(self.dirName, self.extension, self.image))

    def onsuper(self):
        self.superpixel.clicked.connect(lambda :aughelper.onlysuper(self.dirName, self.extension, self.image))

    def onhist(self):
        self.histeq.clicked.connect(lambda :aughelper.onlyhisteq(self.dirName, self.extension, self.image))

    def onskel(self):
        self.skel.clicked.connect(lambda :aughelper.onlyskelonotize(self.dirName, self.extension, self.image))

    def onaffine(self):
        self.affine.clicked.connect(lambda :aughelper.onlyaffine(self.dirName, self.extension, self.image))

    def onaugmentclicked(self):
        self.augment.clicked.connect(self.onaugment)

    def onexit(self):
        self.quit.clicked.connect(sys.exit)

    def __del__(self):
        sys.stdout = sys.__stdout__

    def cleartext(self):
        self.clear.clicked.connect(self.clearcon)

    def clearcon(self):
        self.cmdop.clear()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainApp()
    w.show()
    sys.exit(app.exec_())