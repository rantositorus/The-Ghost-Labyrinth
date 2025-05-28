from core.entities import Ghost, PacMan
from core.game_logic import find_shortest_path_bfs

class MoveGhostServices:
    def execute(self, ghost: Ghost, pacman: PacMan):
        path = find_shortest_path_bfs(
            ghost.position,
            pacman.position,
            ghost.maze
        )

        if path and len(path) > 1:
            ghost.move_to(path[1])