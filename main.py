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
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    gray= cv2.addWeighted(gray,1.7,blurred,-0.5,0)

    #different method where we perform thresholding by adaptive thresholding
    #  Adaptive thresholding with larger block size (better for big objects)
    # thresh = cv2.adaptiveThreshold(
    #     gray, 255,
    #     cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    #     cv2.THRESH_BINARY_INV,  # Use binary inverse to highlight dark on light
    #     35, 15  # ← larger blockSize & C to focus on broad regions
    # )


    edge= cv2.Canny(gray,75,200)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    edge = cv2.morphologyEx(edge, cv2.MORPH_CLOSE, kernel)

    #Now lets detect the largest contours of the image
    contrs= cv2.findContours(edge.copy(),cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contrs= imutils.grab_contours(contrs)
    contrs= sorted(contrs,key=cv2.contourArea,reverse=True)[:5]

    #Here we loop over the contours
    l=[]
    for c in contrs:
        #approx the contour
        perimeter= cv2.arcLength(c,True)
        approx= cv2.approxPolyDP(c,0.02*perimeter,True)
        #lets save the first contour that has a size of 4 
        
        if len(approx)==4:
            screenContr= approx
            break
        else:
            l.append(c)
   # Inside the main() function, after the for-loop
    if 'screenContr' not in locals():
        print("No contour with 4 points found.")
        for i in l:
            if len(i)>4:
                screenContr=i
                break
        

    # Just to be extra safe
    cv2.drawContours(img, [screenContr.reshape(-1, 1, 2)], -1, (0, 255, 0), 2)
    
    #we will apply fourpointtransform tom obtain a topdown view of the image
    warped= four_point_transform(og,screenContr.reshape(4,2)*ratio)

    warped= cv2.cvtColor(warped,cv2.COLOR_BGR2GRAY)

    T = threshold_local(warped,11,offset=10,method="gaussian")
    warped=(warped>T).astype("uint8")*255

    cv2.imshow("original",imutils.resize(og,height=650))
    cv2.imshow("scanned",imutils.resize(warped,height=650))
    


    cv2.waitKey(0)
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()
