# Learning to make games with Pyxel

[Pyxel](https://github.com/kitao/pyxel) is a tiny game engine for Python. It gives
you a small window, a 16-color retro palette, and a simple way to draw shapes,
sprites, and text — perfect for learning how games work without fighting a big
framework.

## 1. Install it

```bash
pip install pyxel
```

Pyxel opens a real window, so you need to run these examples on a computer with
a display (not inside a plain terminal-only server).

## 2. The shape every Pyxel game has

Almost every Pyxel game has exactly three parts:

```python
import pyxel

pyxel.init(160, 120)   # 1. SET UP: create a window, 160x120 pixels

def update():
    pass                # 2. UPDATE: runs ~30 times per second. Move things,
                         #    check the keyboard, check for collisions.

def draw():
    pyxel.cls(0)         # 3. DRAW: runs ~30 times per second, right after
    pyxel.text(10, 10, "Hello!", 7)   #    update(). Clear the screen, then
                                       #    draw everything in its new place.

pyxel.run(update, draw)
```

`pyxel.run` takes over the program and calls `update()` then `draw()` forever,
about 30 times a second. That's the whole "game loop" — every game you'll ever
make in Pyxel is built out of those two functions.

- **`update()`** never draws anything. It only changes numbers (positions,
  scores, timers) and reacts to input.
- **`draw()`** never changes game state. It only looks at the current numbers
  and paints the screen.

Keeping that split clean is the single most useful habit for a beginner to
learn — it's what stops games from turning into spaghetti.

## 3. The examples, in order

Run each one with `python3 <filename>` and read the comments — they're written
to be read top to bottom like a mini-lesson.

| File | What it teaches |
| --- | --- |
| `01_window.py` | The absolute minimum: open a window, draw text. `init` / `update` / `draw` / `run`. |
| `02_moving_square.py` | Game *state* (a variable that persists between frames), reading the keyboard with `pyxel.btn`, keeping something inside the screen. |
| `03_catch_game.py` | A full mini-game: multiple falling objects, collision detection, score, lives, and a "game over" state. |

## 4. Ideas to try next (good exercises for a student)

Once `03_catch_game.py` makes sense, these are small, satisfying changes to
attempt — each one only touches a line or two:

- Change the falling speed or spawn rate to make the game harder over time.
- Change the player's color, size, or the shape of the falling objects
  (`pyxel.rect` → `pyxel.circ`).
- Add a second color of falling object that costs a life instead of scoring a
  point.
- Add a sound effect when a star is caught (`pyxel.sounds`, `pyxel.play`).
- Save and show a high score using a plain Python variable.

Pyxel's own examples (`python3 -m pyxel play <name>` after
`python3 -m pyxel copy_examples`) are also worth browsing once these feel
comfortable.
