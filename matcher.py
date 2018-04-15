import cv2
import numpy as np
import os
from matplotlib import pyplot as plt

sift = cv2.xfeatures2d.SIFT_create()


def match(img1, img2):
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)
    return match(img1, img2, kp1, des1, kp2, des2)


def match(img1, img2, kp1, des1, kp2, des2):

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append([m])

    img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, None, flags=2)

    plt.imshow(cv2.cvtColor(img3, cv2.COLOR_BGR2RGB)), plt.show()


def main():
    img_photo = cv2.imread('Museum_Images/IMG_20180415_024946.jpg')
    kp1, des1 = sift.detectAndCompute(img_photo, None)
    for fname in os.listdir('Artwork'):
        img_art = cv2.imread('Artwork/' + fname)
        kp2, des2 = sift.detectAndCompute(img_art, None)
        match(img_photo, img_art, kp1, des1, kp2, des2)
    # match(img_photo, img_true)
    # match(img_photo, img_false)


if __name__ == '__main__':
    main()
