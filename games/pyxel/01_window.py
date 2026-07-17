"""
Lesson 1: the smallest possible Pyxel program.

Every Pyxel game is built from the same four steps:
    1. pyxel.init(...)      -> open a window
    2. def update(): ...    -> called ~30 times a second, changes state
    3. def draw(): ...      -> called ~30 times a second, right after update
    4. pyxel.run(update, draw)  -> hand control over to Pyxel

This one doesn't move anything yet. It just proves the window works.
"""
import pyxel

pyxel.init(160, 120, title="Lesson 1: Window")


def update():
    # Nothing changes yet, so there is nothing to do here.
    # Pyxel still calls this function 30 times a second.
    pass


def draw():
    pyxel.cls(0)  # clear the screen to color 0 (black)
    pyxel.text(45, 55, "Hello, Pyxel!", 7)  # x, y, text, color (7 = white)


pyxel.run(update, draw)
