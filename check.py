
import collections
import pyautogui
import os
from PIL import Image
import numpy as np
from skimage.metrics import structural_similarity as ssim
import cv2
import matplotlib.pyplot as plt
# import subprocess
import glob


def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err


def check(a, b):
    
    print(a)
    print(b)

    max_ = 0

    plt.figure(figsize=(10, 5))
    
    for y in a:
        for x in b:
            plt.clf()

            imageA = Image.open(x) 
            imageB = Image.open(y)

            imageA = cv2.cvtColor(np.array(imageA), cv2.COLOR_RGB2BGR)
            imageB = cv2.cvtColor(np.array(imageB), cv2.COLOR_RGB2BGR)

            plt.subplot(1, 2, 1)
            plt.imshow(imageB)
            plt.title('Image 1')

            plt.subplot(1, 2, 2)
            plt.imshow(imageA)
            plt.title('Image 2')

            m = mse(imageA, imageB)
            # s = ssim(im, imageB)
            s = 0
            # print(f"MSE: %.2f, SSIM: %.2f" % (m, s))
            
   
            if 1000 < m:
                plt.show()
            

            max_ = max(max_, m)
    
    print(f"mse: {int(max_)}")

check(glob.glob(os.path.join("images", "a1", "*")), glob.glob(os.path.join("images", "a1.bmp")))
check(glob.glob(os.path.join("images", "a2", "*")), glob.glob(os.path.join("images", "a2.bmp")))
check(glob.glob(os.path.join("images", "a3", "*")), glob.glob(os.path.join("images", "a3.bmp")))
check(glob.glob(os.path.join("images", "a4", "*")), glob.glob(os.path.join("images", "a4.bmp")))
check(glob.glob(os.path.join("images", "a5", "*")), glob.glob(os.path.join("images", "a5.bmp")))
check(glob.glob(os.path.join("images", "a6", "*")), glob.glob(os.path.join("images", "a6.bmp")))
check(glob.glob(os.path.join("images", "a7", "*")), glob.glob(os.path.join("images", "a7.bmp")))
check(glob.glob(os.path.join("images", "a8", "*")), glob.glob(os.path.join("images", "a8.bmp")))
check(glob.glob(os.path.join("images", "a9", "*")), glob.glob(os.path.join("images", "a9.bmp")))
