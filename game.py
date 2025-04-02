import matplotlib.pyplot as plt
import collections
import pyautogui
import os
from PIL import Image
import numpy as np
from skimage.metrics import structural_similarity as ssim
import cv2
from datetime import datetime
import sys
from collections.abc import Callable, Awaitable
import glob

Box = collections.namedtuple('Box', 'left top width height')
Point = collections.namedtuple('Point', 'x y')
Apple = collections.namedtuple('Apple', 'index num, score')


def Region(box: Box) -> tuple[int, int, int, int]:
    return (
        int(box.left),
        int(box.top),
        int(box.width),
        int(box.height))


def unixTime():
    unix_timestamp = (datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()
    return unix_timestamp


def btnPlay_click(screen: Box, offset=Point(200, 250)):
    dp = pyautogui.position()

    p = Point(screen.left + offset.x, screen.top + offset.y)
    pyautogui.click(x=p.x, y=p.y)

    pyautogui.moveTo(x=dp.x, y=dp.y)


def mouseMove_default(screen: Box):
    pyautogui.moveTo(x=screen.left, y=screen.top)


def screenshot(box: Box, file: str, dump=False):

    im = pyautogui.screenshot(region=Region(box))

    if dump:
        im.save(file)

    return im


def crop(image: Image.Image, region: Box) -> Image.Image:
    region_ = (int(region.left),
               int(region.top),
               int(region.left + region.width),
               int(region.top + region.height))
    im = image.crop(box=region_)

    return im


def captureApple(grid: Point, appleZero: Box, image: Image.Image) -> list[Image.Image]:
    dx = 7
    dy = 8

    matrix: list[Image.Image] = []

    for j in range(0, grid.y):
        for i in range(0, grid.x):
            box = Box(
                (appleZero.left + (appleZero.width * i) + (dx * i)),
                (appleZero.top + (appleZero.height * j) + (dy * j)),
                appleZero.width,
                appleZero.height)

            im = crop(image=image, region=box)

            matrix.append(im)

    return matrix


def applePositions(grid: Box, appleZero=Box(67, 72, 26, 25)) -> list[Box]:
    dx = 7
    dy = 8

    matrix: list[Box] = []

    for j in range(0, grid.y):
        for i in range(0, grid.x):
            box = Box(
                (appleZero.left + (appleZero.width * i) + (dx * i)),
                (appleZero.top + (appleZero.height * j) + (dy * j)),
                appleZero.width,
                appleZero.height)

            matrix.append(box)

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


def identify(index: list[Image.Image], apples: list[Image.Image]) -> list[Apple]:

    matrix: list[Apple] = []

    for i in range(len(apples)):

        imageA = apples[i]

        imageA = cv2.cvtColor(np.array(imageA), cv2.COLOR_RGB2RGBA)

        apple = 0
        score = sys.maxsize

        for imageB in index:
            m = mse(imageA, imageB[1])

            if m < score:
                score = int(m)
                apple = imageB[0]

        matrix.append(Apple(i, apple, score))

    return matrix


def identify2(apples: list[Image.Image], guess: Callable[[Image.Image], (int, int)]) -> list[Apple]:

    matrix: list[Apple] = []

    for i in range(len(apples)):

        imageA = apples[i]

        apple = guess(imageA)

        matrix.append(Apple(i, apple[0], apple[1]))

    return matrix


def mouseDrag(screen: Box, a: Point, b: Point, duration=0.22, margin=5):
    a_ = Point(
        screen.left + a.x,
        screen.top + a.y)
    b_ = Point(
        screen.left + b.x,
        screen.top + b.y)

    # diff = max(abs(a_.x - b_.x), abs(a_.y - b_.y))

    # diff = diff / a.x

    # d = diff * duration

    print(f"mouse drag a:{a_} b:{b_}, duration:{duration}")

    pyautogui.moveTo(a_.x-margin, a_.y-margin)
    pyautogui.dragTo(b_.x+margin+margin, b_.y+margin, duration, button='left')


def getScreen(screenFile: str, show=False) -> Box:

    screenBox = pyautogui.locateOnScreen(image=screenFile, confidence=0.99)

    if show:
        screen = pyautogui.screenshot()

        mat = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2RGBA)

        red = (255, 0, 0)

        mat = cv2.rectangle(
            mat,
            (screenBox.left, screenBox.top),
            (screenBox.left + screenBox.width, screenBox.top + screenBox.height),
            color=red,
            thickness=1)

        plt.figure(figsize=(17, 10))

        plt.imshow(mat)

        plt.show(block=True)

    return Box(screenBox.left,    screenBox.top,
               screenBox.width, screenBox.height)


