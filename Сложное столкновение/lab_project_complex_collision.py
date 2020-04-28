# Сложное столкновение

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation
from sympy import *

# Определяем функции
L = Function('L')
phi = Function('phi')
v_phi = Function('v_phi')

# Определяем переменные
t = Symbol('t')

# _____________________ Equation _____________________
print()
print('_____________________ Equation _____________________')

# Определяем уравнение
m = Symbol('m')
g = Symbol('g')
l = Symbol('l')

L = m * l**2 / 2 * v_phi(t)**2 + m * g * l * cos(phi(t))

# Дифференцируем (берем производные)
dLdv_phi = diff(L, v_phi(t))
dLdv_phi_dt = diff(dLdv_phi, t)
print('d/dt (dL/dLdv_phi) = ', dLdv_phi_dt)
print()

dLdphi = diff(L, phi(t))
print('dL/dphi = ', dLdphi)
print()

# Дифференциальное уравнение движения
print(dLdv_phi_dt - dLdphi, '= 0')

# _____________________ Solve _____________________
print()
print('_____________________ Solve _____________________')

# Определяем переменную величину
N = 100
t = np.linspace(0, 10, N)

# Определяем функцию для системы диф. уравнений
def move_func(s, t):
    phi, v_phi, x2, vx2, y2, vy2 = s

    dphidt = v_phi
    dv_phidt = - (g/l) * np.sin(phi)

    dx2dt = vx2
    dvx2dt = 0
    dy2dt = vy2
    dvy2dt = 0

    return dphidt, dv_phidt, dx2dt, dvx2dt, dy2dt, dvy2dt

# ----------------- МОЖНО ИССЛЕДОВАТЬ ПАРАМЕТРЫ: ---------------------------
# Определяем начальные значения и параметры, входящие в систему диф. уравнений
phi0 = 0*np.pi/180 # Начальное отклонение маятника
v_phi0 = 0.0 # Начальная скорость маятника

x20 = 2 # Начальная координата Х - шарика
y20 = -2 # Начальная координата У - шарика
vx20 = -4.5 # Х компонента начальной скорости шарика
vy20 = 0 # У компонента начальной скорости шарика

s0 = phi0, v_phi0, x20, vx20, y20, vy20

g = 10
l = 2
mass1 = 3 # Масса маятника
mass2 = 5 # Масса шарика
K = 0  # Коэффициент столкновений К = 1 - упругое столкновение, К = 0 - неупругое столкновение
radius = 0.1  # Радиус шариков
# ---------------------------------------------------------------------

# Проверка на условия столкновения
move_array = np.ndarray(shape=(len(t), 4)) # Массив для записи координат

