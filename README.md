# Python Arcade Collection

A collection of classic arcade games implemented in Python using Pygame.

## Games Included

### 1. Snake Game
- Classic snake gameplay with modern visuals
- Grid-based movement with wall crossing feature
- Score tracking and game over screen
- Smooth animations and visual effects
- Controls: Arrow keys to move, ESC for menu

### 2. Hangman
- Multiple word categories with extensive vocabulary (100+ words each):
  - Animals: From common pets to exotic wildlife
  - Crypto: Comprehensive blockchain and cryptocurrency terms
  - AI: Artificial Intelligence concepts and terminology
  - LLMs: Large Language Models and NLP terminology
- Smart word selection system to avoid repetition
- Detailed hints for educational value
- Hint system (Ctrl+H to show hints)
- Animated drawing of the hangman
- Visual feedback for correct/incorrect guesses
- Controls: Type letters to guess, ESC for menu

### 3. Pong
- Single-player vs AI with three difficulty levels
- Dynamic AI behavior with realistic paddle movement
- Score limit of 10 points to win
- Player and AI labels with score display
- Controls: W/S keys to move, ESC for menu

### 4. Tetris
- Classic Tetris gameplay with modern interface
- Score system and level progression
- Next piece preview and score display
- Controls: Arrow keys to move/rotate, ESC for menu

## Features

### Main Menu
- Dynamic game previews with animations
- Smooth transitions between games
- Easy navigation with arrow keys
- Visual feedback for selected games

### Common Features
- Consistent ESC key behavior across all games
- Modern UI with clean visuals
- Score tracking and high scores
- Game over screens with restart options
- Smooth animations and transitions

## Technical Details

### Requirements
- Python 3.x
- Pygame library

### Installation
1. Clone the repository
2. Install dependencies:
```bash
pip install pygame
```
3. Run the game:
```bash
python main.py
```

### Controls
- Arrow Keys: Navigation in menus and games
- ESC: Return to previous menu/quit
- Game-specific controls are shown in each game

## Development

### Code Structure
- `main.py`: Main game launcher
- `games/`: Individual game modules
  - `snake/`: Snake game files
  - `hangman/`: Hangman game files
  - `pong/`: Pong game files
  - `tetris/`: Tetris game files
- `utils/`: Shared utilities and effects
  - `effects.py`: Animation and visual effects
  - `sounds/`: Game sound effects

### Features Added
- Dynamic game previews in main menu
- Transition effects between screens
- Unified control scheme
- Score tracking system
- Sound effects for games
- Error handling and performance optimizations

## Updates and Changes
- Added wall crossing feature to Snake game
- Implemented AI difficulty levels in Pong
- Enhanced Hangman with expanded vocabulary (400+ words total)
- Added detailed hints and descriptions for all words
- Added score limit and winner screen to Pong
- Improved visual feedback across all games
- Fixed various bugs and performance issues
- Added preview animations for all games
- Standardized menu navigation and controls

## Contributing
Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Submitting pull requests

## License
This project is open source and available under the MIT License. 