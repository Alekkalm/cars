# объяснения кода: https://habr.com/ru/companies/yandex_praktikum/articles/1068624/


#Терминал умеет принимать не только обычный текст, но и специальные управляющие последовательности.
#С их помощью можно перемещать курсор, очищать экран, менять цвет символов и управлять режимом их отображения.

#Чаще всего в таких командах используются ANSI escape-последовательности.
#Они начинаются с управляющего символа Escape, который в строке Python записывается как "\033".
#После него указывается команда для терминала.


# указываем какие библиотеки будем использовать
# файл xxx.py - это "модуль", папка c такими файлами - это "пакет". По коду невозможно определить: мы импортируем модуль или пакет. Поэтому все это будем называть "библиотека".
import os
import random
import sys
import time
import keyboard #работает и на windows и на linux и на mac. нужно установить библиотеку в систему: pip install keyboard

# константы:
WIDTH = 9       # ширина игрового поля в символах
HEIGHT= 18      # высота игрового поля в символах
SPEED = 0.12    # время задержки между кадрами, в секундах


  


def draw(car, obstacles, score):

    #rows = [[" "] * WIDTH for _ in range(HEIGHT)]  #герератор матрицы одинаковых элементов
    
     #создаем двухмерный массив: список пробелов размером с наше игровое поле   
    rows = []
    for i in range(HEIGHT):
        row = [" "] * WIDTH
        rows.append(row)
    
    # заполняем препятствиями
    for x, y in obstacles:
        rows[y][x] = "#"
    
    # устанавливаем автомобиль    
    rows[-1][car] = "A"
    

    #road = "\n".join("|" + "".join(row) + "|" for row in rows)
    
    #делаем из массива символов - строку:
    road=""
    for r in rows:
        road += "|"
        for c in r:
            road += rows[r][c]
        road += "|"
 
 
    #собераем все в одну строку
    s = (
        "\033[H" +              # перемещает курсор в левый верхний угол,
        f"Счёт: {score}" +      # в верхней строке указываем счет,
        "\n" +                  # делаем перенос строки
        f"{road}"               # прицепляем остальное игровое поле
    )
    print(s, end="", flush=True) # flush=True - напечатать немедленно, без задержек.



def game():
    
    # начальные значения:
    car = WIDTH // 2    # позиция машины
    obstacles = set()   # препятствия. Функция set() - встроена в Python, создает пустое множество (коллекция уникальных элементов).
                        # Элементами могут быть любые неизменяемые объекты. Мы будем хранить кортежи чисел - координаты припятствий.
                        # Пример: (5, 12) 
    score = 0           # счет

    print("\033[2J", end="") # очистить экран

    while True:
        
        # Считываем нажатие
        #pressed = key()
        
        # Движение машины
        if keyboard.is_pressed('right'):
            car = min(car + 1, WIDTH - 1)
        if keyboard.is_pressed('left'):
            car = max(car - 1, 0)


        #герератор множества
        #obstacles = {
        #    (x, y + 1)
        #    for x, y in obstacles
        #    if y + 1 < HEIGHT
        #}
        
        
        # Перемещаем препятствия вниз
        new_obstacles = set()
        for x, y in obstacles:
            new_y = y + 1
            if new_y < HEIGHT:
                new_obstacles.add((x, new_y))
        obstacles = new_obstacles
        

        # Добавляем новое препятствие в верхнюю строку. (координата y = 0)
        if random.random() < 0.22: #добавляем не всегда, а в 22% случайных случаев.
            x = random.randrange(WIDTH)
            obstacles.add(x, 0)


        # Рисуем игровое поле
        draw(car, obstacles, score)

        # Проверяем столкновение
        if (car, HEIGHT - 1) in obstacles:
            print(f"\nАвария! Итоговый счёт: {score}")
            break

        score += 1
        time.sleep(SPEED)
           


if __name__ == "__main__":
    game()