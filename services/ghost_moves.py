from core.entities import Ghost, PacMan
from core.game_logic import find_shortest_path_bfs

class MoveGhostServices:
    def execute(self, ghost: Ghost, pacman: PacMan):
        path = find_shortest_path_bfs(
            start_pos=ghost.position,
            target_pos=pacman.position,
            maze=ghost.maze,
            avoid_positions=[],
            avoid_radius=0
        )

        if path and len(path) > 1:
            ghost.move_to(path[1])