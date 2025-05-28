from core.entities import PacMan, Ghost, Coin
from core.game_logic import find_shortest_path_bfs

class MovePacManServices:
    def execute(self, pacman: PacMan, ghosts: list[Ghost], coins: list[Coin]):
        best_path = None
        min_path_len = float('inf')

        ghost_positions = [ghost.position for ghost in ghosts]

        for coin in coins:
            path_to_coin = find_shortest_path_bfs(
                start_pos=pacman.position,
                target_pos=coin.position,
                maze=pacman.maze,
                avoid_positions=ghost_positions,
                avoid_radius=3
            )

            if path_to_coin:
                is_next_step_safe = True
                if len(path_to_coin) > 1:
                    next_step = path_to_coin[1]
                    for ghost_pos in ghost_positions:
                        if max(abs(next_step[0] - ghost_pos[0]), abs(next_step[1] - ghost_pos[1])) < 2:
                            is_next_step_safe = False
                            break
                
                if is_next_step_safe and len(path_to_coin) < min_path_len:
                    best_path = path_to_coin
                    min_path_len = len(path_to_coin)
                
        if not best_path:
            farthest_safe_pos = pacman.position
            max_safe_dist = -1
            valid_neighbors = pacman.get_neighbors()
        
            if not valid_neighbors:
                return

            for neighbor in valid_neighbors:
                min_dist_to_ghost = float('inf')

                for ghost_pos in ghost_positions:
                    dist = max(abs(neighbor[0] - ghost_pos[0]), abs(neighbor[1] - ghost_pos[1]))
                    min_dist_to_ghost = min(min_dist_to_ghost, dist)
                
                if min_dist_to_ghost > max_safe_dist:
                    max_safe_dist = min_dist_to_ghost
                    farthest_safe_pos = neighbor
                
            if farthest_safe_pos != pacman.position:
                pacman.move_to(farthest_safe_pos)
            return
            
        if best_path and len(best_path) > 1:
            pacman.move_to(best_path[1])