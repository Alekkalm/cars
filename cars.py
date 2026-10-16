import os
import random
import select
import sys
import termios
import time
import tty

WIDTH, HEIGHT, SPEED = 9, 18, 0.12


def key():
    if not select.select([sys.stdin], [], [], 0)[0]:
        return ""
    return os.read(sys.stdin.fileno(), 3).decode(errors="ignore")


def draw(car, obstacles, score):
    rows = [[" "] * WIDTH for _ in range(HEIGHT)]
    for x, y in obstacles:
        rows[y][x] = "#"
    rows[-1][car] = "A"
    road = "\n".join("|" + "".join(row) + "|" for row in rows)
    print(f"\033[HСчёт: {score}\n{road}", end="", flush=True)


def game():
    car, obstacles, score = WIDTH // 2, set(), 0
    settings = termios.tcgetattr(sys.stdin)

    try:
        tty.setcbreak(sys.stdin)
        print("\033[2J\033[?25l", end="")

        while True:
            pressed = key()
            car = max(
                0,
                min(
                    WIDTH - 1,
                    car
                    + (pressed == "\x1b[C")
                    - (pressed == "\x1b[D"),
                ),
            )

            obstacles = {
                (x, y + 1)
                for x, y in obstacles
                if y + 1 < HEIGHT
            }

            if random.random() < 0.22:
                obstacles.add((random.randrange(WIDTH), 0))

            draw(car, obstacles, score)

            if (car, HEIGHT - 1) in obstacles:
                print(f"\nАвария! Итоговый счёт: {score}")
                break

            score += 1
            time.sleep(SPEED)

    finally:
        termios.tcsetattr(
            sys.stdin,
            termios.TCSADRAIN,
            settings,
        )
        print("\033[?25h", end="", flush=True)


if __name__ == "__main__":
    game()