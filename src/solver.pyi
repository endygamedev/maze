from tkinter import (
    Tk,
    Button,
    Label
)

from typing import (
    List,
    Tuple,
    Union
)


class App(Tk):
    def __init__(self, *args, width: int, height: int, zoom: int, **kwargs) -> None:
        super(App, self).__init__(*args, **kwargs)

        self.__width: int
        self.__height: int
        self.__zoom: int

        self.__start: Tuple[int, int]
        self.__finish: Tuple[int, int]
        self.__maze: List[List[int]]

        self.__btn_start: Button
        self.__btn_generate: Button
        self.__label: Label
        ...

    def step(self, matrix: List[List[int]], k: int) -> List[List[int]]: ...
    def update_image(self, matrix: List[List[int]], elem: Union[None, Tuple[int, int]]) -> None: ...
    def scan(self) -> List[List[int]]: ...
    def find_path(self) -> Tuple[List[Tuple[int, int]], List[List[int]]]: ...

    def btn_start_event(self) -> None: ...
    def btn_generate_event(self) -> None: ...
    def gui(self) -> None: ...
