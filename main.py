from transform import four_point_transform
from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2
import imutils


def main():
    #arguments need to be parsed hence we construct the argument parser
    ap = argparse.ArgumentParser()
    ap.add_argument("-i","--image",required=True,help="Path to the image that is to be scanned")
    args = vars(ap.parse_args())

    #now lets read the image from the parsed argument and then use that

    img= cv2.imread(args["image"])
    ratio = img.shape[0]/500.0
    og = img.copy()
    img= imutils.resize(img,height = 500)

    #convt image to grayscale and then we blur the image and then we detect the edges
    gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blurred= cv2.GaussianBlur(gray,(9,9),10)
    gray= cv2.addWeighted(gray,1.5,blurred,-0.5,0)
    edge= cv2.Canny(gray,75,200)

    cv2.imshow("Image",img)
    cv2.imshow("edges",edge)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()
