import random


class Maze:
    def __init__(self, *, width, height):
        """ Class that randomly generates a maze (matrix of values)

        :param width: desired maze width
        :type width: int
        :param height: desired maze height
        :type height: int

        :return: `side effect`: initializes class values
        :rtype: None
        """
        self.__width = width
        self.__height = height

        self.start_x, self.start_y = random.randint(1, width - 2), random.randint(1, height - 2)
        self.finish = (random.randint(1, width - 2), random.randint(1, height - 2))

        self._maze = [[1 for _ in range(width)] for _ in range(height)]
        self._maze[self.start_y][self.start_x] = 0

        self.__current_x = self.start_x
        self.__current_y = self.start_y
        self._cells = [(self.__current_x, self.__current_y)]

    def can_go(self, way):
        """ Returns the result of checking whether we can go in a specific direction `way` (up, down, left, right)

        :param way: way for verification
        :type way: str

        :return: result of checking (True/False)
        :rtype: bool
        """
        if way == "up":
            return self.__current_y - 1 > 0 and self._maze[self.__current_y - 1][self.__current_x] == 1
        elif way == "down":
            return self.__current_y < self.__height - 2 and self._maze[self.__current_y + 1][self.__current_x] == 1
        elif way == "left":
            return self.__current_x - 1 > 0 and self._maze[self.__current_y][self.__current_x - 1] == 1
        else:
            return self.__current_x < self.__width - 2 and self._maze[self.__current_y][self.__current_x + 1] == 1

    def get_direction(self, way):
        """ Takes one step in the matrix of values to the side `way`

        :param way: direction of the changed cell
        :type way: str

        :return: `side effect`: modifies a matrix of values
        :rtype: None
        """
        if way == "up":
            self.__current_y -= 1
        elif way == "down":
            self.__current_y += 1
        elif way == "left":
            self.__current_x -= 1
        else:
            self.__current_x += 1
        self._maze[self.__current_y][self.__current_x] = 0

    def create_maze(self):
        """ Generates a matrix of values (maze) at random

        :return: created matrix of values
        :rtype: List[List[int]]
        """
        while (self.__current_x, self.__current_y) != self.finish:
            n = min(self.__width, self.__height)    # obstacle coefficient
            n_cells = self._cells[-(len(self._cells)//n):]
            self.__current_x, self.__current_y = random.choice(n_cells)
            ways = ["up", "down", "left", "right"]
            current_way = random.choice(ways)

            while not any([self.can_go(way) for way in ways]):
                n_cells = [(x, y) for (x, y) in n_cells[-(len(n_cells)//n):]
                           if x != self.__current_x and y != self.__current_y]
                try:
                    self.__current_x, self.__current_y = random.choice(n_cells)
                except IndexError:
                    self.__current_x, self.__current_y = random.choice(self._cells)

            while not self.can_go(current_way):
                ways.remove(current_way)
                current_way = random.choice(ways)

            self.get_direction(current_way)
            self._cells.append((self.__current_x, self.__current_y))
        return self._maze


if __name__ == "__main__":
    from pprint import pprint

    maze = Maze(width=20, height=10)
    maze.create_maze()
    pprint(maze._maze)
