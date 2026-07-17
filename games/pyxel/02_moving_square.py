"""
Lesson 2: game state + keyboard input.

"Game state" just means: plain variables that remember something between
frames. Here it's the player's x, y position. update() changes those numbers
based on the keyboard; draw() paints a square at wherever they currently are.

Notice update() never calls a draw function, and draw() never touches the
keyboard. That split keeps games easy to reason about.
"""
import pyxel

pyxel.init(160, 120, title="Lesson 2: Moving Square")

# --- game state ---
player_x = 80
player_y = 60
SPEED = 2
SIZE = 8


def update():
    global player_x, player_y

    if pyxel.btn(pyxel.KEY_LEFT):
        player_x -= SPEED
    if pyxel.btn(pyxel.KEY_RIGHT):
        player_x += SPEED
    if pyxel.btn(pyxel.KEY_UP):
        player_y -= SPEED
    if pyxel.btn(pyxel.KEY_DOWN):
        player_y += SPEED

    # keep the square fully inside the 160x120 window
    player_x = max(0, min(player_x, 160 - SIZE))
    player_y = max(0, min(player_y, 120 - SIZE))

    # press Q to quit
    if pyxel.btn(pyxel.KEY_Q):
        pyxel.quit()


def draw():
    pyxel.cls(1)  # dark blue background
    pyxel.rect(player_x, player_y, SIZE, SIZE, 11)  # x, y, w, h, color
    pyxel.text(4, 4, "arrow keys to move, Q to quit", 7)


pyxel.run(update, draw)