for i in range(len(t)-1):

    # Разбиваем все время t на маленькие промежутки tau
    tau = [t[i], t[i+1]]

    # Решаем задачу в маленьком промежутке времени tau
    sol = odeint(move_func, s0, tau)

    # Преобразуем координаы к декартовым
    x1 = l * np.sin(sol[1, 0])
    y1 = - l * np.cos(sol[1, 0])
    vx1 =  sol[1, 1] * l * np.cos(sol[1, 0])
    vy1 =  sol[1, 1] * l * np.sin(sol[1, 0])

    x2 = sol[1, 2]
    vx2 = sol[1, 3]
    y2 = sol[1, 4]
    vy2 = sol[1, 5]

    # Записываем координаты новых положений в массив
    move_array[i, 0] = x1
    move_array[i, 1] = y1
    move_array[i, 2] = x2
    move_array[i, 3] = y2

    r12 = np.sqrt((x1 - x2)**2 + (y1 - y2)**2) # расчет расстояния между центрами частиц
    v1 = np.sqrt(vx1**2 + vy1**2) # расчет модулей скоростей частиц
    v2 = np.sqrt(vx2**2 + vy2**2)

    # Проверка условия на столкновение: расстояние должно быть меньше 2-х радиусов
    if r12 <= 2 * radius:
        '''вычисление углов движения частиц theta1(2), т.е. углов между
        направлением скорости частицы и положительным направлением оси X.
        Если частица  покоится, то угол считается равным нулю. Т.к. функция
        arccos имеет область значений от 0 до Pi, то в случае отрицательных
        y-компонент скорости для вычисления угла theta1(2) надо из 2*Pi
        вычесть значение arccos(vx/v)
        '''
        if v1!=0:
            theta1 = np.arccos(vx1 / v1)
        else:
            theta1 = 0
        if v2!=0:
            theta2 = np.arccos(vx2 / v2)
        else:
            theta2 = 0
        if vy1<0:
            theta1 = - theta1 + 2 * np.pi
        if vy2<0:
            theta2 = - theta2 + 2 * np.pi

        # Вычисление угла соприкосновения.
        if (y1-y2)<0:
            phi = - np.arccos((x1-x2) / r12) + 2 * np.pi
        else:
            phi = np.arccos((x1-x2) / r12)

        # Пересчет  x-компоненты скорости первой частицы
        VX1 = v1 * np.cos(theta1 - phi) * (mass1 - K * mass2) \
            * np.cos(phi) / (mass1 + mass2)\
            + ((1 + K) * mass2 * v2 * np.cos(theta2 - phi))\
            * np.cos(phi) / (mass1 + mass2)\
            + K * v1 * np.sin(theta1 - phi) * np.cos(phi + np.pi / 2)

        # Пересчет y-компоненты скорости первой частицы
        VY1 = v1 * np.cos(theta1 - phi) * (mass1 - K * mass2) \
            * np.sin(phi) / (mass1 + mass2) \
            + ((1 + K) * mass2 * v2 * np.cos(theta2 - phi)) \
            * np.sin(phi) / (mass1 + mass2) \
            + K * v1 * np.sin(theta1 - phi) * np.sin(phi + np.pi / 2)

        # Пересчет x-компоненты скорости второй частицы
        VX2 = v2 * np.cos(theta2 - phi) * (mass2 - K * mass1) \
            * np.cos(phi) / (mass1 + mass2)\
            + ((1 + K) * mass1 * v1 * np.cos(theta1 - phi)) \
            * np.cos(phi) / (mass1 + mass2)\
            + K * v2 * np.sin(theta2 - phi) * np.cos(phi + np.pi / 2)

        # Пересчет y-компоненты скорости второй частицы
        VY2 = v2 * np.cos(theta2 - phi) * (mass2 - K * mass1) \
            * np.sin(phi) / (mass1 + mass2) \
            + ((1 + K) * mass1 * v1 * np.cos(theta1 - phi)) \
            * np.sin(phi) / (mass1 + mass2)\
            + K * v2 * np.sin(theta2 - phi) * np.sin(phi + np.pi / 2)
    else:
        # Если условие столкновнеия не выполнено, то скорости частиц не пересчитываются
        VX1, VY1, VX2, VY2 = vx1, vy1, vx2, vy2

    # Определенные положения и скорости становяться начальными условиями для
    # следующего маленького промежутка времени tau
    phi0 = sol[1, 0]
    #важный момент: если скорость vx направлена против оси  x, то угловая скорость
    #отрицательна, без учета знака получается ерунда
    v_phi0 = sign(VX1)*np.sqrt(VX1**2 + VY1**2) / l

    x20 = x2
    vx20 = VX2
    y20 = y2
    vy20 = VY2

    s0 = phi0, v_phi0, x20, vx20, y20, vy20

# Строим решение в виде графика и анимируем
fig = plt.figure()

bodys = []

for i in range(0, len(t)-1, 1):
    body1, = plt.plot([0, move_array[i, 0]], [0, move_array[i, 1]], 'o-', color='r', ms=5)
    body2, = plt.plot(move_array[i, 2], move_array[i, 3], 'o', color='b', ms=5)

    bodys.append([body1, body2])

ani = ArtistAnimation(fig, bodys, interval=50)
plt.grid()
plt.axis('equal')
plt.xlim(-5,5)
plt.show()
# ani.save('results/complex_collision_acleration.gif')
