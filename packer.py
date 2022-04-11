import cv2 as cv
import numpy as np
import os
import re
from numpy.lib.utils import who

padding = 10

def findCommonName(names):
    commonName = ''
    for j in range(len(names[0])):
        allSame = True
        for i in range(1,len(names)):
            if(names[i][j] != names[0][j]):
                allSame = False
            
        if(allSame):
                commonName += names[0][j]
        else:
            break
    return commonName

def findSides(h,w,n):
    r = h/w
    nX = np.sqrt(n*r)
    nY = np.sqrt(n/r)

    return (int(np.ceil(nY)),int(np.ceil(nX)))

wholeImage = []
outputFile = ''

for dirname, _, filenames in os.walk('.'):
    images = list(filter(lambda x: (x.find('.png') != -1) and (x.find('_packed.png') == -1), filenames))
    #test = cv.imread(images[0], cv.IMREAD_UNCHANGED)
    print(images)
    test = cv.imdecode(np.fromfile(images[0], dtype=np.uint8), cv.IMREAD_UNCHANGED)
    (h,w,_) = test.shape

    nY,nX = findSides(test.shape[0], test.shape[1], len(images))

    wholeImage = np.zeros(((test.shape[0] + padding)*nY + padding, (test.shape[1] + padding)*nX + padding, test.shape[2]))

    outputFile = findCommonName(images) +'_'+ str(nX) +'_'+ str(nY) +'_'+ str(np.maximum(wholeImage.shape[0], wholeImage.shape[1])) + '_packed.png'
    for i in range(len(images)): 
        #img = cv.imread(images[i], cv.IMREAD_UNCHANGED)
        img = cv.imdecode(np.fromfile(images[i], dtype=np.uint8), cv.IMREAD_UNCHANGED)
        yOffset = (test.shape[0] + padding) * int(np.floor(i/nX)) + padding
        xOffset = (test.shape[1] + padding) * (i%(nX)) + padding
        try:
            wholeImage[yOffset:yOffset+img.shape[0],xOffset:xOffset+img.shape[1]] = img
        except:
            print(wholeImage.shape)
            print('(' + str(yOffset) + ':' + str(yOffset+img.shape[0]) + ',' + str(xOffset) + ':' + str(xOffset+img.shape[1]) + ')')

cv.imwrite( re.sub('[^a-zA-Z0-9 \n\.]', '', outputFile), wholeImage)