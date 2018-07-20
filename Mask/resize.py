import cv2
import numpy as np,sys
def main():
    image = cv2.imread(sys.argv[1])
    resized = cv2.resize(image, (640, 480))
    cv2.imwrite(sys.argv[1],resized)

if __name__ == "__main__":
    main()
