from modulation import modulation, pcg, datdot
from utils import movie, make_grid, parser
import numpy as np
from time import time

args = parser()

grid_width = args.width
grid_height = args.height
eta = args.eta
file_name = args.name

# Создаем начальную структуру
grid = make_grid((grid_width, grid_height))
print(f"Размерность начальной структуры: {grid.shape}")
print(f"Гиперпараметр свойств среды: \u03B7 = {eta}")

# Запуск моделирования
start_time = time()
Phis_vis_dbm = modulation(grid, max_n=2500, eta=eta)
total_time = time() - start_time

# Вывод статистики по времени работы
pcg_time = pcg.at
pcg_dot_time = pcg.dot
pcg_get_z_time = pcg.get_z

print(f"\nВремя работы:")
print(f"  Время выполнения PCG: {pcg_time:.2f}s ({(pcg_time / total_time) * 100:.2f}%)")
print(f"  Время вычисления dot-операций: {pcg_dot_time:.2f}s ({(pcg_dot_time / total_time) * 100:.2f}%)")
print(f"  Время вычисления get_z: {pcg_get_z_time:.2f}s ({(pcg_get_z_time / total_time) * 100:.2f}%)")
print("-" * 50)

# Статистика по времени вычислений для операций с матрицами и векторами
dot_vec_time = datdot.vectime
dot_mat_time = datdot.mattime
vec_count = datdot.veccount
mat_count = datdot.matcount

print(f"Время работы с матрицами и векторами:")
print(f"  Время выполнения векторных операций: {dot_vec_time:.2f}s ({(dot_vec_time / total_time) * 100:.2f}%) - {vec_count} раз(а)")
print(f"  Время выполнения матричных операций: {dot_mat_time:.2f}s ({(dot_mat_time / total_time) * 100:.2f}%) - {mat_count} раз(а)")
print("-" * 50)
print(f"Общая продолжительность моделирования: {total_time:.2f}s")

# Визуализация результата
file_name = f"{grid.shape[0]}x{grid.shape[1]}(eta={eta}).mp4" if file_name == "" else file_name
movie(np.sqrt(abs(Phis_vis_dbm)), iskwargs={'cmap': 'Blues'}, interval=5, name=file_name)

print(f"\nВизуализация сохранена в файл: \"{file_name}\"\n")
