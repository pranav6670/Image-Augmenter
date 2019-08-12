import cv2
import numpy as np
import itertools
import random
from skimage.util import img_as_float
from skimage.segmentation import slic
from skimage.exposure import rescale_intensity


def seq(start, end, step):
    if step == 0:
        raise ValueError("step must not be 0")
    sample_count = int(abs(end - start) / step)
    return itertools.islice(itertools.count(start, step), sample_count)


def resizeimage(dirName, extension, image, w, h):
    resized_image = cv2.resize(image, (w, h))
    cv2.imwrite(dirName + "/Resized-" + str(w) + "*" + str(h) + extension, resized_image)
    print("Resizing done with " + str(w) + " * " + str(h) + " resolution")


def padimage(dirName, extension, image, top, bottom, left, right, padcolor=[0, 0, 0]):
    paddedimage = cv2.copyMakeBorder(image, top, bottom, left, right,
                                     cv2.BORDER_CONSTANT, value=padcolor)
    cv2.imwrite(dirName + "/Padded-" + "(" + str(top) + "," + str(bottom) + ")" + "*" + "(" + str(left) + "," + str(
        right) + ")" +
                extension, paddedimage)
    print("Padding done with " + " (" + str(top) + "," + str(bottom) + ")" + " * " + "(" + str(left) + "," + str(
        right) + ")")


def cropimage(dirName, extension, image, y1, y2, x1, x2):
    croppedimage = image[y1:y2, x1:x2]
    cv2.imwrite(dirName + "/Cropped-" + "[" + str(y1) + ", " + str(y2) + "]" + " * " + "[" + str(x1) + ", " + str(
        x2) + "]" + extension,
                croppedimage)
    print("Cropping done with " + "[" + str(y1) + ", " + str(y2) + "]" + " * " + "[" + str(x1) + ", " + str(x2) + "]")


def flipimage(dirName, extension, image, dir):
    flippedimage = cv2.flip(image, dir)
    cv2.imwrite(dirName + "/Flipped-" + str(dir) + extension, flippedimage)
    print("Flipping done with " + str(dir))


def invertimage(dirName, extension, image, channel):
    image = (channel - image)
    cv2.imwrite(dirName + "/Inverted-" + str(channel) + extension, image)
    print("Inverted with channel -" + str(channel))


def gammacorrection(dirName, extension, image, gamma=1.0):
    invgamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invgamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")
    image = cv2.LUT(image, table)
    if gamma >= 1:
        cv2.imwrite(dirName + "/Light" + str(gamma) + extension, image)
        print("Gamma correction with <1.0(light)-" + str(gamma))
    else:
        cv2.imwrite(dirName + "/Dark" + str(gamma) + extension, image)
        print("Gamma correction with gamma >1(dark)-" + str(gamma))


