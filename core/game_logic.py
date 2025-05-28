import collections
from core.entities import Maze, PacMan, Ghost, Coin

class GameState:
    def __init__(self, maze: Maze, pacman: PacMan, ghosts: list[Ghost], coins: list[Coin]):
        self.maze = maze
        self.pacman = pacman
        self.ghosts = ghosts
        self.coins = coins
        self.game_over = False
        self.won = False

    def check_collisions(self):
        for ghost in self.ghosts:
            if ghost.position == self.pacman.position:
                self.game_over = True
                print(f"Game Over! {ghost.name} caught Pacman.")
                break

    def check_coin_eaten(self):
        coin_positions = [c.position for c in self.coins]
        if self.pacman.position in coin_positions:
            coin_to_remove = None
            for coin in self.coins:
                if coin.position == self.pacman.position:
                    coin_to_remove = coin
                    break

            if coin_to_remove:
                self.coins.remove(coin_to_remove)
                self.pacman.score += 10
                print(f"Pacman ate a coin! Score: {self.pacman.score}")
                if not self.coins:
                    self.won = True
                    print("Pacman has eaten all coins! You LOSE!")
    
    def update(self):
        self.check_coin_eaten()
        if not self.won:
            self.check_collisions()

def find_shortest_path_bfs(start_pos: tuple[int, int], target_pos: tuple[int, int], maze: Maze, avoid_positions: list[tuple[int, int]] = None, avoid_radius: int = 2) -> list[tuple[int, int]] | None:
    if avoid_positions is None:
        avoid_positions = []

    queue = collections.deque([(start_pos, [start_pos])])
    visited = {start_pos}

    movements = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while queue:
        current_pos, path = queue.popleft()
        if current_pos == target_pos:
            return path
        
        ## avoidance logic
        if current_pos != start_pos:
            is_too_close_to_avoid = False # Don't avoid the start position itself
            for avoid_p in avoid_positions:
                dist_x = abs(current_pos[0] - avoid_p[0])
                dist_y = abs(current_pos[1] - avoid_p[1])
                if max(dist_x, dist_y) < avoid_radius:
                    is_too_close_to_avoid = True
                    break
    
            if is_too_close_to_avoid:
                continue
        
        x, y = current_pos
        for dx, dy in movements:
            new_x, new_y = x + dx, y + dy
            next_pos = (new_x, new_y)

            if maze.is_valid_position(new_x, new_y) and not maze.is_wall(new_x, new_y):
                if next_pos not in visited:
                    visited.add(next_pos)
                    queue.append((next_pos, path + [next_pos]))
    return None