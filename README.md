# 🐍 Snake

A polished, feature-rich Snake game built with **Python + Tkinter** — created as a CBSE Class XI Computer Science final term project.

![Python](https://img.shields.io/badge/Python-3.x-blue) ![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green) ![License](https://img.shields.io/badge/License-MIT-yellow)

## Features

- 🎮 Smooth grid-based movement with rounded, gradient-colored snake body
- 🏆 Persistent high score (saved to `highscore.json`)
- ⚡ Three difficulty levels — Easy / Medium / Hard
- 📈 Progressive level system — speed increases as you score
- ⭐ Bonus food (pulsing gold) worth extra points, appears periodically and expires
- ⏸️ Pause / Resume support
- 🖥️ Animated main menu with a live demo snake
- 🔊 Optional sound effects (Windows only via `winsound`, silently skipped elsewhere)
- 🎨 Custom dark theme with decorative bezel frame and HUD panel

## Requirements

- Python 3.x
- Tkinter (bundled with standard Python installation)

No external/third-party packages required.

## Controls

| Key            | Action                     |
|----------------|----------------------------|
| Arrow Keys     | Move the snake             |
| Space          | Pause / Resume             |
| D              | Change difficulty (menu)   |
| Enter          | Start / Restart game       |
| M              | Return to menu (game over) |
| Q              | Quit                       |

## Project Structure

```
├── snake.py           # Main game source code
├── highscore.json     # Auto-generated high score file
├── Screenshot1.png
├── Screenshot2.png
└──README.md
```

## Concepts Demonstrated

| Concept                   | Where it's used                              |
|----------------------------|-----------------------------------------------|
| Object-Oriented Programming| `Snake` class — encapsulation of state/logic  |
| Event-driven programming   | Tkinter key bindings, `after()` game loop      |
| File handling               | JSON read/write for high score persistence    |
| Data structures             | Snake body as a list of `(x, y)` tuples        |
| Control structures          | Finite state machine (MENU/PLAY/PAUSE/OVER)   |
| Recursion                  | Collision-safe recursive food placement        |
| GUI design                 | Canvas drawing, color interpolation/gradients |

## How It Works

The game runs on a finite state machine with four states — `MENU`, `PLAY`, `PAUSE`, and `OVER` — driven by Tkinter's event loop. Each game tick recalculates the snake's head position, checks wall/self collisions, updates food/bonus/score/level, and re-renders the canvas via `root.after()`.
