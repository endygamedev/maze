# Copyright (c) 2021 Egor Bronnikov
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from maze import Maze
from pprint import pprint


class App(tk.Tk):
    def __init__(self, *args, width, height, zoom, **kwargs):
        """ Class that creates the `root` window

        :param args: all `args` options that has `tkinter.Tk`
        :param width: width of the resulting maze
        :type width: int
        :param height: height of the resulting maze
        :type height: int
        :param zoom: maze scale
        :type zoom: int
        :param kwargs: all `kwargs` options that has `tkinter.Tk`

        :return: `side effect`: creates a window
        :rtype: None
        """
        super().__init__(*args, **kwargs)

        self.title("Maze")
        self.resizable(False, False)
        self.geometry(f"{width * zoom + 100}x{height * zoom + 150}")

        self.__width = width
        self.__height = height
        self.__zoom = zoom

        self.gui()
        self.btn_generate_event()
        self.mainloop()

    def step(self, matrix, k):
        """ Makes one iteration (step) required to find the finish

        :param matrix: matrix of values in cells from the previous step
        :type matrix: List[List[int]]
        :param k: iteration number
        :type k: int

        :return: matrix in which the values were changed in such a way that from the last iteration we took a step to the sides
        :rtype: List[List[int]]
        """
        for i in range(self.__height):
            for j in range(self.__width):
                if matrix[i][j] == k:
                    # up
                    if i > 0 and matrix[i - 1][j] == 0 and self.__maze[i - 1][j] == 0:
                        matrix[i - 1][j] = k + 1
                    # left
                    if j > 0 and matrix[i][j - 1] == 0 and self.__maze[i][j - 1] == 0:
                        matrix[i][j - 1] = k + 1
                    # right
                    if j < self.__width - 1 and matrix[i][j + 1] == 0 and self.__maze[i][j + 1] == 0:
                        matrix[i][j + 1] = k + 1
                    # down
                    if i < self.__height - 1 and matrix[i + 1][j] == 0 and self.__maze[i + 1][j] == 0:
                        matrix[i + 1][j] = k + 1
        return matrix

    def update_image(self, matrix, elem=None):
        """ Updates the image (maze) depending on the matrix of values

        :param matrix: matrix of values in maze cells
        :type matrix: List[List[int]]
        :param elem: element from the `path` from the finish to the start, it is needed so that we can paint a new cell of the `path`
        :type elem: Union[None, Tuple[int, int]]

        :return: `side effect`: draws a new image and loads it into `label`
        :rtype: None
        """
        img = Image.new("RGB", (self.__height * self.__zoom, self.__width * self.__zoom))
        draw = ImageDraw.Draw(img)
        width, height = img.size

        for x in range(0, width, self.__zoom):
            for y in range(0, height, self.__zoom):
                val_x, val_y = x // self.__zoom, y // self.__zoom
                if (val_y, val_x) == self.__start:
                    r, g, b = (0, 255, 0)
                elif (val_y, val_x) == self.__finish:
                    r, g, b = (255, 0, 255)
                elif (val_x, val_y) == elem or matrix[val_x][val_y] == "path":
                    r, g, b = (0, 255, 255)
                    matrix[val_x][val_y] = "path"
                elif matrix[val_x][val_y] > 1:
                    r, g, b = (255, 0, 0)
                elif self.__maze[val_x][val_y] == 0:
                    r, g, b = (255, 255, 255)
                else:
                    r, g, b = (0, 0, 0)

                for x1 in range(x, x + self.__zoom):
                    for y1 in range(y, y + self.__zoom):
                        draw.point((x1, y1), (r, g, b))

        img_tk = ImageTk.PhotoImage(img.transpose(Image.ROTATE_90).transpose(Image.FLIP_TOP_BOTTOM))
        self.__label.config(image=img_tk)
        self.__label.image = img_tk
        self.update()

    def scan(self):
        """ Makes one step of iteration until it reaches the finish

        :return: matrix of values with cells from start to finish
        :rtype: List[List[int]]
        """
        matrix = [[0 for _ in range(len(self.__maze[0]))] for _ in range(len(self.__maze))]
        matrix[self.__start[1]][self.__start[0]] = 1
        k = 0
        while not matrix[self.__finish[1]][self.__finish[0]]:
            k += 1
            matrix = self.step(matrix, k)
            self.update_image(matrix)
        return matrix

    def find_path(self):
        """ Finds the shortest path from start to finish using the matrix of values

        :return: list with coordinates of cells of the shortest path and a modified matrix of values (maze)
        :rtype: Tuple[List[Tuple[int, int]], List[List[int]]]
        """
        (y, x) = self.__finish
        matrix = self.scan()
        k = matrix[x][y]
        path = [(x, y)]
        while k > 1:
            if x > 0 and matrix[x - 1][y] == k - 1:
                (x, y) = x - 1, y
            elif y > 0 and matrix[x][y - 1] == k - 1:
                (x, y) = x, y - 1
            elif x < self.__height - 1 and matrix[x + 1][y] == k - 1:
                (x, y) = x + 1, y
            else:
                (x, y) = x, y + 1
            path.append((x, y))
            k -= 1
        pprint(matrix)
        return path, matrix

    def btn_start_event(self):
        """ Button event for `btn_start`

        :return: `side effect`: button event
        :rtype: None
        """
        self.__btn_generate["state"] = tk.DISABLED
        self.__btn_start["state"] = tk.DISABLED
        path, m = self.find_path()
        for elem in path:
            self.update_image(m, elem)
        self.__btn_generate["state"] = tk.NORMAL
        self.__btn_start["state"] = tk.NORMAL

    def btn_generate_event(self):
        """ Button event for `btn_generate`

        :return: `side effect`: button event
        :rtype: None
        """
        m_rand = Maze(width=self.__width, height=self.__height)
        self.__start = (m_rand.start_x, m_rand.start_y)
        self.__finish = m_rand.finish

        self.__maze = m_rand.create_maze()
        self.update_image(self.__maze)

    def gui(self):
        """ Renders graphics primitives

        :return: `side effect`: renders GUI
        :rtype: None
        """
        self.__btn_start = tk.Button(self, text="Find path", command=lambda: self.btn_start_event())
        self.__btn_generate = tk.Button(self, text="Generate maze", command=lambda: self.btn_generate_event())
        btn_exit = tk.Button(self, text="Exit", command=self.quit)
        self.__label = tk.Label(self)

        self.__btn_start.pack(pady=5)
        self.__btn_generate.pack(pady=5)
        self.__label.pack(fill=tk.BOTH, expand=True, pady=5)
        btn_exit.pack(pady=5)


if __name__ == "__main__":
    App(className="Maze", width=10, height=10, zoom=20)
