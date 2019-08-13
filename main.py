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

        print("Augmenting...")
        self.image = cv2.imread(self.fileName)
        self.msgbox.exec_()
        aughelper.callall(self.dirName, self.extension, self.image)

    def onresize(self):
        self.resz.clicked.connect(self.augrsz)

    def augrsz(self):
        aughelper.onlyresize(self.dirName, self.extension, self.image)

    def onpad(self):
        self.pad.clicked.connect(self.augpad)

    def augpad(self):
        aughelper.onlypad(self.dirName, self.extension, self.image)

    def oncrop(self):
        self.crop.clicked.connect(self.augcrop)

    def augcrop(self):
        aughelper.onlycrop(self.dirName, self.extension, self.image)

    def onflip(self):
        self.flip.clicked.connect(self.augflip)

    def augflip(self):
        aughelper.onlyflip(self.dirName, self.extension, self.image)

    def onhsi(self):
        self.hsi.clicked.connect(self.aughsi)

    def aughsi(self):
        aughelper.onlyhsi(self.dirName, self.extension, self.image)

    def ongc(self):
        self.gc.clicked.connect(self.auggc)

    def auggc(self):
        aughelper.onlygc(self.dirName, self.extension, self.image)

    def ongcc(self):
        self.gcc.clicked.connect(self.auggcc)

    def auggcc(self):
        aughelper.onlygcc(self.dirName, self.extension, self.image)

    def onmul(self):
        self.pchmul.clicked.connect(self.augmul)

    def augmul(self):
        aughelper.onlymul(self.dirName, self.extension, self.image)

    def ongb(self):
        self.gb.clicked.connect(self.auggb)

    def auggb(self):
        aughelper.onlygb(self.dirName, self.extension, self.image)

    def onab(self):
        self.ab.clicked.connect(self.augab)

    def augab(self):
        aughelper.onlyab(self.dirName, self.extension, self.image)

    def onmb(self):
        self.mb.clicked.connect(self.augmb)

    def augmb(self):
        aughelper.onlymb(self.dirName, self.extension, self.image)

    def onbb(self):
        self.bb.clicked.connect(self.augbb)

    def augbb(self):
        aughelper.onlybb(self.dirName, self.extension, self.image)

    def oncc(self):
        self.cc.clicked.connect(self.augcc)

    def augcc(self):
        aughelper.onlycc(self.dirName, self.extension, self.image)

    def onmop1(self):
        self.mor1.clicked.connect(self.augmo1)

    def augmo1(self):
        aughelper.onlymo1(self.dirName, self.extension, self.image)

    def onmop2(self):
        self.mor2.clicked.connect(self.augmo2)

    def augmo2(self):
        aughelper.onlymo2(self.dirName, self.extension, self.image)

    def onsharp(self):
        self.sharp.clicked.connect(self.augsharp)

    def augsharp(self):
        aughelper.onlysharp(self.dirName, self.extension, self.image)

    def onemboss(self):
        self.emboss.clicked.connect(self.augemboss)

    def augemboss(self):
        aughelper.onlyemboss(self.dirName, self.extension, self.image)

    def onedge(self):
        self.edge.clicked.connect(self.augedge)

    def augedge(self):
        aughelper.onlyedges(self.dirName, self.extension, self.image)

    def onagn(self):
        self.agn.clicked.connect(self.augagn)

    def augagn(self):
        aughelper.onlyagn(self.dirName, self.extension, self.image)
###
    def onsp(self):
        self.sp.clicked.connect(self.augsp)

    def augsp(self):
        aughelper.onlysp(self.dirName, self.extension, self.image)

    def onpoi(self):
        self.pnoi.clicked.connect(self.augpoi)

    def augpoi(self):
        aughelper.onlypoi(self.dirName, self.extension, self.image)

    def onspec(self):
        self.spnoi.clicked.connect(self.augspec)

    def augspec(self):
        aughelper.onlyspec(self.dirName, self.extension, self.image)

    def oncontrast(self):
        self.contrast.clicked.connect(self.augcon)

    def augcon(self):
        aughelper.onlycontrast(self.dirName, self.extension, self.image)

    def onscale(self):
        self.scale.clicked.connect(self.augscale)

    def augscale(self):
        aughelper.onlyscale(self.dirName, self.extension, self.image)

    def onrotate(self):
        self.rot.clicked.connect(self.augrot)

    def augrot(self):
        aughelper.onlyrotate(self.dirName, self.extension, self.image)

    def ontranslate(self):
        self.trans.clicked.connect(self.augtrans)

    def augtrans(self):
        aughelper.onlytranslate(self.dirName, self.extension, self.image)

    def onsuper(self):
        self.superpixel.clicked.connect(self.augsuper)

    def augsuper(self):
        aughelper.onlysuper(self.dirName, self.extension, self.image)

    def onhist(self):
        self.histeq.clicked.connect(self.aughist)

    def aughist(self):
        aughelper.onlyhisteq(self.dirName, self.extension, self.image)

    def onskel(self):
        self.skel.clicked.connect(self.augskel)

    def augskel(self):
        aughelper.onlyskelonotize(self.dirName, self.extension, self.image)

    def onaffine(self):
        self.affine.clicked.connect(self.augaff)

    def augaff(self):
        aughelper.onlyaffine(self.dirName, self.extension, self.image)

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
