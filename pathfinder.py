import pygame
from queue import PriorityQueue
from cell import Cell
from math import sqrt

_ROWS, _COLS = 50, 50
_WIDTH, _HEIGHT = 800, 800
_FRAMERATE = 60


class Grid:
    """
    Represents an interactive, N x N grid in which the user can view a graph algorithm find a path from the
    starting cell to the end cell.
    """

    def __init__(self) -> None:
        """Initializes the state of the grid."""
        self._running = True
        self._rows, self._cols = _ROWS, _COLS
        self._grid = self._create_grid()
        self._start_node, self._end_node = self._grid[0][0], self._grid[self._rows - 1][self._cols - 1]
        self._start_node.is_start_node, self._end_node.is_end_node = True, True
        self._erase_block_on, self._is_creating_blocks, self._is_erasing_blocks = False, False, False
        self._dragging_start_flag, self._dragging_end_flag = False, False
        Cell.set_cell_dimensions(_WIDTH // _COLS, _HEIGHT // _ROWS)
        self._disable_events = False

    def run_app(self) -> None:
        """Starts running the pathfinder visualizer application."""
        try:
            pygame.init()
            pygame.display.set_mode((_WIDTH, _HEIGHT))
            pygame.display.set_caption("Pathfinding Visualizer")
            clock = pygame.time.Clock()
            while self._running:
                clock.tick(_FRAMERATE)
                self._handle_events()
        finally:
            pygame.quit()

    def _end_pathfinder_visualizer(self) -> None:
        """Ends the pathfinder visualizer application."""
        self._running = False

    def _handle_mouse_button_down_events(self) -> None:
        """Handles all the events in which the user presses their mouse button."""
        row, col = self._convert_screen_coordinate_to_grid_coordinate(pygame.mouse.get_pos())
        if self._erase_block_on and not self._is_a_flag_node(row, col):
            self._is_erasing_blocks = True
        elif self._grid[row][col].is_start_node:
            self._dragging_start_flag = True
        elif self._grid[row][col].is_end_node:
            self._dragging_end_flag = True
        elif self._able_to_create_blocks(row, col):
            self._grid[row][col].walkable = False
            self._is_creating_blocks = True

    def _is_a_flag_node(self, row: int, col: int) -> bool:
        """Returns True if the given cell is either the starting node or the end node. Otherwise, it returns False."""
        return self._grid[row][col].is_start_node or self._grid[row][col].is_end_node

    def _handle_mouse_button_up_events(self) -> None:
        """Handles all the events in which the user releases their finger from the mouse button."""
        if self._dragging_start_flag:
            self._dragging_start_flag = False
        elif self._dragging_end_flag:
            self._dragging_end_flag = False
        elif self._is_creating_blocks:
            self._is_creating_blocks = False
        elif self._is_erasing_blocks:
            self._is_erasing_blocks = False

    def _dragging_flag_node(self, dragging_node: str, row: int, col: int) -> None:
        """Drags a flag node (a starting node or an end node) across the grid."""
        if dragging_node == 'drag start flag':
            self._start_node.is_start_node = False
            self._start_node = self._grid[row][col]
            self._start_node.is_start_node = True
        else:
            self._end_node.is_end_node = False
            self._end_node = self._grid[row][col]
            self._end_node.is_end_node = True

    def _handle_mouse_motions_events(self) -> None:
        """Handles all the events in which the user has the mouse on the pygame window."""
        row, col = self._convert_screen_coordinate_to_grid_coordinate(pygame.mouse.get_pos())
        if self._dragging_start_flag and not self._is_a_flag_node(row, col):
            self._dragging_flag_node('drag start flag', row, col)
        elif self._dragging_end_flag and not self._is_a_flag_node(row, col):
            self._dragging_flag_node('drag end flag', row, col)
        elif self._is_erasing_blocks and not self._is_a_flag_node(row, col):
            self._grid[row][col].walkable = True
        elif self._is_creating_blocks and self._able_to_create_blocks(row, col):
            self._grid[row][col].walkable = False

    def _able_to_create_blocks(self, row: int, col: int) -> bool:
        """Returns True if the user is able to create blocks on the given coordinate. Otherwise, it returns False."""
        return not self._erase_block_on and self._grid[row][col].walkable and not self._is_a_flag_node(row, col)

    def _handle_key_events(self, event: pygame.event) -> None:
        """Handles all key presses events in the which is able to do."""
        if event.key == pygame.K_c:
            # clear the grid when the user hits the 'c' key
            self._reset()
        elif event.key == pygame.K_RETURN:
            self._disable_events = True
            self.find_optimal_path()
            self._disable_events = False
        elif event.key == pygame.K_e:
            # if the user hits 'e' key and self._erase_block_on is off, it will turn it on and the user will be able to
            # clear any square but the start node and the end node
            # if the user hits 'e' key and self._erase_block_on is on, it will turn it off.
            self._erase_block_on, self._is_creating_blocks = not self._erase_block_on, False

    def _handle_user_events(self, event: pygame.event) -> None:
        """Handles all the user events that user can do while application runs."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_button_down_events()
        elif event.type == pygame.MOUSEMOTION:
            self._handle_mouse_motions_events()
        elif event.type == pygame.MOUSEBUTTONUP:
            self._handle_mouse_button_up_events()
        elif event.type == pygame.KEYDOWN:
            self._handle_key_events(event)

    def _handle_events(self) -> None:
        """Handles all the pygame events that could occur during the game."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._end_pathfinder_visualizer()
            elif not self._disable_events:
                self._handle_user_events(event)
        self._draw_pathfinder_visualizer()

    @staticmethod
    def _convert_screen_coordinate_to_grid_coordinate(mouse_position: (int, int)) -> (int, int):
        """Converts the given mouse position to its corresponding position on the grid, which is a list of list."""
        row, col = mouse_position
        cell_size = _WIDTH // _ROWS
        return col // cell_size, row // cell_size

    @staticmethod
    def _convert_grid_coordinates_to_screen_coordinate(grid_coordinates: (int, int)) -> (int, int):
        """Converts the given grid coordinates to its corresponding position on the pygame surface."""
        row, col = grid_coordinates
        cell_size = _WIDTH // _ROWS
        return row * cell_size, col * cell_size

    def _reset(self, reset_all_blocks: bool = True) -> None:
        """Resets the state of the grid."""
        white = (255, 255, 255)
        for cell in self:
            if not cell.is_start_node and not cell.is_end_node:
                cell.walkable = (True if reset_all_blocks else cell.walkable)
                cell.color = (white if not reset_all_blocks and cell.walkable else cell.color)
            cell.last_node = None

    def _draw_pathfinder_visualizer(self) -> None:
        """Draws the pathfinder visualizer."""
        surface = pygame.display.get_surface()
        background_color = (255, 255, 255)
        surface.fill(background_color)
        self._draw_grid(surface)
        pygame.display.flip()

    def __iter__(self) -> Cell:
        """Yields every cell on the grid."""
        for row in self._grid:
            for cell in row:
                yield cell

    def _draw_grid(self, surface: pygame.Surface) -> None:
        """Draws the _ROWS x COLS onto the screen."""
        x, y = 0, 0
        for cell in self:
            cell.draw_cell(surface, pygame.Rect(x, y, cell.get_cell_height(), cell.get_cell_width()))
            if cell.col == self._cols - 1:
                x = 0
                y += cell.get_cell_width()
            else:
                x += cell.get_cell_height()

    def _compute_diagonal_distance(self, current_node: Cell) -> float:
        """Approximates the distance from the current node to the end node using the diagonal distance formula."""
        delta_x = abs(current_node.row - self._end_node.row)
        delta_y = abs(current_node.col - self._end_node.col)
        return min(delta_x, delta_y) * sqrt(2) + abs(delta_x - delta_y)

    def _compute_manhattan_distance(self, current_node: Cell) -> int:
        delta_x = abs(current_node.row - self._end_node.row)
        delta_y = abs(current_node.col - self._end_node.col)
        return (delta_x + delta_y) * 4

    def _create_grid(self) -> [[Cell]]:
        """Creates a _ROWS x _COLS grid."""
        return [[Cell(row, col) for col in range(self._cols)] for row in range(self._rows)]

    def _find_neighbors(self, cell: Cell) -> [Cell]:
        """Finds the neighbors of given cell in the grid."""
        neighbors = []
        self.add_valid_neighbor(cell.row + 1, cell.col + 1, neighbors)

        self.add_valid_neighbor(cell.row, cell.col + 1, neighbors)
        self.add_valid_neighbor(cell.row, cell.col - 1, neighbors)

        self.add_valid_neighbor(cell.row - 1, cell.col + 1, neighbors)

        self.add_valid_neighbor(cell.row - 1, cell.col, neighbors)
        self.add_valid_neighbor(cell.row + 1, cell.col, neighbors)

        self.add_valid_neighbor(cell.row + 1, cell.col - 1, neighbors)
        self.add_valid_neighbor(cell.row - 1, cell.col - 1, neighbors)
        return neighbors

    def add_valid_neighbor(self, row: int, col: int, neighbors: [Cell]) -> None:
        """
        If the given coordinate is valid, it will add it as a neighbor to the given cell. Otherwise, it will not be
        added as a neighbor.
        """
        if self._is_valid_coordinate(row, col) and self._grid[row][col].walkable:
            neighbors.append(self._grid[row][col])

    def _is_valid_coordinate(self, row: int, col: int) -> [Cell]:
        """Returns True if the given coordinate is on the grid."""
        return row in range(self._rows) and col in range(self._cols)

    def _set_up_flag_nodes(self) -> None:
        """Sets up both the start node and end node that will be used during the search."""
        self._start_node.walkable, self._end_node.walkable = True, True
        self._start_node.is_start_node, self._end_node.is_end_node = True, True

    def find_optimal_path(self) -> None:
        """Finds the optimal from the start node to the end node using the a star search algorithm."""
        self._set_up_flag_nodes()
        self._reset(reset_all_blocks=False)
        count, self._start_node.g_score = 0, 0
        # self._start_node.f_score = self._compute_manhattan_distance(self._start_node)
        open_set, closed_set = PriorityQueue(), set()
        open_set.put(self._start_node)
        self._start_node.f_score = self._compute_diagonal_distance(self._start_node)

        while not open_set.empty() and self._running:
            current_node = open_set.get()
            current_node.color = (current_node.color if current_node.is_start_node else (255, 0, 0))
            closed_set.add(current_node)
            if current_node.row == self._end_node.row and current_node.col == self._end_node.col:
                self._reconstruct_path(current_node)
                current_node.is_end_node = True
                return
            for neighbor in self._find_neighbors(current_node):
                if self._is_optimal_neighbor(neighbor, current_node, open_set, closed_set) \
                        and neighbor not in open_set.queue:
                    open_set.put(neighbor)
                    neighbor.color = (216, 0, 245)
            self._handle_events()

    def _is_optimal_neighbor(self, neighbor: Cell, current_node: Cell, open_set: PriorityQueue, closed_set: {Cell}) -> bool:
        """Returns True if the given neighbor can be considered part of the optimal path."""
        cells = open_set.queue
        tentative_g_score = current_node.g_score + 1
        if neighbor not in closed_set and (tentative_g_score < neighbor.g_score or neighbor not in cells):
            neighbor.last_node, neighbor.g_score = current_node, current_node.g_score + 1
            # neighbor.f_score = neighbor.g_score + self._compute_manhattan_distance(neighbor)
            neighbor.f_score = neighbor.g_score + self._compute_diagonal_distance(neighbor)
            return True
        return False

    def _reconstruct_path(self, end_node: Cell) -> None:
        """Returns the reconstructed path in which it starts from the end node to the starting node."""
        while end_node is not None:
            end_node.color = (47, 234, 247) if not end_node.is_start_node else end_node.color
            end_node = end_node.last_node
            self._handle_events()


if __name__ == '__main__':
    grid = Grid()
    grid.run_app()