def add_light_color(dirName, extension, image, color, gamma=1.0):
    invgamma = 1.0 / gamma
    image = (color - image)
    table = np.array([((i / 255.0) ** invgamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")
    image = cv2.LUT(image, table)
    if gamma >= 1:
        cv2.imwrite(dirName + "/Light" + str(gamma) + str(color) + extension, image)
        print("Gamma correction with <1.0(light)-" + str(gamma) + str(color))
    else:
        cv2.imwrite(dirName + "/Dark" + str(gamma) + str(color) + extension, image)
        print("Gamma correction with gamma >1(dark)-" + str(gamma) + str(color))


def saturateimage(dirName, extension, image, saturation):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    x = image[:, :, 2]
    x = np.where(x <= 255 - saturation, x + saturation, 255)
    image[:, :, 2] = x
    image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
    cv2.imwrite(dirName + "/Saturated with" + str(saturation) + extension, image)
    print("Saturated with-" + str(saturation))


def hueimage(dirName, extension, image, hue):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    x = image[:, :, 2]
    x = np.where(x <= 255 - hue, x - hue, 255)
    image[:, :, 2] = x
    image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
    cv2.imwrite(dirName + "/Hued with" + str(hue) + extension, image)
    print("Hued with-" + str(hue))


def multiplywith(dirName, extension, image, B, G, R):
    mulimage = image * [B, G, R]
    cv2.imwrite(dirName + "/Multiplied with-" + "(" + str(B) + ", " + str(G) + ", " + str(R) + ")" + extension,
                mulimage)
    print("Multiplied with" + "(" + str(B) + ", " + str(G) + ", " + str(R) + ")")


def gaussianblur(dirName, extension, image, blur):
    gbimage = cv2.GaussianBlur(image, (5, 5), blur)
    cv2.imwrite(dirName + "/Gaussian blurred-" + str(blur) + extension, gbimage)
    print("Gaussian blurred with " + str(blur))


def avgblur(dirName, extension, image, kernalcoeff):
    avgimage = cv2.blur(image, (kernalcoeff, kernalcoeff))
    cv2.imwrite(dirName + "/Average blurred-" + "(" + str(kernalcoeff) + ", " + str(kernalcoeff) + ")" + extension,
                avgimage)
    print("Average blurred with" + " (" + str(kernalcoeff) + ", " + str(kernalcoeff) + ")")


def medblur(dirName, extension, image, shift):
    medimage = cv2.medianBlur(image, shift)
    cv2.imwrite(dirName + "/Median blurred-" + str(shift) + extension, medimage)
    print("Median blurred with " + str(shift))


def bilblur(dirName, extension, image, d, color, space):
    bilblur = cv2.bilateralFilter(image, d, color, space)
    cv2.imwrite(dirName + "/Bilateral blurred- " + str(d) + ", " + str(color) + ", " + str(space) + extension,
                bilblur)
    print("Bilateral blurred with " + str(d) + ", " + str(color) + ", " + str(space))


def morphops(dirName, extension, image, shift):
    kernal = np.ones((shift, shift), dtype=np.uint8)
    erodedimage = cv2.erode(image, kernal, iterations=1)
    cv2.imwrite(dirName + "/Eroded-" + " (" + str(shift) + str(shift) + ")" + extension, erodedimage)
    dilatedimage = cv2.dilate(image, kernal, iterations=1)
    cv2.imwrite(dirName + "/Dilated-" + " (" + str(shift) + str(shift) + ")" + extension, dilatedimage)
    openedimage = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernal)
    cv2.imwrite(dirName + "/Opened-" + " (" + str(shift) + str(shift) + ")" + extension, openedimage)
    closedimage = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernal)
    cv2.imwrite(dirName + "/Closed-" + " (" + str(shift) + str(shift) + ")" + extension, closedimage)
    morphgradim = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernal)
    cv2.imwrite(dirName + "/Morphological gradient-" + " (" + str(shift) + str(shift) + ")" + extension, morphgradim)


def skelotonize(dirName, extention, image):
    imagegray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    size = np.size(imagegray)
    skel = np.zeros(imagegray.shape, np.uint8)
    ret, imagegray = cv2.threshold(imagegray, 127, 255, 0)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    a = False
    while(not a):
        eroded = cv2.erode(imagegray, element)
        temp = cv2.dilate(eroded,element)
        temp = cv2.subtract(imagegray,temp)
        skel = cv2.bitwise_or(skel,temp)
        imagegray = eroded.copy()
        zeros = size - cv2.countNonZero(imagegray)
        if zeros == size:
            a = True

    cv2.imwrite(dirName+"/Skelotonize"+extention, skel)
    print("Done with skelotonizing")


def morphop2(dirName, extension, image, shift):
    kernal = np.ones((shift, shift), dtype=np.uint8)
    tophat = cv2.morphologyEx(image, cv2.MORPH_TOPHAT, kernal)
    cv2.imwrite(dirName + "/Top Hat-" + " (" + str(shift) + str(shift) + ")" + extension, tophat)
    blackhat = cv2.morphologyEx(image, cv2.MORPH_BLACKHAT, kernal)
    cv2.imwrite(dirName + "/Black Hat-" + " (" + str(shift) + str(shift) + ")" + extension, blackhat)


def sharpenimage(dirName, extension, image):
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
    cv2.imwrite(dirName + "/Sharpen-Outward" + extension, image_outward)
    print("Sharpened with outward edges")
    cv2.imwrite(dirName + "/Sharpen-Inward" + extension, image_inward)
    print("Sharpened with inward edges")


