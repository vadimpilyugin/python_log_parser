"""
Lesson 3: a full mini-game - "Catch the Stars".

New ideas on top of lesson 2:
  - more than one moving thing at once (a list of Star objects)
  - collision detection: did the paddle touch a star?
  - keeping score and lives
  - a game that can be in different "states" (playing vs. game over) and
    switches between them
"""
import pyxel

WIDTH = 160
HEIGHT = 120
PADDLE_W = 24
PADDLE_H = 4
STAR_SIZE = 3
FRAMES_BETWEEN_STARS = 20


class Star:
    """One falling star: its position, and how fast it falls."""

    def __init__(self):
        self.x = pyxel.rndi(0, WIDTH - STAR_SIZE)
        self.y = -STAR_SIZE
        self.speed = pyxel.rndi(1, 3)

    def update(self):
        self.y += self.speed

    def draw(self):
        pyxel.rect(self.x, self.y, STAR_SIZE, STAR_SIZE, 10)  # 10 = yellow


pyxel.init(WIDTH, HEIGHT, title="Lesson 3: Catch the Stars")

# --- game state ---
paddle_x = WIDTH // 2 - PADDLE_W // 2
stars = []
score = 0
lives = 3
game_over = False
frame_count = 0


def reset_game():
    global paddle_x, stars, score, lives, game_over, frame_count
    paddle_x = WIDTH // 2 - PADDLE_W // 2
    stars = []
    score = 0
    lives = 3
    game_over = False
    frame_count = 0


def update():
    global paddle_x, score, lives, game_over, frame_count

    if game_over:
        if pyxel.btnp(pyxel.KEY_R):  # btnp = "button pressed just now"
            reset_game()
        return

    # --- move the paddle, keep it on screen ---
    if pyxel.btn(pyxel.KEY_LEFT):
        paddle_x -= 3
    if pyxel.btn(pyxel.KEY_RIGHT):
        paddle_x += 3
    paddle_x = max(0, min(paddle_x, WIDTH - PADDLE_W))

    # --- spawn a new star every FRAMES_BETWEEN_STARS frames ---
    frame_count += 1
    if frame_count % FRAMES_BETWEEN_STARS == 0:
        stars.append(Star())

    # --- move every star, then decide what happens to it ---
    paddle_y = HEIGHT - 10
    still_falling = []
    for star in stars:
        star.update()

        caught = (
            star.y + STAR_SIZE >= paddle_y
            and star.y <= paddle_y + PADDLE_H
            and star.x + STAR_SIZE >= paddle_x
            and star.x <= paddle_x + PADDLE_W
        )
        missed = star.y > HEIGHT

        if caught:
            score += 1
        elif missed:
            lives -= 1
        else:
            still_falling.append(star)  # keep stars that are still in play

    stars[:] = still_falling

    if lives <= 0:
        game_over = True


def draw():
    pyxel.cls(0)
    paddle_y = HEIGHT - 10

    if game_over:
        pyxel.text(55, 50, "GAME OVER", 8)
        pyxel.text(38, 60, f"score: {score}  (press R)", 7)
        return

    pyxel.rect(paddle_x, paddle_y, PADDLE_W, PADDLE_H, 11)
    for star in stars:
        star.draw()

    pyxel.text(4, 4, f"score: {score}", 7)
    pyxel.text(WIDTH - 44, 4, f"lives: {lives}", 8)


pyxel.run(update, draw)
