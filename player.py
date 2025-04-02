from game import getScreen
from game import Box, Point, Apple, Game 


def player(grid: Point, apples: list[Apple]) -> list[list[Apple]]:

    i = 0
    for apple in apples:
        if 500 < apple.score:
            print("score too high", i, apple)

        i = i + 1

    alives: list[bool] = []
    for a in apples:
        alives.append(True)

    rst: list[list[Apple]] = []

    def seek_g():
        i = 0
        while i < len(apples):

            left = (i % (grid.x))
            right = (grid.x - i % grid.x) - 1
            up = int(i / (grid.x))
            down = (grid.y - int(i / (grid.x))) - 1

            print(left, right, up, down)

            def rl(i):
                cursor = apples[i]
                # a = pos[i]
                alive = alives[i]

                index = []
                index.append(i)
                if alive == True:

                    sum = cursor.num
                    for l in range(0, left):
                        l = l + 1

                        tango = apples[i-l]
                        # b = pos[i-l]
                        alive = alives[i-l]

                        if alive == True:
                            sum = sum + tango.num

                            index.append(i-l)

                            if sum == 10:
                                # mouseDrag(screen, b, a, duration=duration)

                                rst.append((cursor, tango))

                                for i in index:
                                    apples[i] = Apple(
                                        apples[i].index, apples[i].num, apples[i].score)
                                    alives[i] = False

                                return i-1
                            elif 10 < sum:
                                break

                return i+1

            i = rl(i)

    for _ in range(grid.x):
        for _ in range(grid.y):

            seek_g()

    return rst


def player2(grid: Point, apples: list[Apple]) -> list[list[Apple]]:

    i = 0
    for apple in apples:
        if 500 < apple.score:
            print("score too high", i, apple)

        i = i + 1

    alives: list[bool] = []
    for a in apples:
        alives.append(True)

    rst: list[list[Apple]] = []

    def horizontal(c: int):
        d = 1

        for i in range(len(apples)-1):

            left = (i % (grid.x))
            right = (grid.x - i % grid.x) - c
            up = int(i / (grid.x))
            down = (grid.y - int(i / (grid.x))) - c

            if right <= 0:
                continue

            aa = []
            al = []
            sum = 0
            for x in range(i, i+(c*d)+1, d):
                if alives[x]:
                    aa.append(apples[x])
                    al.append(x)
                    sum = sum + apples[x].num

            if sum == 10:
                rst.append(aa)

                for x in al:
                    alives[x] = False

    def vertical(c: int):
        d = grid.x

        for i in range(len(apples)-1):

            left = (i % (grid.x))
            right = (grid.x - i % grid.x) - c
            up = int(i / (grid.x))
            down = (grid.y - int(i / (grid.x))) - c

            if down <= 0:
                continue

            aa = []
            al = []
            sum = 0
            for x in range(i, i+(c*d)+1, d):
                if alives[x]:
                    aa.append(apples[x])
                    al.append(x)
                    sum = sum + apples[x].num

            if sum == 10:
                rst.append(aa)

                for x in al:
                    alives[x] = False

    def rectangle(c: int):
        for i in range(len(apples)-1):

            left = (i % (grid.x))
            right = (grid.x - i % grid.x) - c
            up = int(i / (grid.x))
            down = (grid.y - int(i / (grid.x))) - c

            if right <= 0:
                continue

            if down <= 0:
                continue

            aa = []
            al = []
            sum = 0

            # d = 1
            # for x in range(i, i+(c*d)+1, d):
            #     if alives[x]:
            #         aa.append(apples[x])
            #         al.append(x)
            #         sum = sum + apples[x].num

            for x in range(i, i+(c*grid.x)+1, grid.x):
                # if alives[x]:
                #     aa.append(apples[x])
                #     al.append(x)
                #     sum = sum + apples[x].num

                for x in range(x, x+(c*1)+1, 1):
                    if alives[x]:
                        aa.append(apples[x])
                        al.append(x)
                        sum = sum + apples[x].num

            if sum == 10:
                rst.append(aa)

                for x in al:
                    alives[x] = False

    def macro(n: int):
        # 대각
        for i in range(n, n+1):
            rectangle(i)
        # 가로
        horizontal(n)
        # 세로
        vertical(n) 

    macro(1)
    macro(2)
    macro(3)
    macro(4)
    macro(5)
    macro(6)
    macro(7)
    macro(8)
    macro(9)
    macro(10)

    return rst


if __name__ == "__main__":

    grid = Point(17, 10)
    appleZero = Box(67, 72, 26, 25)
    screen = Box(0, 0, 0, 0)

    screen = getScreen("images/screen.bmp", show=False)
    print(
        f"screen = Box({screen.left}, {screen.top}, {screen.width}, {screen.height})")

    # indexImages = getIndexImages()

    game = Game(grid=grid, screen=screen,
                appleZero=appleZero)

    game.btn_play_click()

    game.Play(player2, show=False)
