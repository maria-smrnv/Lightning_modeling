import matplotlib.pyplot as plt
from IPython.display import HTML, display
import matplotlib.animation as animation
import numpy as np
import argparse

def parser():
    parser = argparse.ArgumentParser(description="Парсинга параметров запуска.")

    parser.add_argument('--width', type=int, default=100, help="Ширина сетки")
    parser.add_argument('--height', type=int, default=100, help="Высота сетки")
    parser.add_argument('--eta', type=int, default=3, help="Гиперпараметр свойств среды")
    parser.add_argument('--name', type=str, default="", help="Название выходного файла")

    return parser.parse_args()


# Функция создает и возвращает массив с начальными граничными условиями для задачи
def make_grid(shape):
    grid = np.full(shape, np.nan) # Создается массив b заданной формы (shape) заполненный NaN
    dims = len(shape) # Вычисляется количество измерений массива shape
    grid = np.moveaxis(grid, -1, 0) # Последняя ось массива grid перемещается на первое место
    grid[(shape[0] // 2,) * (dims - 1)][:3] = 0 # Создает точку роста (центральные клетки в первых трех строках сетки)
    grid[...,-1] = 1 # Нижний ряд заполняем 1 (потенциал земли)
    grid = np.moveaxis(grid, -1, 0) # Возвращаем оси в исходный порядок
    return grid # Возвращаем сетку

def make_grid2(shape):
    grid = np.full(shape, np.nan)  # Создаем массив с заданной формой, заполненный NaN

    # Центральная точка роста
    center_x = shape[0] // 2
    grid[center_x, :3] = 0  # Заполняем первые три клетки центрального ряда нулями

    # Нижний ряд заполняем 1 (потенциал земли)
    grid[...,-1] = 1 

    # Добавляем прямоугольник
    rect_height = 40
    rect_width = 2
    center_offset = (shape[1] // 2) - (rect_width // 2 + 35)  # Отступ от центра по горизонтали
        
    grid = np.moveaxis(grid, -1, 0) 
    grid[-rect_height:, center_offset:center_offset + rect_width] = 1  # Добавляем прямоугольник
    return grid


#Cоздает анимацию
def movie(vol, iskwargs={}, interval=10, repeat_delay=1000, name="out.mp4", **kwargs):
    fig = plt.figure()
    plts = [[plt.imshow(A, **iskwargs)] for A in vol]
    ani = animation.ArtistAnimation(fig, plts, interval=interval, blit=True, repeat_delay=repeat_delay, **kwargs)
    ani.save("animation/"+name)
