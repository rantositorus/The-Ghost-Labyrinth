# pacman_game/main.py (Finalisasi)

import pygame
from drivers.game_app import GameApp # Import GameApp yang sudah lengkap

if __name__ == "__main__":
    # game_mode = "PLAYER_AS_ENEMY"
    game_mode = "AI_VS_AI" 
    
    app = GameApp(game_mode)
    app.run()