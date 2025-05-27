class Maze:
    def __init__(self, width: height, initial_data=None):
        self.width = width
        self.height = height
        if initial_data:
            self.grid = initial_data
        else:
            self.grid = [[0 for _ in range(width)] for _ in range(height)]

    def is_wall(self, x, y):
        return self.grid[y][x] == 1
    
    def is_valid_position(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height
    
class Character:
    def __init__(self, name, start_pos, maze: Maze):
        self.name = name
        self.position = start_pos
        self.maze = maze
        self.direction = (0, 0)

    def set_direction(self, dx, dy):
        self.direction = (dx, dy)
    
    def get_next_position(self):
        return (self.pos[0] + self.direction[0], self.pos[1] + self.direction[1])
    
    def move_to(self, new_pos):
        self.pos = new_pos
    
    def can_move_to(self, x, y):
        return self.maze.is_valid_position(x, y) and not self.maze.is_wall(x, y)
    
    def get_neighbors(self, current_pos=None):
        if current_pos is None:
                current_pos = self.pos
        x, y = current_pos
        neighbors = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            if self.can_move_to(new_x, new_y):
                neighbors.append((new_x, new_y))
        return neighbors
    
class Pacman(Character):
    def __init__(self, start_pos, maze: Maze):
        super().__init__("Pacman", start_pos, maze)
        self.score = 0

class Ghost(Character):
    def __init__(self, name, start_pos, maze: Maze):
        super().__init__(name, start_pos, maze)

class Coin:
    def __init__(self, pos):
        self.position = pos
