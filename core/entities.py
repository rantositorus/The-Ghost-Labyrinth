class Maze:
    def __init__(self, width: int, height: int, initial_grid: list[list[int]] = None):
        self.width = width
        self.height = height
        self.grid = initial_grid if initial_grid is not None else [[0 for _ in range(self.width)] for _ in range (self.height)]

    def is_wall(self, x: int, y: int) -> bool:
        if not self.is_valid_position(x, y):
            return True
        return self.grid[y][x] == 1
    
    def is_valid_position(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height
    
class Character:
    def __init__(self, name: str, start_pos: tuple[int, int], maze: Maze):
        self.name = name
        self.position = start_pos
        self.maze = maze
        self.direction = (0, 0)

    def set_direction(self, dx: int, dy: int):
        self.direction = (dx, dy)
    
    def get_next_position(self) -> tuple[int, int]:
        return (self.position[0] + self.direction[0], self.position[1] + self.direction[1])
    
    def move_to(self, new_pos: tuple[int, int]):
        self.position = new_pos
    
    def can_move_to(self, x: int, y: int) -> bool:
        return self.maze.is_valid_position(x, y) and not self.maze.is_wall(x, y)
    
    def get_neighbors(self, current_pos: tuple[int, int] = None) -> list[tuple[int, int]]:
        if current_pos is None:
                current_pos = self.position
        x, y = current_pos
        neighbors = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            if self.can_move_to(new_x, new_y):
                neighbors.append((new_x, new_y))
        return neighbors
    
class PacMan(Character):
    def __init__(self, start_pos: tuple[int, int], maze: Maze):
        super().__init__("Pacman", start_pos, maze)
        self.score = 0

class Ghost(Character):
    def __init__(self, name: str, start_pos: tuple[int, int], maze: Maze):
        super().__init__(name, start_pos, maze)

class Coin:
    def __init__(self, position: tuple[int, int]):
        self.position = position
