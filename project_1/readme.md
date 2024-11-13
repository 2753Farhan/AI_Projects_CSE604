# Cosmic Gomoku Game

## Overview
This repository presents **Cosmic Gomoku**, an enhanced Gomoku game using the Pygame framework. The game features a cosmic-themed UI with an animated background, and an AI opponent using the minimax algorithm with alpha-beta pruning.

---

## Key Implementation Features

### 1. Game Architecture
- **Board Size**: 10x10 grid.
- **Display**: 800x800 pixel window with centered 600x600 board.
- **Theme**: Cosmic aesthetic with animated starry background.
- **UI Elements**: Gradient effects, semi-transparent overlays, and enhanced visual feedback.

### 2. AI Implementation

#### Evaluation Function
The AI uses a weighted scoring system for game state evaluation:
- **Win condition (5 in a row)**: 100,000 points
- **Open four**: 50,000 points
- **Closed four**: 10,000 points
- **Open three**: 5,000 points
- **Closed three**: 1,000 points
- **Blocking opponent's three**: 7,500 points
- **Open two**: 500 points
- **Closed two**: 100 points

##### Additional Scoring Factors
- Position bonuses based on distance from center.
- Multipliers for recognizing opponent threats.
- Pattern recognition for open-ended sequences.

### 3. Search Algorithm
- **Algorithm**: Minimax with alpha-beta pruning.
- **Depth**: Searches up to 3 moves deep.
- **Move Ordering**: Prioritizes moves adjacent to existing stones.
- **Pruning Optimization**: Alpha-beta boundaries to reduce search space efficiently.

### 4. UI/UX Considerations
- **Real-time stone placement preview**.
- **Two-player mode** for human vs. human play.
- **Animated star background** enhances immersion.
- **Winning line visualization** for game clarity.
- **Game Over screen** with replay options.

### 5. Technical Optimizations
- **Frame Rate**: Capped at 60 FPS for smooth performance.
- **Efficient Board Management**: 2D arrays for optimized state handling.
- **Smart Move Generation**: Focuses on moves adjacent to stones.
- **Memory-Efficient Pattern Detection**: Improved performance for large searches.

---

## Critical Evaluation

### Strengths
- **UI/UX**: Strong visual feedback and cosmic theme.
- **Sophisticated AI**: Weighted position evaluation function.
- **Efficient Algorithms**: Move generation and pattern detection.
- **Performance**: Smooth animation, robust state management.

### Areas for Improvement
- **AI Depth**: Can be increased with further move ordering optimizations.
- **Pattern Detection**: Caching could improve performance.
- **Opening Book**: Stronger early game moves.
- **Difficulty Levels**: Add adjustable difficulty settings.
- **Game State Saving/Loading**: Persistent gameplay functionality.

---

## Conclusion
Cosmic Gomoku combines robust mechanics with an engaging user interface, featuring challenging AI and immersive cosmic elements. The AI’s evaluation function and search strategies provide a competitive experience, making it a complete and polished game.

---

## Getting Started
### Prerequisites
- Python 3.x
- Pygame

### Installation
```bash
# Clone this repository
git clone https://github.com/username/cosmic-gomoku.git
cd cosmic-gomoku

# Install dependencies
pip install pygame