def guess() -> Callable[[Image.Image], tuple[int, int]]:

    def load(s: list[str]) -> list[cv2.typing.MatLike]:
        mats: list[cv2.typing.MatLike] = []

        for s in s:
            img = Image.open(s)
            mats.append(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2RGBA))

        return mats

    a1 = load(glob.glob(os.path.join("images", "a1", "*")))
    a2 = load(glob.glob(os.path.join("images", "a2", "*")))
    a3 = load(glob.glob(os.path.join("images", "a3", "*")))
    a4 = load(glob.glob(os.path.join("images", "a4", "*")))
    a5 = load(glob.glob(os.path.join("images", "a5", "*")))
    a6 = load(glob.glob(os.path.join("images", "a6", "*")))
    a7 = load(glob.glob(os.path.join("images", "a7", "*")))
    a8 = load(glob.glob(os.path.join("images", "a8", "*")))
    a9 = load(glob.glob(os.path.join("images", "a9", "*")))

    def fn(img: Image.Image) -> int:
        mat = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2RGBA)

        def comp(n: int) -> bool:

            # plt.figure(figsize=(5, 6))

            # plt.imshow(mat)

            # plt.show(block=True)

            return n < 500

        for a in a1:
            if comp(mse(a, mat)):
                return (1, mse(a, mat))
        for a in a2:
            if comp(mse(a, mat)):
                return (2, mse(a, mat))
        for a in a3:
            if comp(mse(a, mat)):
                return (3, mse(a, mat))
        for a in a4:
            if comp(mse(a, mat)):
                return (4, mse(a, mat))
        for a in a5:
            if comp(mse(a, mat)):
                return (5, mse(a, mat))
        for a in a6:
            if comp(mse(a, mat)):
                return (6, mse(a, mat))
        for a in a7:
            if comp(mse(a, mat)):
                return (7, mse(a, mat))
        for a in a8:
            if comp(mse(a, mat)):
                return (8, mse(a, mat))
        for a in a9:
            if comp(mse(a, mat)):
                return (9, mse(a, mat))

        return 0

    return fn


class Game:
    def __init__(self, grid: Point, screen: Box, appleZero: Box):
        self.grid = grid
        self.screen = screen
        self.appleZero = appleZero
        # self.indexImages = indexImages
        self.guess = guess()

    def btn_play_click(self):
        btnPlay_click(self.screen)

    def Play(self, player: Callable[[Point, list[Apple]], list[list[Apple]]], show=False):

        self.screenImg = pyautogui.screenshot(region=Region(self.screen))

        if show:
            plt.imshow(cv2.cvtColor(
                np.array(self.screenImg), cv2.COLOR_RGB2RGBA))
            plt.show(block=True)

        self.applepositions = applePositions(
            grid=self.grid,   appleZero=self.appleZero)

        if show:
            mat = cv2.cvtColor(np.array(self.screenImg), cv2.COLOR_RGB2RGBA)

            for box in self.applepositions:
                red = (255, 0, 0)

                mat = cv2.rectangle(
                    mat,
                    (box.left, box.top),
                    (box.left+box.width, box.top+box.height),
                    color=red,
                    thickness=1)

                print(
                    f"apple = Box({box.left}, {box.top}, {box.width}, {box.height})")

            plt.figure(figsize=(17, 10))
            plt.imshow(mat)
            plt.show(block=True)

        self.appleimgs = captureApple(
            self.grid, self.appleZero, self.screenImg)

        if show:
            plt.figure(figsize=(17, 10))

            i = 0
            for img in self.appleimgs:
                mat = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2RGBA)

                plt.subplot(10, 17, i+1)

                plt.imshow(mat)

                i = i + 1

            plt.show(block=True)

        # self.apples = identify(self.indexImages, self.appleimgs)
        self.apples = identify2(self.appleimgs, self.guess)

        # player(self.grid, self.screen, self.appleZero)

        solutions = player(self.grid, self.apples)

        def squr(x):
            return x*x

        def getLT(group: list[Apple]):
            w, h = 0, 0
            if 0 < len(group):
                w = self.applepositions[group[0].index].left
                h = self.applepositions[group[0].index].top
            for item in group:
                w = min(w, self.applepositions[item.index].left)
                h = min(h, self.applepositions[item.index].top)

            return Point(w, h)

        def getRB(group: list[Apple]):
            w, h = 0, 0
            if 0 < len(group):
                p = self.applepositions[group[0].index]

                w = p.left + p.width
                h = p.top + p.height

            for item in group:
                p = self.applepositions[item.index]

                w = max(w, p.left+p.width)
                h = max(h, p.top + p.height)

            return Point(w, h)

        import math
        for solution in solutions:

            print(f"solution: {solution}")

            lt = getLT(solution)
            rb = getRB(solution)

            box = (lt.x, lt.y, rb.x, rb.y)

            a = box[2] - box[0]
            b = box[3] - box[1]
            c = math.sqrt(squr(a) + squr(b))

            print(f"distance a:{a} b:{b} c:{c}")

            mouseDrag(self.screen, lt,
                      rb, duration=(c/80.0)+0.1)


if __name__ == "__main__":
    print("fruit_box_a solver")
    print("v0.0.1")
    print("https://www.gamesaien.com/game/fruit_box_a/")
    print("python player.py")
