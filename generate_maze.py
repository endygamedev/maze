from pprint import pprint
import random


class Maze:
    def __init__(self, *, width, height):
        self.__width = width
        self.__height = height

        self.start_x, self.start_y = random.randint(1, width//2), random.randint(1, height//2)
        self.finish = (random.randint(width//2, width - 2), random.randint(height//2, height - 2))

        self.__maze = [[1 for _ in range(width)] for _ in range(height)]
        self.__maze[self.start_x][self.start_y] = 0

        self.__current_x = self.start_x
        self.__current_y = self.start_y
        self.__cells = [(self.__current_x, self.__current_y)]

    def can_go(self, way):
        if way == "up":
            return self.__current_x - 1 > 0 and self.__maze[self.__current_x - 1][self.__current_y] == 1
        elif way == "down":
            return self.__current_x < len(self.__maze) - 2 and self.__maze[self.__current_x + 1][self.__current_y] == 1
        elif way == "left":
            return self.__current_y - 1 > 0 and self.__maze[self.__current_x][self.__current_y - 1] == 1
        else:
            return self.__current_y < len(self.__maze[0]) - 2 and self.__maze[self.__current_x][self.__current_y + 1] == 1

    def get_direction(self, way):
        if way == "up":
            self.__current_x -= 1
        elif way == "down":
            self.__current_x += 1
        elif way == "left":
            self.__current_y -= 1
        else:
            self.__current_y += 1
        self.__maze[self.__current_x][self.__current_y] = 0

    def create_maze(self):
        while (self.__current_x, self.__current_y) != self.finish:
            ncells = self.__cells[-(len(self.__cells)//(self.__width//2)):]
            self.__current_x, self.__current_y = random.choice(ncells)
            ways = ["up", "down", "left", "right"]
            current_way = random.choice(ways)

            while not any([self.can_go(way) for way in ways]):
                ncells = [(x, y) for (x, y) in ncells[-(len(ncells)//(self.__width//2)):] if x != self.__current_x and y != self.__current_y]
                try:
                    self.__current_x, self.__current_y = random.choice(ncells)
                except IndexError:
                    self.__current_x, self.__current_y = random.choice(self.__cells)

            while not self.can_go(current_way):
                ways.remove(current_way)
                current_way = random.choice(ways)

            self.get_direction(current_way)
            self.__cells.append((self.__current_x, self.__current_y))
        return self.__maze


if __name__ == "__main__":
    maze = Maze(width=200, height=100)
    pprint(maze.create_maze())