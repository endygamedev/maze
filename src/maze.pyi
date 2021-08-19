from typing import (
    List,
    Tuple
)


class Maze:
    def __init__(self, *, width: int, height: int) -> None:
        self.__width: int
        self.__height: int

        self.start_x: int
        self.start_y: int
        self.finish: Tuple[int, int]

        self._maze: List[List[int]]

        self.__current_x: int
        self.__current_y: int

        self._cells = List[Tuple[int, int]]
        ...

    def can_go(self, way: str) -> bool: ...
    def get_direction(self, way: str) -> None: ...
    def create_maze(self) -> List[List[int]]: ...
