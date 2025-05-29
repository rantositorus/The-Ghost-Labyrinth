from core.entities import Ghost, PacMan
from core.game_logic import find_shortest_path_bfs

class MoveGhostServices:
    def execute(self, ghost: Ghost, pacman: PacMan, all_ghosts: list[Ghost]) -> None:
        avoid_positions = [g.position for g in all_ghosts if g != ghost]
        path = find_shortest_path_bfs(
            start_pos=ghost.position,
            target_pos=pacman.position,
            maze=ghost.maze,
            avoid_positions=[],
            avoid_radius=0
        )

        if path and len(path) > 1:
            if path[1] not in avoid_positions:
                ghost.move_to(path[1])