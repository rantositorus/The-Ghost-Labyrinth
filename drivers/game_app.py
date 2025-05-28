import pygame
from core.entities import Maze, PacMan, Ghost, Coin
from core.game_logic import GameState
from use_cases.pacman_moves import MovePacManUseCase
from use_cases.ghost_moves import MoveGhostUseCase
import config

class GameApp:
    def __init__(self, game_mode="PLAYER_AS_ENEMY"):
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("Pac-Man AI")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_mode = game_mode

        self.maze = self._generate_initial_maze()
        self.pacman = PacMan(start_pos=(1, 1), maze=self.maze)
        self.ghosts = [
            Ghost(name="Jacobi", start_pos=(config.MAZE_WIDTH - 2, config.MAZE_HEIGHT - 2), maze=self.maze),
            Ghost(name="Azril", start_pos=(config.MAZE_WIDTH - 2, 1), maze=self.maze)
        ]
        self.coins = self._place_initial_coins()

        self.game_state = GameState(self.maze, self.pacman, self.ghosts, self.coins)
        self.move_pacman_use_case = MovePacManUseCase()
        self.move_ghost_use_case = MoveGhostUseCase()

    def _generate_initial_maze(self):
        maze_data = [[1 for _ in range(config.MAZE_WIDTH)] for _ in range(config.MAZE_HEIGHT)]
        for y in range(1, config.MAZE_HEIGHT - 1):
            for x in range(1, config.MAZE_WIDTH - 1):
                maze_data[y][x] = 0

        # Add some specific walls
        for i in range(5):
            maze_data[3][3+i] = 1
            maze_data[3+i][3] = 1
            maze_data[config.MAZE_HEIGHT - 4][config.MAZE_WIDTH - 4 - i] = 1
            maze_data[config.MAZE_HEIGHT - 4 - i][config.MAZE_WIDTH - 4] = 1
        return Maze(config.MAZE_WIDTH, config.MAZE_HEIGHT, maze_data)

    def _place_initial_coins(self):
        coins = []
        for y in range(config.MAZE_HEIGHT):
            for x in range(config.MAZE_WIDTH):
                if self.maze.grid[y][x] == 0 and \
                   (x, y) != self.pacman.pos and \
                   not any((x, y) == g.pos for g in self.ghosts):
                    coins.append(Coin(pos=(x, y)))
        return coins

    def run(self):
        while self.running:
            self._handle_input()
            if not self.game_state.game_over and not self.game_state.won:
                self._update_game_logic()
            self._draw_elements()
            self.clock.tick(config.FPS)
            pygame.display.flip()

        pygame.quit()

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.game_mode == "PLAYER_AS_ENEMY" and event.type == pygame.KEYDOWN:
                # Player controls the first ghost
                ghost_to_move = self.ghosts[0]
                if event.key == pygame.K_UP:
                    ghost_to_move.set_direction(0, -1)
                elif event.key == pygame.K_DOWN:
                    ghost_to_move.set_direction(0, 1)
                elif event.key == pygame.K_LEFT:
                    ghost_to_move.set_direction(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    ghost_to_move.set_direction(1, 0)
                
                # Apply player ghost move immediately
                next_pos = ghost_to_move.get_next_position()
                if ghost_to_move.can_move_to(next_pos[0], next_pos[1]):
                    ghost_to_move.move_to(next_pos)
                ghost_to_move.set_direction(0,0) # Reset direction


    def _update_game_logic(self):
        # AI Pac-Man moves
        self.move_pacman_use_case.execute(self.pacman, self.ghosts, self.game_state.coins)

        # Ghosts move
        for i, ghost in enumerate(self.ghosts):
            if self.game_mode == "PLAYER_AS_ENEMY" and i == 0:
                # The first ghost is controlled by player, its move was handled in _handle_input
                pass 
            else:
                self.move_ghost_use_case.execute(ghost, self.pacman)
        
        # Update game state after all moves
        self.game_state.update()

    def _draw_elements(self):
        self.screen.fill(config.BLACK)

        # Draw maze
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                if self.maze.is_wall(x, y):
                    pygame.draw.rect(self.screen, config.BLUE, (x * config.TILE_SIZE, y * config.TILE_SIZE, config.TILE_SIZE, config.TILE_SIZE))
                else:
                    pygame.draw.rect(self.screen, config.BLACK, (x * config.TILE_SIZE, y * config.TILE_SIZE, config.TILE_SIZE, config.TILE_SIZE))

        # Draw coins
        for coin in self.game_state.coins:
            pygame.draw.circle(self.screen, config.GREEN,
                               (coin.pos[0] * config.TILE_SIZE + config.TILE_SIZE // 2,
                                coin.pos[1] * config.TILE_SIZE + config.TILE_SIZE // 2),
                               config.TILE_SIZE // 4)

        # Draw Pac-Man
        pygame.draw.circle(self.screen, config.YELLOW,
                           (self.pacman.pos[0] * config.TILE_SIZE + config.TILE_SIZE // 2,
                            self.pacman.pos[1] * config.TILE_SIZE + config.TILE_SIZE // 2),
                           config.TILE_SIZE // 2 - 2)

        # Draw Ghosts
        for ghost in self.ghosts:
            pygame.draw.circle(self.screen, config.RED,
                               (ghost.pos[0] * config.TILE_SIZE + config.TILE_SIZE // 2,
                                ghost.pos[1] * config.TILE_SIZE + config.TILE_SIZE // 2),
                               config.TILE_SIZE // 2 - 2)
        
        # Display Score
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {self.pacman.score}", True, config.WHITE)
        self.screen.blit(text, (5, 5))

        # Display game over/win messages
        if self.game_state.game_over:
            font = pygame.font.Font(None, 74)
            text = font.render("GAME OVER", True, config.RED)
            text_rect = text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)
        elif self.game_state.won:
            font = pygame.font.Font(None, 74)
            text = font.render("YOU WIN!", True, config.GREEN)
            text_rect = text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)