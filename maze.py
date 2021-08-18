import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from generate_maze import Maze


class App(tk.Tk):
    def __init__(self, *args, width=200, height=100, zoom=1, **kwargs) -> None:
        super(App, self).__init__(*args, **kwargs)

        self.title("Maze")
        self.resizable(False, False)
        self.geometry(f"{width * zoom + 100}x{height * zoom + 150}")

        self.__width = width
        self.__height = height
        self.__zoom = zoom

        self.__start = None
        self.__finish = None
        self.__maze = None

        self.__gui()
        self.mainloop()

    def make_step(self, m, k):
        for i in range(len(m)):
            for j in range(len(m[0])):
                if m[i][j] == k:
                    if i > 0 and m[i - 1][j] == 0 and self.__maze[i - 1][j] == 0:
                        m[i - 1][j] = k + 1
                    if j > 0 and m[i][j - 1] == 0 and self.__maze[i][j - 1] == 0:
                        m[i][j - 1] = k + 1
                    if j < len(m[0]) - 1 and m[i][j + 1] == 0 and self.__maze[i][j + 1] == 0:
                        m[i][j + 1] = k + 1
                    if i < len(m) - 1 and m[i + 1][j] == 0 and self.__maze[i + 1][j] == 0:
                        m[i + 1][j] = k + 1
        return m

    def update_image(self, m, elem=None):
        img = Image.new("RGB", (len(self.__maze) * self.__zoom, len(self.__maze[0]) * self.__zoom))
        draw = ImageDraw.Draw(img)
        width, height = img.size
        for x in range(0, width, self.__zoom):
            for y in range(0, height, self.__zoom):
                if (y // self.__zoom, x // self.__zoom) == self.__start:
                    r, g, b = (0, 255, 0)
                elif (y // self.__zoom, x // self.__zoom) == self.__finish:
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
        self.update()

    def scan(self):
        m = [[0 for _ in range(len(self.__maze[0]))] for _ in range(len(self.__maze))]
        m[self.__start[1]][self.__start[0]] = 1
        k = 0
        while not m[self.__finish[1]][self.__finish[0]]:
            k += 1
            m = self.make_step(m, k)
            self.update_image(m)
        return m

    def find_path(self):
        (y, x) = self.__finish
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
        self.__btn_generate["state"] = tk.DISABLED
        self.__btn_start["state"] = tk.DISABLED
        path, m = self.find_path()
        for elem in path:
            self.update_image(m, elem)
        self.__btn_generate["state"] = tk.NORMAL
        self.__btn_start["state"] = tk.NORMAL

    def btn_generate_event(self):
        m_rand = Maze(width=self.__width, height=self.__height)
        self.__start = (m_rand.start_x, m_rand.start_y)
        self.__finish = m_rand.finish

        self.__maze = m_rand.create_maze()
        self.update_image(self.__maze)

        if self.__btn_start["state"] == tk.DISABLED:
            self.__btn_start["state"] = tk.NORMAL

    def __gui(self):
        self.__btn_start = tk.Button(self, text="Find path", state=tk.DISABLED, command=lambda: self.btn_start_event())
        self.__btn_generate = tk.Button(self, text="Generate maze", command=lambda: self.btn_generate_event())
        btn_exit = tk.Button(self, text="Exit", command=self.quit)
        self.__label = tk.Label(self)

        self.__btn_start.pack(pady=5)
        self.__btn_generate.pack(pady=5)
        self.__label.pack(fill=tk.BOTH, expand=True, pady=5)
        btn_exit.pack(pady=5)


if __name__ == "__main__":
    App(className="Maze", width=90, height=120, zoom=5)

