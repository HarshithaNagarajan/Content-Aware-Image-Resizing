import cv2
from End_Sem_Project.content_aware_resizing import CAIR


def main():
    filename = "boat1.jpg"
    img = cv2.imread(filename)

    img = cv2.resize(img, (300,500))
    # cv2.imshow('f',img)
    # cv2.waitKey(0)

    obj = CAIR(img, 0.8)
    #resized = obj.findHorizontalSeam()

    #resized = obj.reduceWidth()
    #resized = obj.reduceHeight()

    resized = obj.increaseWidth()
    cv2.imshow('Final Image', resized)
    cv2.waitKey(0)

    # outfile = "output.jpg"
    # cv2.imwrite(outfile, resized)


if __name__ == '__main__':
    main()


