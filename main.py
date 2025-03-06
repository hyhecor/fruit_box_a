
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

Box = collections.namedtuple('Box', 'left top width height')
Point = collections.namedtuple('Point', 'x y')

def TopLeft() -> str:
    return "images/TopLeft.bmp"

def BottomRight() -> str:
    return "images/BottomRight.bmp"

def btnPlay_click(screen: Box):
    dp =  pyautogui.position()

    p = Point(screen.left + 200, screen.top + 250)
    pyautogui.click(x= p.x, y= p.y)

    pyautogui.moveTo(x= dp.x, y= dp.y)

def mouseMove_default(screen: Box):
    pyautogui.moveTo(x= screen.left, y= screen.top)

def screenshot(region: Box, file: str, dump=False):
    region_ = (
        int(region.left), 
        int(region.top), 
        int(region.width), 
        int(region.height))
    im = pyautogui.screenshot(region= region_)
   
    if dump:
        im.save(file)

    return im

def crop(image: Image.Image, region: Box) -> Image.Image:
    region_ =(int(region.left), 
          int(region.top), 
          int(region.left + region.width), 
          int(region.top + region.height))
    im = image.crop(box= region_)

    return im

def TempDir(subpath="")-> str:
    return os.path.join("temp", subpath) 

def ImagesDir(subpath="")-> str:
    return os.path.join("images", subpath) 

# subprocess.run(["cmd", "start https://www.gamesaien.com/game/fruit_box_a/"])

topLeft = pyautogui.locateOnScreen(image= TopLeft(), confidence= 0.99)
bottomRight = pyautogui.locateOnScreen(image= BottomRight(), confidence= 0.99)

screen = Box(int(topLeft.left), 
          int(topLeft.top), 
          int(bottomRight.left + bottomRight.width - topLeft.left), 
          int(bottomRight.top + bottomRight.height - topLeft.top))
try:
    os.mkdir(path= TempDir())
except:
    pass

print(f"screen: {screen}")
screenshot(region= screen, file= TempDir("S1.bmp"))

btnPlay_click(screen)
# mouseMove_default(screen)
s2 = screenshot(region= screen, file= TempDir("S2.bmp"))

A1 = Box(67, 72, 93, 97) 
A2 = Box(100, 72, 126, 97)
A18 = Box(67, 105, 93, 130)
A170 = Box(595, 369, 621, 394)

# print(f"A1: {A1.left - A2.left}")
# print(f"A1: {A1.top - A18.top}")
print(f"A1-w: {A1.left - A1.width}")
print(f"A1-h: {A1.top - A1.height}")
print(f"A2-w: {A2.left - A2.width}")
print(f"A2-h: {A2.top - A2.height}")


print(f"A1-A2-w: {A1.width - A2.left}")
print(f"A1-A18-h: {A1.height - A18.top}")

def captureApple(image: Image.Image, x: int, y: int, firstApple: Box, dump=False) -> list[list[tuple[Image.Image, Box]]]:
    dx = 7
    dy = 8

    matrix = []

    for j in range(0, y):
        row = []
        for i in range(0, x):
            # region = firstApple

            # region.left = firstApple.left + (firstApple.width * x) + (dx * x)
            # region.top = firstApple.top + (firstApple.top * x) + (dy * x)

            region = Box(
                (firstApple.left + (firstApple.width * i) + (dx * i)), 
                (firstApple.top + (firstApple.height * j) + (dy * j)),
                firstApple.width, 
                firstApple.height)
            
            filename = f"A_{str(i)}x{str(j)}.bmp"

            
            print(f"{filename}: {region}")

            im = crop(image= image,region= region)

            if dump:
                im.save(TempDir(filename))

            row.append((im, region))
        
        matrix.append(row)
    
    return matrix

def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err

Apple = collections.namedtuple('Apple', 'num, region alive')

def identify(apples: list[list[tuple[Image.Image, Box]]]) -> list[list[Apple]]:

    index = []

    for i in range(1, 9):
        a = cv2.cvtColor(np.array(Image.open(ImagesDir(f"a{str(i)}.bmp"))), cv2.COLOR_RGB2BGR)
        index.append(a)

    matrix = []

    for y in apples:

        row = []
        for x in y:
            
            imageA = x[0]
            region = x[1]

            imageA = cv2.cvtColor(np.array(imageA), cv2.COLOR_RGB2BGR)

            i = 0
            apple = 0
            score = 10000

            for imageB in index:
                m = mse(imageA, imageB)
  
                if m < score:
                    score = m
                    apple = i+1
                
                i = i + 1

            row.append(Apple(apple, region, True))
        
        matrix.append(row)
        
    return matrix

        

apples = captureApple(image= s2, x= 17, y= 10, firstApple= Box(67, 72, 26, 25), dump= True)
print(len(apples))

apples = identify(apples)
print(apples)

for turn in range(0, 5):
    for x in range(1, len(apples)):
        for y in range(1, len(apples[x])):
            print(apples[x][y])

            
        
    # pyautogui.drag()