import os
from PIL import Image
import numpy as np
import cv2
import matplotlib.pyplot as plt
import glob

from game import mse, captureApple
from game import Point, Box


def crop(screens: list[str], a: list[str], destDir: str):
    grid = Point(17, 10)
    appleZero = Box(67, 72, 26, 25)

    apples: list[Image.Image] = []

    for a in a:

        appleImg = Image.open(a)
        apples.append(cv2.cvtColor(np.array(appleImg), cv2.COLOR_RGB2RGBA))

    for screen in screens:

        screenImg = Image.open(screen)

        crops = captureApple(grid, appleZero, screenImg)

        # screenImg = cv2.cvtColor(np.array(screenImg), cv2.COLOR_RGB2RGBA)

        i = 0
        for crop in crops:
            c = cv2.cvtColor(
                np.array(crop), cv2.COLOR_RGB2RGBA)

            for apple in apples:
                # crop = cv2.cvtColor(np.array(crop), cv2.COLOR_RGB2RGBA)
                m = mse(apple, c)

                if m < 200:
                    if False:
                        plt.figure(figsize=(10, 5))
                        plt.subplot(1, 2, 1)
                        plt.title(a)
                        plt.imshow(apple)

                        plt.subplot(1, 2, 2)
                        plt.title(f"{i}_{int(m)}")
                        plt.imshow(crop)

                        plt.show(block=True)

                    dest = os.path.join(destDir, f"{i}.bmp")

                    if os.path.isdir(os.path.dirname(dest)) == False:
                        os.makedirs(os.path.dirname(dest))

                    crop.save(dest)

                    break
 
            i = i+1



if __name__ == "__main__":
    print("사과 아이콘을 테스트 한다")

    def star(r) -> str:
        match int(r):
            case 0:
                return "☆☆☆☆☆"
            case 1:
                return "★☆☆☆☆"
            case 2:
                return "★★☆☆☆"
            case 3:
                return "★★★☆☆"
            case 4:
                return "★★★★☆"
            case 5:
                return "★★★★★"

        return "☆☆☆☆☆"

    def imageFiles(s: str):
        return glob.glob(os.path.join("images", s, "*"))

    def tmpDir(s: str):
        return os.path.join("tmp", s)

    screenPaths = glob.glob(os.path.join("images", "screens", "*"))

    crop(screenPaths, imageFiles("a1"), tmpDir("a1"))
    crop(screenPaths, imageFiles("a2"), tmpDir("a2"))
    crop(screenPaths, imageFiles("a3"), tmpDir("a3"))
    crop(screenPaths, imageFiles("a4"), tmpDir("a4"))
    crop(screenPaths, imageFiles("a5"), tmpDir("a5"))
    crop(screenPaths, imageFiles("a6"), tmpDir("a6"))
    crop(screenPaths, imageFiles("a7"), tmpDir("a7"))
    crop(screenPaths, imageFiles("a8"), tmpDir("a8"))
    crop(screenPaths, imageFiles("a9"), tmpDir("a9"))
