
# Memory Maze: A Strategic 2D Maze Game

## Overview
*Memory Maze* is a 2D maze game where two players navigate a grid, avoiding traps, collecting bonuses, and using memory tokens to temporarily reveal surrounding tiles. The game combines strategic decision-making and memory management. Players can play against each other or challenge an AI opponent powered by the **Minimax algorithm**.

## Features:
- **Memory Tokens**: Players can reveal adjacent tiles for a limited time to plan their path.
- **Traps**: Players must avoid traps. If a player steps on three traps, they are eliminated.
- **Bonuses**: Bonuses can be collected to gain extra memory tokens.
- **AI Opponent**: The game features an AI that uses **Minimax** and **Alpha-Beta Pruning** for decision-making.
- **Multiplayer Mode**: Supports two players who alternate turns to navigate the maze.

## Demo Video:
https://drive.google.com/file/d/1foi-lBW1IJMTdsLMYoD4zeSGPXe76hv-/view?usp=sharing

## How to Play:
1. **Objective**: The goal is to be the first to reach the center of the maze. Avoid stepping on traps and use memory tokens strategically to navigate the maze.
2. **Controls**:
   - **Arrow Keys**: Move the player in the respective direction (up, down, left, right).
   - **Spacebar**: Use a memory token to reveal surrounding tiles.
   - **Traps**: Stepping on a trap will decrease your chances of winning. The player is eliminated after hitting 3 traps.

## How to Run the Game

### Prerequisites:
- Python 3.x
- Pygame library (for the graphical interface)

### Steps to Run:
1. **Clone the Repository**:
   ```
   git clone https://github.com/Umer-ship-it-bot/memory-maze-game.git
   ```

2. **Install Dependencies**:
   Navigate to the project directory and install the required libraries:
   ```
   pip install -r requirements.txt
   ```

3. **Run the Game**:
   After installation, run the game using the following command:
   ```
   python final_project.py
   ```

4. **Gameplay**:
   - Player 1 (blue) and Player 2 (red) take turns moving on the grid.
   - Players use the **Spacebar** to reveal tiles around them temporarily.
   - The first player to reach the center of the maze wins. If a player is eliminated by hitting 3 traps, the other player wins.

## Project Report

A detailed **Project Report** is available for download, where we discuss the game design, AI methodology, and implementation details. 

[Download Full Project Report here](./Project_Report.pdf).

## Contributing

We welcome contributions to the project. If you'd like to contribute, feel free to fork this repository, make your changes, and submit a pull request. For any issues or improvements, open an issue in the repository.

