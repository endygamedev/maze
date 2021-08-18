import tkinter as tk
import time
from PIL import Image, ImageTk, ImageDraw
from generate_maze import Maze


class App(tk.Tk):
    def __init__(self, *args, maze=None, start=None, finish=None, zoom=1, **kwargs) -> None:
        super(App, self).__init__(*args, **kwargs)

        self.title("Maze")

        self.__maze = maze
        self.__start = start
        self.__finish = finish
        self.__zoom = zoom

        self.__gui()

        self.mainloop()

    # Iterative step
    def make_step(self, m, k):
        for i in range(len(m)):
            for j in range(len(m[0])):
                # Edit last cells
                if m[i][j] == k:
                    # Left
                    if i > 0 and m[i - 1][j] == 0 and self.__maze[i - 1][j] == 0:
                        m[i - 1][j] = k + 1
                    # Down
                    if j > 0 and m[i][j - 1] == 0 and self.__maze[i][j - 1] == 0:
                        m[i][j - 1] = k + 1
                    # Right
                    if j < len(m[0]) - 1 and m[i][j + 1] == 0 and self.__maze[i][j + 1] == 0:
                        m[i][j + 1] = k + 1
                    # Up
                    if i < len(m) - 1 and m[i + 1][j] == 0 and self.__maze[i + 1][j] == 0:
                        m[i + 1][j] = k + 1
        return m

    def update_image(self, m, elem=None):
        img = Image.new("RGB", (len(self.__maze) * self.__zoom, len(self.__maze[0]) * self.__zoom))
        draw = ImageDraw.Draw(img)
        width, height = img.size
        for x in range(0, width, self.__zoom):
            for y in range(0, height, self.__zoom):
                if (x // self.__zoom, y // self.__zoom) == self.__start:
                    r, g, b = (0, 255, 0)
                elif (x // self.__zoom, y // self.__zoom) == self.__finish:
                    r, g, b = (255, 0, 255)
                elif (x // self.__zoom, y // self.__zoom) == elem or m[x // self.__zoom][y // self.__zoom] == "path":
                    r, g, b = (0, 255, 255)
                    m[x // self.__zoom][y // self.__zoom] = "path"
                elif m[x // self.__zoom][y // self.__zoom] > 1:
                    r, g, b = (255, 0, 0)
                elif self.__maze[x // self.__zoom][y // self.__zoom] == 0:
                    r, g, b = (255, 255, 255)
                else:
                    r, g, b = (0, 0, 0)

                for x1 in range(x, x + self.__zoom):
                    for y1 in range(y, y + self.__zoom):
                        draw.point((x1, y1), (r, g, b))
        img_tk = ImageTk.PhotoImage(img.transpose(Image.ROTATE_90).transpose(Image.FLIP_TOP_BOTTOM))
        self.__label.config(image=img_tk)
        self.__label.image = img_tk
        time.sleep(0.01)
        self.update()

    def scan(self):
        m = [[0 for _ in range(len(self.__maze[0]))] for _ in range(len(self.__maze))]
        m[self.__start[0]][self.__start[1]] = 1
        k = 0
        while not m[self.__finish[0]][self.__finish[1]]:
            k += 1
            m = self.make_step(m, k)
            self.update_image(m)
        return m

    def find_path(self):
        (x, y) = self.__finish
        m = self.scan()
        k = m[x][y]
        path = [(x, y)]
        while k > 1:
            if x > 0 and m[x - 1][y] == k - 1:
                (x, y) = x - 1, y
            elif y > 0 and m[x][y - 1] == k - 1:
                (x, y) = x, y - 1
            elif x < len(m) - 1 and m[x + 1][y] == k - 1:
                (x, y) = x + 1, y
            else:
                (x, y) = x, y + 1
            path.append((x, y))
            k -= 1
        return path, m

    def btn_start_event(self):
        path, m = self.find_path()
        for elem in path:
            self.update_image(m, elem)

    def btn_generate_event(self):
        mRand = Maze(width=50, height=50)
        self.__start = (mRand.start_x, mRand.start_y)
        self.__finish = mRand.finish

        self.__maze = mRand.create_maze()
        self.update_image(self.__maze)

    def __gui(self):
        btn_start = tk.Button(self, text="start", command=lambda: self.btn_start_event())
        btn_generate = tk.Button(self, text="generate", command=lambda: self.btn_generate_event())
        self.__label = tk.Label(self)

        btn_start.pack(pady=10)
        btn_generate.pack(pady=10)
        self.__label.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    m1 = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]

    s1 = (1, 1)
    f1 = (2, 5)

    m2 = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0 ,0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0 ,0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0 ,0, 0, 0, 1, 0, 1, 1, 1, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0 ,0, 0, 0, 1, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0 ,0, 0, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0 ,0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0 ,0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]

    s2 = (1, 1)
    f2 = (5, 19)

    App(className="Maze", zoom=10)

