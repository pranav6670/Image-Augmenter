import cv2
from PyQt5 import QtGui, QtCore, QtWidgets
import gui
import os
import numpy as np
import sys
import random
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

    def invertimage(self, image, channel):
        image = (channel - image)
        cv2.imwrite(self.dirName+"/Inverted-"+str(channel)+self.extention, image)
        print("Inverted with channel -"+str(channel))

    def gammacorrection(self, image, gamma=1.0):
        invgamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invgamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")
        image = cv2.LUT(image, table)
        if gamma >= 1:
            cv2.imwrite(self.dirName+"/Light"+str(gamma)+self.extention, image)
            print("Gamma correction with <1.0(light)-"+str(gamma))
        else:
            cv2.imwrite(self.dirName+"/Dark"+str(gamma)+self.extention, image)
            print("Gamma correction with gamma >1(dark)-"+str(gamma))

    def add_light_color(self, image, color, gamma=1.0):
        invgamma = 1.0 / gamma
        image = (color - image)
        table = np.array([((i / 255.0) ** invgamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")
        image=cv2.LUT(image, table)
        if gamma >= 1:
            cv2.imwrite(self.dirName+"/Light"+str(gamma)+str(color)+self.extention, image)
            print("Gamma correction with <1.0(light)-"+str(gamma)+str(color))
        else:
            cv2.imwrite(self.dirName+"/Dark"+str(gamma)+str(color)+self.extention, image)
            print("Gamma correction with gamma >1(dark)-"+str(gamma)+str(color))

    def saturateimage(self, image, saturation):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        x = image[:, :, 2]
        x = np.where(x <= 255 - saturation, x + saturation, 255)
        image[:, :, 2] = x
        image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
        cv2.imwrite(self.dirName+"/Saturated with"+str(saturation)+self.extention, image)
        print("Saturated with-"+str(saturation))

    def hueimage(self, image, hue):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        x = image[:, :, 2]
        x = np.where(x <= 255 - hue, x - hue, 255)
        image[:, :, 2] = x
        image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
        cv2.imwrite(self.dirName+"/Hued with"+str(hue)+self.extention, image)
        print("Hued with-"+str(hue))

    def multiplywith(self, image, B, G, R):
        mulimage = image * [B, G, R]
        cv2.imwrite(self.dirName+"/Multiplied with-"+"("+str(B)+", "+str(G)+", "+str(R)+")"+self.extention, mulimage)
        print("Multiplied with"+"("+str(B)+", "+str(G)+", "+str(R)+")")

    def gaussianblur(self, image, blur):
        gbimage = cv2.GaussianBlur(image, (5, 5), blur)
        cv2.imwrite(self.dirName+"/Gaussian blurred-"+str(blur)+self.extention, gbimage)
        print("Gaussian blurred with "+str(blur))

    def avgblur(self, image, kernalcoeff):
        avgimage = cv2.blur(image, (kernalcoeff, kernalcoeff))
        cv2.imwrite(self.dirName+"/Average blurred-"+"("+str(kernalcoeff)+", "+str(kernalcoeff)+")"+self.extention,
                    avgimage)
        print("Average blurred with"+" ("+str(kernalcoeff)+", "+str(kernalcoeff)+")")

    def medblur(self, image, shift):
        medimage = cv2.medianBlur(image, shift)
        cv2.imwrite(self.dirName+"/Median blurred-"+str(shift)+self.extention, medimage)
        print("Median blurred with "+str(shift))

    def bilblur(self, image, d, color, space):
        bilblur = cv2.bilateralFilter(image, d, color, space)
        cv2.imwrite(self.dirName+"/Bilateral blurred- "+str(d)+", "+str(color)+", "+str(space)+self.extention,
                    bilblur)
        print("Bilateral blurred with "+str(d)+", "+str(color)+", "+str(space))

    def morphops(self, image, shift):
        kernal = np.ones((shift, shift), dtype=np.uint8)
        erodedimage = cv2.erode(image, kernal, iterations=1)
        cv2.imwrite(self.dirName+"/Eroded-"+" ("+str(shift)+str(shift)+")"+self.extention, erodedimage)
        dilatedimage = cv2.dilate(image, kernal, iterations=1)
        cv2.imwrite(self.dirName+"/Dilated-"+" ("+str(shift)+str(shift)+")"+self.extention, dilatedimage)
        openedimage = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernal)
        cv2.imwrite(self.dirName+"/Opened-"+" ("+str(shift)+str(shift)+")"+self.extention, openedimage)
        closedimage = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernal)
        cv2.imwrite(self.dirName+"/Closed-"+" ("+str(shift)+str(shift)+")"+self.extention, closedimage)
        morphgradim = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernal)
        cv2.imwrite(self.dirName+"/Morphological gradient-"+" ("+str(shift)+str(shift)+")"+self.extention, morphgradim)

    def morphop2(self, image, shift):
        kernal = np.ones((shift, shift), dtype=np.uint8)
        tophat = cv2.morphologyEx(image, cv2.MORPH_TOPHAT, kernal)
        cv2.imwrite(self.dirName+"/Top Hat-"+" ("+str(shift)+str(shift)+")"+self.extention, tophat)
        blackhat = cv2.morphologyEx(image, cv2.MORPH_BLACKHAT, kernal)
        cv2.imwrite(self.dirName+"/Black Hat-"+" ("+str(shift)+str(shift)+")"+self.extention, blackhat)


    def sharpenimage(self, image):
        kernal_pos = np.array([
            [0, 1, 0],
            [1, -4, 1],
            [0, 1, 0]
        ])

        kernal_neg = np.array([
            [0, -1, 0],
            [-1, 4, -1],
            [0, -1, 0]
        ])

        image_outward = cv2.filter2D(image, -1, kernal_pos)
        image_inward = cv2.filter2D(image, -1, kernal_neg)
        cv2.imwrite(self.dirName+"/Sharpen-Outward"+self.extention, image_outward)
        print("Sharpened with outward edges")
        cv2.imwrite(self.dirName+"/Sharpen-Inward"+self.extention, image_inward)
        print("Sharpened with inward edges")


    def embossimage(self, image):
        kernal1 = np.array([
            [0, 1, 0],
            [0, 0, 0],
            [0, -1, 0]
        ])

        kernal2 = np.array([
            [1, 0, 0],
            [0, 0, 0],
            [0, 0, -1]
        ])

        kernal3 = np.array([
            [0, 0, 0],
            [1, 0, -1],
            [0, 0, 0]
        ])

        kernal4 = np.array([
            [0, 0, 1],
            [0, 0, 0],
            [-1, 0, 0]
        ])

        kernal5 = np.array([
            [-1, 0, 0],
            [0, 0, 0],
            [0, 0, 1]
        ])

        kernal6 = np.array([
            [0, 0, -1],
            [0, 0, 0],
            [1, 0, 0]
        ])

        im1 = cv2.filter2D(image, -1, kernal1)
        cv2.imwrite(self.dirName+"/Embossed1"+self.extention, im1)
        im2 = cv2.filter2D(image, -1, kernal2)
        cv2.imwrite(self.dirName+"/Embossed2"+self.extention, im2)
        im3 = cv2.filter2D(image, -1, kernal3)
        cv2.imwrite(self.dirName+"/Embossed3"+self.extention, im3)
        im4 = cv2.filter2D(image, -1, kernal4)
        cv2.imwrite(self.dirName+"/Embossed4"+self.extention, im4)
        im5 = cv2.filter2D(image, -1, kernal5)
        cv2.imwrite(self.dirName+"/Embossed5"+self.extention, im5)
        im6 = cv2.filter2D(image, -1, kernal6)
        cv2.imwrite(self.dirName+"/Embossed6"+self.extention, im6)
        total = im1 + im2 + im3 + im4 + im5 + im6
        cv2.imwrite(self.dirName+"/Embossing_total"+self.extention, total)
        print("Done with Embossing")


    def edges(self, image):
        # Sobel
        for i in range(1, 10, 2):
            sobelx = cv2.Sobel(image, cv2.CV_16U, 1, 0, ksize=i)
            cv2.imwrite(self.dirName+"/Sobel_x"+str(i)+self.extention, sobelx)
            sobely = cv2.Sobel(image, cv2.CV_16U, 0, 1, ksize=i)
            cv2.imwrite(self.dirName+"/Sobel_y"+str(i)+self.extention, sobely)
            total = sobelx + sobely
            cv2.imwrite(self.dirName+"/Sobel_total"+self.extention, total)
        print("Done with Sobel operator")

        # Scharr
        scharrx = cv2.Scharr(image, -1, 1, 0)
        cv2.imwrite(self.dirName+"/Scharr_x"+self.extention, scharrx)
        scharry = cv2.Scharr(image, -1, 0, 1)
        cv2.imwrite(self.dirName+"/Scharr_y"+self.extention, scharry)
        total = scharrx + scharry
        cv2.imwrite(self.dirName+"/Scharr_total"+self.extention, total)
        print("Done with Scharr operator")

    def onaugment(self):
        self.image = cv2.imread(self.fileName)

        # Customize your resolutions
        self.resizeimage(self.image, 400, 400)
        self.resizeimage(self.image, 350, 300)
        self.resizeimage(self.image, 100, 150)
        self.resizeimage(self.image, 350, 200)
        self.resizeimage(self.image, 300, 100)
        self.resizeimage(self.image, 250, 140)
        self.resizeimage(self.image, 200, 200)
        self.resizeimage(self.image, 100, 100)
        self.resizeimage(self.image, 200, 160)
        self.resizeimage(self.image, 350, 200)
        self.resizeimage(self.image, 200, 450)
        self.resizeimage(self.image, 500, 500)
        self.resizeimage(self.image, 440, 420)
        self.resizeimage(self.image, 200, 380)
        self.resizeimage(self.image, 180, 200)
        self.resizeimage(self.image, 380, 330)

        # Customize padding here
        self.padimage(self.image, 100, 0, 0, 0)
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

        for i in range(0, 255, 25):
            self.invertimage(self.image, i)
            self.saturateimage(self.image, i)
            self.hueimage(self.image, i)

        for i in self.seq(1, 6, 0.1):
            self.gammacorrection(self.image, i)

        for i in range(0, 255, 50):
            for j in self.seq(1, 5, 0.1):
                self.add_light_color(self.image, i, j)

        for x in self.seq(0.1, 1, 0.2):
            for y in self.seq(0.1, 1, 0.2):
                for z in self.seq(0.1, 1, 0.2):
                    self.multiplywith(self.image, x, y, z)

        for t in self.seq(0, 5, 0.5):
            self.gaussianblur(self.image, t)

        for t in range(1, 12, 1):
            self.avgblur(self.image, t)

        for c in range(1, 13, 2):
            self.medblur(self.image, c)

        self.morphops(self.image, 2)
        self.morphop2(self.image, 100)
        self.morphops(self.image, 3)
        self.morphop2(self.image, 150)
        self.morphops(self.image, 4)
        self.morphop2(self.image, 200)

        self.bilblur(self.image, 9, 75, 75)
        self.bilblur(self.image, 12, 100, 100)
        self.bilblur(self.image, 25, 100, 100)
        self.bilblur(self.image, 40, 75, 75)
        self.bilblur(self.image, 50, 100, 100)
        self.bilblur(self.image, 50, 75, 75)

        self.sharpenimage(self.image)
        self.embossimage(self.image)
        self.edges(self.image)

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





