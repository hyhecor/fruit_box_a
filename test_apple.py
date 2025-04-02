import os
from PIL import Image
import numpy as np
from skimage.metrics import structural_similarity as ssim
import cv2
import matplotlib.pyplot as plt 
import glob

from game import mse


def check(a: str, b: list[str], pltfunc):

    print(a)
    print(b)

    for x in a:

        imageA = Image.open(x)
        imageA = cv2.cvtColor(np.array(imageA), cv2.COLOR_RGB2RGBA)

        max_ = 0
        b_ = ""
        bi = None

        j = 0
        for y in b:

            # imageA = Image.open(x)
            imageB = Image.open(y)

            # imageA = cv2.cvtColor(np.array(imageA), cv2.COLOR_RGB2BGR)
            imageB = cv2.cvtColor(np.array(imageB), cv2.COLOR_RGB2RGBA)

            m = mse(imageA, imageB)
            # s = ssim(im, imageB)
            s = 0
            # print(f"MSE: %.2f, SSIM: %.2f" % (m, s))

            max_ = max(max_, m)
            if m == max_:
                b_ = y
                bi = imageB

            j = j + 1

        pltfunc((x, imageA), (y, imageB, m))

        print(f"mse: {int(max_)}")


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

    fig, axs = plt.subplots(9, 2, figsize=(12, 12))

    def PltFunc(row: int):
        def fn(a, b):
            axa = axs[row-1, 0]
            axb = axs[row-1, 1]

            axa.plot([1, 2, 3])
            axa.set_title(f"A file={a[0]}")
            axa.imshow(a[1])

            mse = int(b[2])

            axb.plot([4, 5, 6])
            axb.set_title(
                f"B file={b[0]} mse={mse} star={star(5 if 500 < mse else mse / 100)}")
            axb.imshow(b[1])

        return fn


    check(glob.glob(os.path.join("images", "a1.bmp")), glob.glob(os.path.join("images", "a1", "*")), PltFunc(1))
    check(glob.glob(os.path.join("images", "a2.bmp")), glob.glob(os.path.join("images", "a2", "*")), PltFunc(2))
    check(glob.glob(os.path.join("images", "a3.bmp")), glob.glob(os.path.join("images", "a3", "*")), PltFunc(3))
    check(glob.glob(os.path.join("images", "a4.bmp")), glob.glob(os.path.join("images", "a4", "*")), PltFunc(4))
    check(glob.glob(os.path.join("images", "a5.bmp")), glob.glob(os.path.join("images", "a5", "*")), PltFunc(5))
    check(glob.glob(os.path.join("images", "a6.bmp")), glob.glob(os.path.join("images", "a6", "*")), PltFunc(6))
    check(glob.glob(os.path.join("images", "a7.bmp")), glob.glob(os.path.join("images", "a7", "*")), PltFunc(7))
    check(glob.glob(os.path.join("images", "a8.bmp")), glob.glob(os.path.join("images", "a8", "*")), PltFunc(8))
    check(glob.glob(os.path.join("images", "a9.bmp")), glob.glob(os.path.join("images", "a9", "*")), PltFunc(9))
    
    plt.show(block=True)
