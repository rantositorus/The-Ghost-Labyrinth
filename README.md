# The-Ghost-Labyrinth

| Name           | NRP        | Kelas     |
| ---            | ---        | ----------|
| Mirza Zaki Rafii | 5025221018 | Design and Analysis Algorithm (H) |
| Genta Putra Prayoga | 5025221040 | Design and Analysis Algorithm (D) |
| Ranto Bastara Hamonangan Sitorus | 5025221228 | Design and Analysis Algorithm (H) | 
|

A simple Pac-Man-inspired AI game built with Python and Pygame. The game features an AI-controlled Pac-Man and AI/Player-controlled ghosts navigating a maze, collecting coins, and avoiding each other.

## Features

- **AI Pac-Man:** Uses BFS pathfinding to collect coins and avoid ghosts.
- **AI Ghosts:** Chase Pac-Man using shortest path logic.
- **Player Mode:** Optionally control a ghost using arrow keys.
- **Customizable Maze:** Maze and coin placement are generated at runtime.
- **Score Tracking:** Pac-Man earns points for collecting coins.
- **Win/Lose Conditions:** Game ends when Pac-Man collects all coins or is caught by a ghost.

## Project Structure

- [`main.py`](main.py): Entry point to run the game.
- [`core/entities.py`](core/entities.py): Defines Maze, PacMan, Ghost, and Coin classes.
- [`core/game_logic.py`](core/game_logic.py): Game state management and BFS pathfinding.
- [`drivers/game_app.py`](drivers/game_app.py): Main game loop, rendering, and input handling.
- [`services/pacman_moves.py`](services/pacman_moves.py): Pac-Man AI movement logic.
- [`services/ghost_moves.py`](services/ghost_moves.py): Ghost AI movement logic.
- [`config.py`](config.py): Game configuration and color constants.

## Requirements

- Python 3.10+
- pygame

Install dependencies:
```sh
pip install pygame
```

To run the game:
```sh
python main.py
```
