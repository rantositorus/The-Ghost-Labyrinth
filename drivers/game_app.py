import pygame
from core.entities import Maze, PacMan, Ghost, Coin
from core.game_logic import GameState
from services.pacman_moves import MovePacManServices
from services.ghost_moves import MoveGhostServices
import config

class GameApp:
    def __init__(self, game_mode: str = "PLAYER_AS_ENEMY"):
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
            Ghost(name="Lutung", start_pos=(config.MAZE_WIDTH - 3, config.MAZE_HEIGHT - 3), maze=self.maze)
        ]
        self.coins = self._place_initial_coins()

        self.game_state = GameState(self.maze, self.pacman, self.ghosts, self.coins)
        self.move_pacman_services = MovePacManServices()
        self.move_ghost_services = MoveGhostServices()

    def _generate_initial_maze(self) -> Maze:
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
            maze_data[8][8+i] = 1
            maze_data[8+i][8] = 1
        
        return Maze(config.MAZE_WIDTH, config.MAZE_HEIGHT, maze_data)

    def _place_initial_coins(self):
        coins = []
        occupieed_positions = [self.pacman.position] + [g.position for g in self.ghosts]
        for y in range(config.MAZE_HEIGHT):
            for x in range(config.MAZE_WIDTH):
                if self.maze.grid[y][x] == 0 and (x, y) not in occupieed_positions:
                    coins.append(Coin(position=(x, y)))
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
                player_controlled_ghost = self.ghosts[0]
                dx, dy = 0, 0

                if event.key == pygame.K_UP:
                    dy = -1
                elif event.key == pygame.K_DOWN:
                    dy = 1
                elif event.key == pygame.K_LEFT:
                    dx = -1
                elif event.key == pygame.K_RIGHT:
                    dx = 1

                if dx != 0 or dy != 0:
                    player_controlled_ghost.set_direction(dx, dy)
                    next_pos = player_controlled_ghost.get_next_position()
                    if player_controlled_ghost.can_move_to(next_pos[0], next_pos[1]):
                        player_controlled_ghost.move_to(next_pos)
                    player_controlled_ghost.set_direction(0, 0)


    def _update_game_logic(self):
        # AI Pac-Man moves
        self.move_pacman_services.execute(self.pacman, self.ghosts, self.game_state.coins)

        # Ghosts move
        for i, ghost in enumerate(self.ghosts):
            if self.game_mode == "PLAYER_AS_ENEMY" and i == 0:
                # The first ghost is controlled by player, its move was handled in _handle_input
                pass 
            else:
                self.move_ghost_services.execute(ghost, self.pacman, self.ghosts)
        
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
                               (coin.position[0] * config.TILE_SIZE + config.TILE_SIZE // 2,
                                coin.position[1] * config.TILE_SIZE + config.TILE_SIZE // 2),
                               config.TILE_SIZE // 4)

        # Draw Pac-Man
        pygame.draw.circle(self.screen, config.YELLOW,
                           (self.pacman.position[0] * config.TILE_SIZE + config.TILE_SIZE // 2,
                            self.pacman.position[1] * config.TILE_SIZE + config.TILE_SIZE // 2),
                           config.TILE_SIZE // 2 - 2)

        # Draw Ghosts
        for ghost in self.ghosts:
            pygame.draw.circle(self.screen, config.RED,
                               (ghost.position[0] * config.TILE_SIZE + config.TILE_SIZE // 2,
                                ghost.position[1] * config.TILE_SIZE + config.TILE_SIZE // 2),
                               config.TILE_SIZE // 2 - 2)
        
        # Display Score
        font = pygame.font.Font(None, 36)
        score_text_surface = font.render(f"Score: {self.pacman.score}", True, config.WHITE)
        self.screen.blit(score_text_surface, (5, 5))

        # Display game over/win messages
        if self.game_state.game_over:
            font = pygame.font.Font(None, 74)
            game_over_text_surface = font.render("GAME OVER", True, config.RED)
            text_rect = game_over_text_surface.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
            self.screen.blit(game_over_text_surface, text_rect)

        elif self.game_state.won:
            font = pygame.font.Font(None, 74)
            win_text_surface = font.render("YOU WIN!", True, config.GREEN)
            text_rect = win_text_surface.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
            self.screen.blit(win_text_surface, text_rect)