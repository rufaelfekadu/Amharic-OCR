# import the necessary packages
from PIL import Image
import pytesseract
import argparse
import cv2
import time
import os

# # construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image",
#                 help="path to input image to be OCR'd",type=str,default="images/image1.png")
# ap.add_argument("-p", "--preprocess", type=str, default="thresh",
#                 help="type of preprocessing to be done")
# args = vars(ap.parse_args())

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# load the example image and convert it to grayscale

def ocr(image):
    start2 = time.time()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # check to see if we should apply thresholding to preprocess the
    # image

    gray = cv2.threshold(gray, 0, 255,
                         cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # make a check to see if median blurring should be done to remove
    # noise

    # gray = cv2.medianBlur(gray, 3)
    # write the grayscale image to disk as a temporary file so we can
    # apply OCR to it
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)

    # load the image as a PIL/Pillow image, apply OCR, and then delete
    # the temporary file
    start = time.time()
    text = pytesseract.image_to_string(Image.open(filename), lang='amh')
    end = time.time()
    print("inference", (end - start))
    os.remove(filename)
    return text

# print(text)
# # show the output images
# cv2.imshow("Image", image)
# cv2.imshow("Output", gray)
# cv2.waitKey(0)
