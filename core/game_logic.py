import collections
from core.entities import Maze, PacMan, Ghost, Coin

class GameState:
    def __init__(self, maze: Maze, pacman: Pacman, ghosts: list[Ghost], coins: list[Coin]):
        self.maze = maze
        self.pacman = pacman
        self.ghosts = ghosts
        self.coins = coins
        self.game_over = False
        self.won = False
        self.score = 0

    def check_collisions(self):
        for ghost in self.ghosts:
            if ghost.position == self.pacman.position:
                self.game_over = True
                print(f"Game Over! {ghost.name} caught Pacman.")
                break

    def check_coin_eaten(self):
        if self.pacman.position in [coin.position for coin in self.coins]:
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


    def find_shortest_path_bfs(start_pos, target_pos, maze: Maze, avoid_positions=None, avoid_radius=2):
        if avoid_positions is None:
            avoid_positions = []

        queue = collections.deque([(start_pos, [start_pos])])
        visited = {start_pos}

        movements = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        while queue:
            is_too_close_to_avoid = False
            if current_pos != start_pos:
                dist_x = abs(current_pos[0] - avoid_p[0])
                dist_y = abs(current_pos[1] - avoid_p[1])
                if max(dist_x, dist_y) < avoid_radius:
                    is_too_close_to_avoid = True
                    break
        
            if is_too_close_to_avoid:
                continue
            
            if current_pos == target_pos:
                return path
            
            x, y = current_pos
            for dx, dy in movements:
                new_x, new_y = x + dx, y + dy
                new_pos = (new_x, new_y)

                if maze.is_valid_position(new_x, new_y) and not maze.is_wall(new_x, new_y):
                    visited.add(new_pos)
                    queue.append((new_pos, path + [new_pos]))
        return None