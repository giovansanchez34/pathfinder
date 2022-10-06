import pygame
from math import inf


class Cell:
    """Represents an individual cell on the grid."""
    cell_width = 0
    cell_height = 0

    def __init__(self, row: int, col: int) -> None:
        """Initializes the state of the cell."""
        self._was_block = False
        self.row, self.col = row, col
        self.f_score, self.g_score = inf, inf
        self.last_node = None
        self.walkable = True
        self.color = (255, 255, 255)
        self.is_start_node, self.is_end_node = False, False

    def draw_cell(self, surface: pygame.Surface, cell_surface: pygame.Rect) -> None:
        """Draws the cell onto the given pygame surface."""
        pygame.draw.rect(surface, self.color, cell_surface)
        pygame.draw.rect(surface, (0, 0, 0), cell_surface, 1)

    @property
    def is_start_node(self) -> bool:
        """Returns whether or not the cell is the start node."""
        return self._is_start_node

    @is_start_node.setter
    def is_start_node(self, start_node: bool) -> None:
        """
        Changes the cell to be the start node or just a regular cell. If the cell is the start node, the color of
        the cell will change to bright green, else it will be white.
        """
        if not start_node:
            self.color = (0, 0, 0) if self._was_block else (255, 255, 255)
        else:
            self._was_block = not self.walkable
            # self.walkable = True
            self.color = (106, 255, 20) if start_node else (255, 255, 255)
        self._is_start_node = start_node

    @property
    def is_end_node(self) -> bool:
        """Returns whether or not the cell is the end node."""
        return self._is_end_node

    @is_end_node.setter
    def is_end_node(self, end_node: bool) -> None:
        """
        Changes the cell to be the end node or just a regular cell. If the cell is the end node, the color of the cell
        will change to bright yellow, else it will be white.
        """
        if not end_node:
            self.color = (0, 0, 0) if self._was_block else (255, 255, 255)
        else:
            self._was_block = not self.walkable
            # self.walkable = True
            self.color = (247, 241, 47) if end_node else (255, 255, 255)
        self._is_end_node = end_node

    @classmethod
    def get_cell_height(cls) -> int:
        """Returns the height of the cell."""
        return cls.cell_width

    @classmethod
    def get_cell_width(cls) -> int:
        """Returns the width of the cell."""
        return cls.cell_height

    @classmethod
    def set_cell_dimensions(cls, width: int, height: int) -> None:
        """Sets the width and height of all cell instances."""
        cls.cell_width, cls.cell_height = width, height

    @property
    def color(self) -> (int, int, int):
        """Returns the color of the cell."""
        return self._color

    @color.setter
    def color(self, new_color: (int, int, int)) -> None:
        """Changes the color of the cell."""
        self._color = new_color

    @property
    def walkable(self) -> bool:
        """
        Returns True if the cell can be considered when calculating for the most optimal path. Otherwise,
        it returns False if it cannot be considered.
        """
        return self._walkable

    @walkable.setter
    def walkable(self, is_walkable: bool) -> None:
        """Sets the state of the cell."""
        self.color = (0, 0, 0) if not is_walkable else (255, 255, 255)
        self._walkable = is_walkable

    @property
    def last_node(self) -> "Cell":
        """
        Returns the last node (cell) that the cell considered when searching
        for an optimal path.
        """
        return self._last_node

    @last_node.setter
    def last_node(self, cell) -> None:
        """Sets the last node (cell) that it considered to part of the optimal path."""
        self._last_node = cell

    @property
    def f_score(self) -> int or float:
        """Returns f score (the sum of the heuristic function and the g score) of the cell."""
        return self._f_score

    @f_score.setter
    def f_score(self, new_f_score: int or float) -> None:
        """Sets the new f score of the cell."""
        self._f_score = new_f_score

    @property
    def g_score(self) -> int or float:
        """Returns the g score ( the current distance from the starting node) of the cell."""
        return self._g_score

    @g_score.setter
    def g_score(self, new_g_score: int or float) -> None:
        """Sets the new g score of the cell."""
        self._g_score = new_g_score

    @property
    def row(self) -> int:
        """Returns what row the cell lies in."""
        return self._row

    @row.setter
    def row(self, row_pos: int) -> None:
        """Sets the current row the cell lies in"""
        self._row = row_pos

    @property
    def col(self) -> int:
        """Returns what col the cell lies in."""
        return self._col

    @col.setter
    def col(self, col_pos: int) -> None:
        """Sets the current col the cell lies in"""
        self._col = col_pos

    def __repr__(self) -> str:
        """Returns the representation of the cell, which shows the coordinate of the cell."""
        return f"Cell(row={self.row}, col={self.col})"

    def is_node_next_to_current_node(self, cell: "Cell") -> bool:
        """
        Returns True if the given node(cell) is right next to this node. This means that the node is right directly
        at the top, bottom, left or right side of the current node. Otherwise, it returns False.
        """
        return cell.row == self.row and cell.col + 1 == self.col or \
               cell.row == self.row and cell.col - 1 == self.col or \
               cell.row - 1 == self.row and cell.col == self.col or \
               cell.row + 1 == self.row and cell.col == self.col

    def get_weight_score(self, cell: "Cell") -> int:
        """
        Returns the weight score of the this cell and the given cell. The weight is calculated based on whether or
        not the cell is diagonal or right at the side of the given cell. Side being at the top of the given cell, right
        next to the given cell, left to the given cell or at the bottom of the given cell.
        """
        return (1 if self.is_node_next_to_current_node(cell) else 1.4) * 10

    def __lt__(self, node: "Cell") -> bool:
        """
        Returns True if the current node (cell) has a lower f score than the given node.
        Otherwise, it returns False.
        """
        if isinstance(node, Cell):
            return self.f_score < node.f_score
        else:
            return False
