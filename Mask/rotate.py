import cv2
import numpy as np
import sys

def crop_minAreaRect(img, rect):

    # rotate img
    angle = rect[2]
    rows,cols = img.shape[0], img.shape[1]
    M = cv2.getRotationMatrix2D((cols/2,rows/2),angle,1)
    img_rot = cv2.warpAffine(img,M,(cols,rows))

    # rotate bounding box
    rect0 = (rect[0], rect[1], 0.0)
    box = cv2.boxPoints(rect)
    pts = np.int0(cv2.transform(np.array([box]), M))[0]    
    pts[pts < 0] = 0

    # crop
    img_crop = img_rot[pts[1][1]:pts[0][1], 
                       pts[1][0]:pts[2][0]]

    return img_crop

def crop_image(img,tol=0):
    # img is image data
    # tol  is tolerance
    mask = img>tol
    return img[np.ix_(mask.any(1),mask.any(0))]
def main():
    # generate image
    img = cv2.imread(sys.argv[1], 0)
    orgimg= cv2.imread(sys.argv[1],cv2.COLOR_BGR2RGB)

    # find contours / rectangle
    _,contours,_ = cv2.findContours(img, 1, 1)
    rect = cv2.minAreaRect(contours[0])

    # crop
    img_croped = crop_minAreaRect(orgimg, rect)
    #imgGray = crop_minAreaRect(img, rect);

    # crop few drak
    #img_croped2 = crop_image(imgGray, 0)

    cv2.imwrite('FinalResult.png', img_croped[5:-5, 5:-5, :]);

if __name__ == "__main__":
    main()
