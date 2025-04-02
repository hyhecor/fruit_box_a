import os
from PIL import Image
import numpy as np
import cv2
import matplotlib.pyplot as plt
from datetime import datetime
from collections.abc import Callable, Awaitable
import glob


from game import mse, captureApple, guess
from game import Point, Box


def check(screens: list[str], guess: Callable[[Image.Image], int]):
    grid = Point(17, 10)
    appleZero = Box(67, 72, 26, 25)

    for screen in screens:

        screenImg = Image.open(screen)

        crops = captureApple(grid, appleZero, screenImg)

        j = 0
        for crop in crops:

            num = guess(crop)

            if num == 0:

                crop.save(os.path.join(
                    "tmp", f"{os.path.basename(screen)}_{j}_undefined-{datetime.now(datetime.UTC)}.bmp"))

                c = cv2.cvtColor(
                    np.array(crop), cv2.COLOR_RGB2RGBA)

                plt.figure(figsize=(10, 5))

                plt.title(f"{os.path.basename(screen)}_{j}")
                plt.imshow(c)

                plt.show(block=True)

            j = j+1

        print(f"{screen} done")


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

    screenPaths = glob.glob(os.path.join("images", "screens", "*"))

    guess = guess()

    check(screenPaths, guess)
