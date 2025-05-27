# use_cases/ghost_moves.py

from core.entities import Ghost, PacMan
from core.game_logic import find_shortest_path_bfs

class MoveGhostUseCase:
    def execute(self, ghost: Ghost, pacman: PacMan):
        # Ghost AI simply chases Pac-Man using BFS
        path = find_shortest_path_bfs(ghost.pos, pacman.pos, ghost.maze)
        if path and len(path) > 1:
            ghost.move_to(path[1])