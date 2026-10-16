# объяснения кода: https://habr.com/ru/companies/yandex_praktikum/articles/1068624/
# переделано для Windows:
#   переделана фунция key(). использует библиотеку keyboard.
#   удалены библиотеки select, termios, tty
import os
import random
import sys
import time
import keyboard #работает и на windows и на linux и на mac. нужно установить библиотеку в систему: pip install keyboard

WIDTH, HEIGHT, SPEED = 9, 18, 0.12

#работает и на windows и на linux и на mac. нужно установить библиотеку в систему: pip install keyboard
def key():
    if keyboard.is_pressed('right'):
        return '\x1b[C'
    if keyboard.is_pressed('left'):
        return '\x1b[D'
    return ""
    


def draw(car, obstacles, score):
    rows = [[" "] * WIDTH for _ in range(HEIGHT)]
    for x, y in obstacles:
        rows[y][x] = "#"
    rows[-1][car] = "A"
    road = "\n".join("|" + "".join(row) + "|" for row in rows)
    
    s = (
        "\033[H" +      # перемещает курсор в левый верхний угол,
        f"Счёт: {score}" +
        "\n" +          # переход на следующую строку
        f"{road}"       
    )
    print(s, end="", flush=True)


def game():
    car, obstacles, score = WIDTH // 2, set(), 0

    #Терминал умеет принимать не только обычный текст, но и специальные управляющие последовательности.
    #С их помощью можно перемещать курсор, очищать экран, менять цвет символов и управлять режимом их отображения.
    
    #Чаще всего в таких командах используются ANSI escape-последовательности.
    #Они начинаются с управляющего символа Escape, который в строке Python записывается как "\033".
    #После него указывается команда для терминала.
    
    print("\033[2J", end="") # очистить экран
    #print("\033[?25l", end="") # скрыть курсор
    #try:
        # Настройка консоли для чистого отображения
        #print("\033[2J\033[?25l", end="") # очистить экран, скрыть курсор

    while True:
        # Считываем нажатие
        pressed = key()
        # Движение машины
        car = max(
            0,
            min(
                WIDTH - 1,
                car
                + (pressed == "\x1b[C")
                - (pressed == "\x1b[D"),
            ),
        )

        # Перемещаем препятствия вниз
        obstacles = {
            (x, y + 1)
            for x, y in obstacles
            if y + 1 < HEIGHT
        }

        # Добавляем новые препятствия
        if random.random() < 0.22:
            obstacles.add((random.randrange(WIDTH), 0))

        # Рисуем игровое поле
        draw(car, obstacles, score)

        # Проверяем столкновение
        if (car, HEIGHT - 1) in obstacles:
            print(f"\nАвария! Итоговый счёт: {score}")
            break

        score += 1
        time.sleep(SPEED)
            
    #finally:
        #print("\033[?25h", end="", flush=True) #показать курсор


if __name__ == "__main__":
    game()