# use_cases/pacman_moves.py

from core.entities import PacMan, Ghost, Coin, Maze
from core.game_logic import find_shortest_path_bfs

class MovePacManUseCase:
    def execute(self, pacman: PacMan, ghosts: list[Ghost], coins: list[Coin]):
        best_path = None
        min_path_len = float('inf')

        ghost_positions = [ghost.pos for ghost in ghosts]

        # Prioritize finding a safe path to a coin
        for coin_pos in coins:
            path_to_coin = find_shortest_path_bfs(
                pacman.pos, coin_pos, pacman.maze, 
                avoid_positions=ghost_positions, avoid_radius=3
            )
            
            if path_to_coin:
                # Basic check: if the next step is too close to a ghost, don't consider this path as ideal
                if len(path_to_coin) > 1:
                    next_step = path_to_coin[1]
                    is_next_step_safe = True
                    for ghost_pos in ghost_positions:
                        if max(abs(next_step[0] - ghost_pos[0]), abs(next_step[1] - ghost_pos[1])) < 2:
                            is_next_step_safe = False
                            break
                    
                    if is_next_step_safe and len(path_to_coin) < min_path_len:
                        best_path = path_to_coin
                        min_path_len = len(path_to_coin)
        
        # If no "safe" path to a coin is found, try to move away from ghosts
        if not best_path:
            farthest_safe_pos = None
            max_safe_dist = -1
            
            # Find the safest adjacent cell (farthest from any ghost)
            for neighbor in pacman.get_neighbors():
                min_dist_to_ghost = float('inf')
                for ghost_pos in ghost_positions:
                    min_dist_to_ghost = min(min_dist_to_ghost, max(abs(neighbor[0] - ghost_pos[0]), abs(neighbor[1] - ghost_pos[1])))
                
                if min_dist_to_ghost > max_safe_dist:
                    max_safe_dist = min_dist_to_ghost
                    farthest_safe_pos = neighbor
            
            if farthest_safe_pos:
                pacman.move_to(farthest_safe_pos)
                return

        # If a best path to a coin was found, move along it
        if best_path and len(best_path) > 1:
            pacman.move_to(best_path[1])