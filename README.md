# 💰 Clash of Coins AI

A grid-based coin collection game built with **Python** and **Pygame**, featuring:
- A human player vs. an intelligent AI agent
- Pathfinding logic using Breadth-First Search (BFS)
- Procedural level generation with accessible coin placement
- Scoreboard, background music, and a clean game loop

> 🚀 Built as part of a learning project to explore game design, AI pathfinding, and Pygame animations.

## 🎮 Gameplay
- You (the green block) and the AI agent (red block) race to collect coins (yellow).
- The map contains walls (black) randomly placed on each level.
- The game ends when all coins are collected. Highest score wins!

## 🧠 AI Logic
The AI uses a BFS algorithm to find the shortest path to the nearest coin while avoiding walls, recalculating its path as the game progresses.

## 🔧 Features
- Smooth grid movement
- Coin and wall generation with accessibility checks
- Background music and sound effects
- Score tracking and winner announcement
- Restart option on game over

## 🕹️ Controls
- **Arrow Keys**: Move the player
- **R**: Restart the game after game over

## 📁 How to Run

1. Make sure you have Python 3 installed.
2. Install dependencies:
   ```bash
   pip install pygame