def embossimage(dirName, extension, image):
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
    cv2.imwrite(dirName + "/Embossed1" + extension, im1)
    im2 = cv2.filter2D(image, -1, kernal2)
    cv2.imwrite(dirName + "/Embossed2" + extension, im2)
    im3 = cv2.filter2D(image, -1, kernal3)
    cv2.imwrite(dirName + "/Embossed3" + extension, im3)
    im4 = cv2.filter2D(image, -1, kernal4)
    cv2.imwrite(dirName + "/Embossed4" + extension, im4)
    im5 = cv2.filter2D(image, -1, kernal5)
    cv2.imwrite(dirName + "/Embossed5" + extension, im5)
    im6 = cv2.filter2D(image, -1, kernal6)
    cv2.imwrite(dirName + "/Embossed6" + extension, im6)
    total = im1 + im2 + im3 + im4 + im5 + im6
    cv2.imwrite(dirName + "/Embossing_total" + extension, total)
    print("Done with Embossing")


def edges(dirName, extension, image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Sobel
    for i in range(1, 10, 2):
        sobelx = cv2.Sobel(image, cv2.CV_16U, 1, 0, ksize=i)
        cv2.imwrite(dirName + "/Sobel_x" + str(i) + extension, sobelx)
        sobely = cv2.Sobel(image, cv2.CV_16U, 0, 1, ksize=i)
        cv2.imwrite(dirName + "/Sobel_y" + str(i) + extension, sobely)
        total_sobel = sobelx + sobely
        cv2.imwrite(dirName + "/Sobel_total" + extension, total_sobel)
        print("Done with Sobel's operator")

    # Scharr
    scharrx = cv2.Scharr(image, -1, 1, 0)
    cv2.imwrite(dirName + "/Scharr_x" + extension, scharrx)
    scharry = cv2.Scharr(image, -1, 0, 1)
    cv2.imwrite(dirName + "/Scharr_y" + extension, scharry)
    total_scharr = scharrx + scharry
    cv2.imwrite(dirName + "/Scharr_total" + extension, total_scharr)
    print("Done with Scharr's operator")

    # Robert
    kernal1 = np.array([
        [1, 0],
        [0, -1]
    ])
    kernal2 = np.array([
        [0, 1],
        [-1, 0]
    ])
    robert1 = cv2.filter2D(image, -1, kernal1)
    cv2.imwrite(dirName + "/Robert1" + extension, robert1)
    robert2 = cv2.filter2D(image, -1, kernal2)
    cv2.imwrite(dirName + "/Robert2" + extension, robert2)
    total_robert = robert1 + robert2
    cv2.imwrite(dirName + "/Robert_total" + extension, total_robert)
    print("Done with Robert's operator")

    # Canny
    canny1 = cv2.Canny(image, 100, 200)
    cv2.imwrite(dirName + "/Canny1" + extension, canny1)
    canny2 = cv2.Canny(image, 200, 400)
    cv2.imwrite(dirName + "/Canny2" + extension, canny2)
    canny3 = cv2.Canny(image, 300, 600)
    cv2.imwrite(dirName + "/Canny3" + extension, canny3)
    print("Done with Canny's operator")

    # Prewitt
    prewittx = np.array([
        [1, 0, -1],
        [1, 0, -1],
        [1, 0, -1]
    ])
    prewitty = np.array([
        [1, 1, 1],
        [0, 0, 0],
        [-1, -1, -1]
    ])

    prx = cv2.filter2D(image, -1, prewittx)
    cv2.imwrite(dirName + "/Prewitt_x" + extension, prx)
    pry = cv2.filter2D(image, -1, prewitty)
    cv2.imwrite(dirName + "/Prewitt_y" + extension, pry)
    total_prewitt = prx + pry
    cv2.imwrite(dirName + "/Prewitt_total" + extension, total_prewitt)
    print("Done with Prewitt's operator")

    # Kirsh
    north = np.array([
        [-3, -3, 5],
        [-3, 0, 5],
        [-3, -3, 5]
    ])
    imnorth = cv2.filter2D(image, -1, north)
    north_west = np.array([
        [-3, 5, 5],
        [-3, 0, 5],
        [-3, -3, -3]
    ])
    imnorthwest = cv2.filter2D(image, -1, north_west)
    north_east = np.array([
        [-3, -3, -3],
        [-3, 0, 5],
        [-3, 5, 5]
    ])
    imnortheast = cv2.filter2D(image, -1, north_east)
    south = np.array([
        [5, -3, -3],
        [5, 0, -3],
        [5, -3, -3]
    ])
    imsouth = cv2.filter2D(image, -1, south)
    south_west = np.array([
        [5, 5, -3],
        [5, 0, -3],
        [-3, -3, -3]
    ])
    imsouthwest = cv2.filter2D(image, -1, south_west)
    south_east = np.array([
        [-3, -3, -3],
        [5, 0, -3],
        [5, 5, -3]
    ])
    imsoutheast = cv2.filter2D(image, -1, south_east)
    west = np.array([
        [5, 5, 5],
        [-3, 0, -3],
        [-3, -3, -3]
    ])
    imwest = cv2.filter2D(image, -1, west)
    east = np.array([
        [-3, -3, -3],
        [-3, 0, -3],
        [5, 5, 5]
    ])
    imeast = cv2.filter2D(image, -1, east)

    cv2.imwrite(dirName + "/Kirsh_N" + extension, imnorth)
    cv2.imwrite(dirName + "/Kirsh_NE" + extension, imnortheast)
    cv2.imwrite(dirName + "/Kirsh_NW" + extension, imnorthwest)
    cv2.imwrite(dirName + "/Kirsh_S" + extension, imsouth)
    cv2.imwrite(dirName + "/Kirsh_SE" + extension, imsoutheast)
    cv2.imwrite(dirName + "/Kirsh_SW" + extension, imsouthwest)
    cv2.imwrite(dirName + "/Kirsh_W" + extension, imwest)
    cv2.imwrite(dirName + "/Kirsh_E" + extension, imeast)
    total_kirsh = imnorth + imsouth + imeast + imwest + imsouthwest + imsoutheast + imnorthwest + imnortheast
    cv2.imwrite(dirName + "/Kirsh_total" + extension, total_kirsh)
    print("Done with Kirsh's operator")


def colorconv(dirName, extension, image):
    grayimage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(dirName + "/Grayimage" + extension, grayimage)
    hsvimage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    cv2.imwrite(dirName + "/HSVimage" + extension, hsvimage)
    Ycrcbimage = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    cv2.imwrite(dirName + "/YCrCbimage" + extension, Ycrcbimage)
    labimage = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    cv2.imwrite(dirName + "/LABimage" + extension, labimage)
    hlsimage = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
    cv2.imwrite(dirName + "/HLSimage" + extension, hlsimage)
    luvimage = cv2.cvtColor(image, cv2.COLOR_BGR2LUV)
    cv2.imwrite(dirName + "/LUVimage" + extension, luvimage)
    rgbimage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.imwrite(dirName + "/RGBimage" + extension, rgbimage)
    rgbaimage = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
    cv2.imwrite(dirName + "/RGBAimage" + extension, rgbaimage)
    yuvimage = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    cv2.imwrite(dirName + "/YUVimage" + extension, yuvimage)
    print("Done with color conversions")


def adgaunoise(dirName, extension, image):
    # Adaptive gaussian noise
    h, s, v = cv2.split(image)
    s = cv2.adaptiveThreshold(s, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    h = cv2.adaptiveThreshold(h, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    v = cv2.adaptiveThreshold(v, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    agimage = cv2.merge([h, s, v])
    cv2.imwrite(dirName + "/AdaGauNoise" + extension, agimage)
    print("Done with adaptive Gaussain")


def sandpnoise(dirName, extension, image, prob):
    op = np.zeros(image.shape, np.uint8)
    thresh = 1 - prob
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                op[i][j] = 0
            elif rdn > thresh:
                op[i][j] = 255
            else:
                op[i][j] = image[i][j]
    cv2.imwrite(dirName + "/Salt and pepper noise" + extension, op)
    print("Salt and Pepper added with prob" + str(prob))


def poissonnoise(dirName, extension, image):
    value = len(np.unique(image))
    value = 2 ** np.ceil(np.log2(value))
    noisy = np.random.poisson(image * value) / float(value)
    noisy = noisy + image
    cv2.imwrite(dirName + "/Poisson noise" + extension, noisy)
    print("Done with Poisson noise")


def specklenoise(dirName, extension, image):
    row, col, ch = image.shape
    gauss = np.random.randn(row, col, ch)
    gauss = gauss.reshape(row, col, ch)
    noisy = image + image * gauss
    cv2.imwrite(dirName + "/Speckle" + extension, noisy)
    print("Done with speckle noise")


def contrastimage(dirName, extension, image, contrast):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    image[:, :, 2] = [[max(pixel - contrast, 0) if pixel < 190 else min(pixel + contrast, 255)
                       for pixel in row] for row in image[:, :, 2]]
    image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
    cv2.imwrite(dirName + "/Contrast-" + str(contrast) + extension, image)
    print("Contrasted with-" + str(contrast))


def scaleimage(dirName, extension, image, fx, fy):
    image = cv2.resize(image, None, fx=fx, fy=fy, interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(dirName + "/Scaled-" + " (" + str(fx) + str(fy) + ")" + extension, image)
    print("Done scaling with- " + "(" + str(fx) + str(fy) + ")")


def translateimage(dirName, extension, image, x, y):
    rows, cols, c = image.shape
    M = np.float32([[1, 0, x], [0, 1, y]])
    image = cv2.warpAffine(image, M, (cols, rows))
    cv2.imwrite(dirName + "/Translated-" + " (" + str(x) + str(y) + ")" + extension, image)
    print("Translated with-" + " (" + str(x) + str(y) + ")")


def rotateimage(dirName, extension, image, deg):
    rows, cols, c = image.shape
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), deg, 1)
    image = cv2.warpAffine(image, M, (cols, rows))
    cv2.imwrite(dirName + "/Rotated-" + str(deg) + extension, image)
    print("Rotated with " + str(deg) + "degrees")


def transform_image(dirName, extension, image):
    rows, cols, ch = image.shape
    pts1 = np.float32([[50, 50], [200, 50], [50, 200]])
    pts2 = np.float32([[10, 100], [200, 50], [100, 250]])
    M = cv2.getAffineTransform(pts1, pts2)
    image = cv2.warpAffine(image, M, (cols, rows))
    cv2.imwrite(dirName + "/Transformation-" + str(1) + extension, image)

    pts1 = np.float32([[50, 50], [200, 50], [50, 200]])
    pts2 = np.float32([[100, 10], [200, 50], [0, 150]])
    M = cv2.getAffineTransform(pts1, pts2)
    image = cv2.warpAffine(image, M, (cols, rows))
    cv2.imwrite(dirName + "/Transformation-" + str(2) + extension, image)

    pts1 = np.float32([[50, 50], [200, 50], [50, 200]])
    pts2 = np.float32([[100, 10], [200, 50], [30, 175]])
    M = cv2.getAffineTransform(pts1, pts2)
    image = cv2.warpAffine(image, M, (cols, rows))
    cv2.imwrite(dirName + "/Transformation-" + str(3) + extension, image)

    pts1 = np.float32([[50, 50], [200, 50], [50, 200]])
    pts2 = np.float32([[100, 10], [200, 50], [70, 150]])
    M = cv2.getAffineTransform(pts1, pts2)
    image = cv2.warpAffine(image, M, (cols, rows))
    cv2.imwrite(dirName + "/Transformation-" + str(4) + extension, image)
    print("Done with transformations")


def superpixel(dirName, extention, image, segments):
    seg = segments

    def segment(image, mask):
        (B, G, R) = cv2.split(image.astype("float"))
        R = np.ma.masked_array(R, mask=mask)
        G = np.ma.masked_array(G, mask=mask)
        B = np.ma.masked_array(B, mask=mask)

        rg = np.absolute(R - G)
        yb = np.absolute(0.5 * (R + G) - B)

        stdRoot = np.sqrt((rg.std() ** 2) + (yb.std() ** 2))
        meanRoot = np.sqrt((rg.mean() ** 2) + (yb.mean() ** 2))

        return stdRoot + (0.3 * meanRoot)

    orig = image
    vis = np.zeros(orig.shape[:2], dtype="float")
    # image = io.imread(image)
    segments = slic(img_as_float(image), n_segments=segments,
                    slic_zero=True)
    for v in np.unique(segments):
        mask = np.ones(image.shape[:2])
        mask[segments == v] = 0

        C = segment(orig, mask)
        vis[segments == v] = C

    vis = rescale_intensity(vis, out_range=(0, 255)).astype("uint8")

    alpha = 0.6
    overlay = np.dstack([vis] * 3)
    output = orig.copy()
    cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)
    cv2.imwrite(dirName + "/superpixels-" + str(seg) + extention, output)
    print("Done with superpixels")

def histeq(dirName, extention, image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    histeqimage = cv2.equalizeHist(img)
    cv2.imwrite(dirName + "/Histogram_equalized" + extention, histeqimage)
    print("Done with Histogram Equalization")


def affine(dirName, extention, image, angle):
    srcTri = np.array( [[0, 0], [image.shape[1] - 1, 0], [0, image.shape[0] - 1]] ).astype(np.float32)
    dstTri = np.array( [[0, image.shape[1]*0.33], [image.shape[1]*0.85, image.shape[0]*0.25],
                        [image.shape[1]*0.15, image.shape[0]*0.7]] ).astype(np.float32)
    warp_mat = cv2.getAffineTransform(srcTri, dstTri)
    warp_dst = cv2.warpAffine(image, warp_mat, (image.shape[1], image.shape[0]))
    # Rotating the image after Warp
    center = (warp_dst.shape[1]//2, warp_dst.shape[0]//2)
    angle = angle
    scale = 1
    rot_mat = cv2.getRotationMatrix2D( center, angle, scale )
    warp_rotate_dst = cv2.warpAffine(warp_dst, rot_mat, (warp_dst.shape[1], warp_dst.shape[0]))
    cv2.imwrite(dirName+"/Warp"+extention, warp_dst)
    cv2.imwrite(dirName+"/Warp&Rotate"+str(angle)+str(scale)+extention, warp_rotate_dst)
    print("Done with affine transforms")


def callall(dirName, extension, image):
    # print("in call all")
    resizeimage(dirName, extension, image, 400, 400)
    resizeimage(dirName, extension, image, 350, 300)
    resizeimage(dirName, extension, image, 100, 150)
    resizeimage(dirName, extension, image, 350, 200)
    resizeimage(dirName, extension, image, 300, 100)
    resizeimage(dirName, extension, image, 250, 140)
    resizeimage(dirName, extension, image, 200, 200)
    resizeimage(dirName, extension, image, 100, 100)
    resizeimage(dirName, extension, image, 200, 160)
    resizeimage(dirName, extension, image, 350, 200)
    resizeimage(dirName, extension, image, 200, 450)
    resizeimage(dirName, extension, image, 500, 500)
    resizeimage(dirName, extension, image, 440, 420)
    resizeimage(dirName, extension, image, 200, 380)
    resizeimage(dirName, extension, image, 180, 200)
    resizeimage(dirName, extension, image, 380, 330)

    print("Done resizing")
    # Customize padding here
    padimage(dirName, extension, image, 100, 0, 0, 0)
    padimage(dirName, extension, image, 0, 100, 0, 0)
    padimage(dirName, extension, image, 0, 0, 100, 0)
    padimage(dirName, extension, image, 0, 0, 0, 100)
    padimage(dirName, extension, image, 100, 100, 0, 0)
    padimage(dirName, extension, image, 0, 100, 100, 0)
    padimage(dirName, extension, image, 0, 0, 100, 100)
    padimage(dirName, extension, image, 100, 0, 100, 0)
    padimage(dirName, extension, image, 0, 100, 0, 100)
    padimage(dirName, extension, image, 200, 0, 0, 0)
    padimage(dirName, extension, image, 0, 200, 0, 0)
    padimage(dirName, extension, image, 0, 0, 200, 0)
    padimage(dirName, extension, image, 0, 0, 0, 200)
    padimage(dirName, extension, image, 200, 200, 0, 0)
    padimage(dirName, extension, image, 0, 200, 200, 0)
    padimage(dirName, extension, image, 0, 0, 200, 200)
    padimage(dirName, extension, image, 200, 0, 200, 0)
    padimage(dirName, extension, image, 0, 200, 0, 200)
    print("Done padding")
    # Customize cropping here
    cropimage(dirName, extension, image, 100, 400, 0, 350)
    cropimage(dirName, extension, image, 100, 400, 100, 450)
    cropimage(dirName, extension, image, 0, 300, 0, 350)
    cropimage(dirName, extension, image, 0, 300, 100, 450)
    cropimage(dirName, extension, image, 100, 300, 100, 350)

    print("Done cropping")
    flipimage(dirName, extension, image, 0)  # horizontal
    flipimage(dirName, extension, image, 1)  # vertical
    flipimage(dirName, extension, image, -1)  # both

    print("Done flipping")
    for i in range(0, 255, 25):
        print(i)
        invertimage(dirName, extension, image, i)
        saturateimage(dirName, extension, image, i)
        hueimage(dirName, extension, image, i)
    print("Done invering, saturating and huing")

    for i in seq(1, 6, 0.1):
        gammacorrection(dirName, extension, image, i)

    print("Done Gamma Correcting")
    for i in range(0, 255, 50):
        for j in seq(1, 5, 0.8):
            add_light_color(dirName, extension, image, i, j)

    print("Done Adding light and color")

    for x in seq(0.1, 1, 0.2):
        for y in seq(0.1, 1, 0.2):
            for z in seq(0.1, 1, 0.2):
                multiplywith(dirName, extension, image, x, y, z)

    print("Done with multiplication")

    for t in seq(0, 5, 0.5):
        gaussianblur(dirName, extension, image, t)

    print("Done with Gaussian Blur")

    for t in range(1, 12, 1):
        avgblur(dirName, extension, image, t)

    print("Done with Average Blur")

    for c in range(1, 13, 2):
        medblur(dirName, extension, image, c)

        print("Done with Median Blur")

        morphops(dirName, extension, image, 2)
        morphop2(dirName, extension, image, 100)
        morphops(dirName, extension, image, 3)
        morphop2(dirName, extension, image, 150)
        morphops(dirName, extension, image, 4)
        morphop2(dirName, extension, image, 200)

        print("Done with Morphological operation set 1 & 2")

        bilblur(dirName, extension, image, 9, 75, 75)
        bilblur(dirName, extension, image, 12, 100, 100)
        bilblur(dirName, extension, image, 25, 100, 100)
        bilblur(dirName, extension, image, 40, 75, 75)
        bilblur(dirName, extension, image, 50, 100, 100)
        bilblur(dirName, extension, image, 50, 75, 75)

        print("Done with Bilateral Blur")

        sharpenimage(dirName, extension, image)
        print("Done with sharpening")
        embossimage(dirName, extension, image)
        print("Done with Embossing")
        edges(dirName, extension, image)
        print("Done with Edge operations")
        colorconv(dirName, extension, image)
        print("Done with Color Convertion")
        adgaunoise(dirName, extension, image)
        print("Done with Adaptive Gaussian Noise")
        sandpnoise(dirName, extension, image, 0.05)
        sandpnoise(dirName, extension, image, 0.08)
        sandpnoise(dirName, extension, image, 0.02)
        sandpnoise(dirName, extension, image, 0.04)
        print("Done with Salt and Pepper Noise")
        poissonnoise(dirName, extension, image)
        print("Done with Poisson Noise")
        specklenoise(dirName, extension, image)
        print("Done with Speckle Noise")

    for i in range(0, 125, 25):
        contrastimage(dirName, extension, image, i)

    print("Done with Contrast Changes")

    for i in seq(1, 4, 1):
        for j in seq(1, 4, 1):
            scaleimage(dirName, extension, image, i, j)

    print("Done with Scaling Operations")

    for s in range(0, 360, 90):
            rotateimage(dirName, extension, image, s)

    print("Done with Image Rotation Operations")
    translateimage(dirName, extension, image, 150, 150)
    translateimage(dirName, extension, image, -150, 150)
    translateimage(dirName, extension, image, 150, -150)
    translateimage(dirName, extension, image, -150, -150)
    print("Done with Translation Operations")

    superpixel(dirName, extension, image, 50)
    superpixel(dirName, extension, image, 100)
    superpixel(dirName, extension, image, 150)
    superpixel(dirName, extension, image, 200)
    superpixel(dirName, extension, image, 255)
    superpixel(dirName, extension, image, 75)
    superpixel(dirName, extension, image, 125)
    print("Done with SuperPixel")

    histeq(dirName, extension, image)
    print("Done with Histogram equalization")
    skelotonize(dirName, extension, image)
    print("Done with Skelonotizing")

    for x in range(0, 360, 30):
        affine(dirName, extension, image, x)
    print("Done with Affine Transformations")