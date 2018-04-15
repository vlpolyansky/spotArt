import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
import pandas as pd
from tinydb import TinyDB, Query
import shutil


def add_photo(filename, description, location=None):
    sift = cv2.xfeatures2d.SIFT_create()
    image = cv2.imread(filename)
    image = cv2.resize(image, (0, 0), fx=0.2, fy=0.2)
    image = cv2.GaussianBlur(image, (5, 5), 0)
    kp1, des1 = sift.detectAndCompute(image, None)

    data = pd.read_csv('NMS_Data.csv')

    best_i = -1
    best_good = 0
    avg_good = 0
    cnt = 0

    for i in range(len(data)):
        code = data['artifact.defaultMediaIdentifiers'][i]
        filename2 = 'Artwork_Subset/' + code + '.jpg'
        if not os.path.exists(filename2):
            continue
        image2 = cv2.imread(filename2)
        kp2, des2 = sift.detectAndCompute(image2, None)

        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)

        good = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good.append([m])
        print code, len(good)
        avg_good += len(good)
        cnt += 1
        if best_good < len(good):
            best_i = i
            best_good = len(good)

        # # TEMP
        # img3 = cv2.drawMatchesKnn(image, kp1, image2, kp2, good, None, flags=2)
        # # plt.imshow(cv2.cvtColor(img3, cv2.COLOR_BGR2RGB)), plt.show()
        # plt.imsave('frames/' + str(cnt) + '.png', cv2.cvtColor(img3, cv2.COLOR_BGR2RGB))

    if best_good > 5 * (avg_good / cnt):
        pass
    else:
        best_i = -1

    if best_i >= 0:
        db = TinyDB('paintings/db.json')
        image_file = data['artifact.defaultMediaIdentifiers'][best_i] + '.jpg'
        test = Query()
        if len(db.search(test.img == image_file)) == 0:
            shutil.copyfile('Artwork_Subset/' + image_file, 'paintings/' + image_file)
            db.insert({'name': data['artifact.ingress.titles'][best_i],
                       'img': image_file})
            print 'New entry added!'
        else:
            print 'Already exists...'


if __name__ == '__main__':
    add_photo('Museum_images_subset/IMG_20180415_052951.jpg', 'NAME')
