import cv2
import numpy as np 
from matplotlib import pyplot as plt 

img_rgb = cv2.imread('full.png')

img_gray = cv2.cvtColor(img_rgb,cv2.COLOR_BGR2GRAY)
cv2.imshow('gray',img_gray)

template = cv2.imread("whitePiece.png",0)
h,w = template.shape[::]
#print(h,w)

res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED) #cv2.TM_SQDIFF-ennel a minimumnal van a legjobb talalat, tobbinema max-nal
                                                                #min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
# plt.imshow(res,cmap='gray')
cv2.imshow('res',res)
cv2.waitKey()

threshold = 0.79
#print(res)
loc = np.where(res>= threshold)

for pt in zip(*loc[::-1]):
    cv2.rectangle(img_rgb,pt,(pt[0]+w,pt[1]+h),(0,0,255),2)

cv2.imshow('Azonositott Feherek',img_rgb)
cv2.waitKey()
cv2.destroyAllWindows()

