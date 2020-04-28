# Жесткий астероид

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation
from scipy.integrate import odeint

def collision(x1, vx1, y1, vy1, x2, vx2, y2, vy2, radius1, radius2, mass1, mass2, K):
    """Аргументы функции:
    x1,y1,vx1,vy1 - координаты и компоненты скорости 1-ой частицы
    x2,y2,vx2,vy2 - ... 2-ой частицы
    radius,mass1,mass2 - радиус частиц и их массы (массы разные можно задавать,
    радиус для простоты взят одинаковый)
    K - коэффициент восстановления (K=1 для абсолютного упругого удара, K=0
    для абсолютно неупругого удара, 0<K<1 для реального удара).
    В данном случае коэффициент ВАЖНО положить больше 1, чтобы учесть дополнительную
    кенетическую энергию, возникающую в результате взрыва.
    Функция возвращает компоненты скоростей частиц, рассчитанные по формулам для
    реального удара, если стокновение произошло. Если удара нет, то возвращаются
    те же значения скоростей, что и заданные в качестве аргументов.
    """
    r12 = np.sqrt((x1-x2)**2 + (y1-y2)**2) #расчет расстояния между центрами частиц
    # расчет модулей скоростей частиц
    v1 = np.sqrt(vx1**2 + vy1**2)
    v2 = np.sqrt(vx2**2 + vy2**2)

    #проверка условия на столкновение: расстояние должно быть меньше 2-х радиусов
    if r12 <= radius1 + radius2:
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

        #вычисление угла соприкосновения.
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
        #если условие столкновнеия не выполнено, то скорости частиц не пересчитываются
        VX1, VY1, VX2, VY2 = vx1,vy1,vx2,vy2

    return VX1, VY1, VX2, VY2

# Определяем переменную величину
T = 365 * 24 * 60 * 60 # Общее время анимации
years = 2.5
n = 1000
dT = T / n # Время одного шага итерации
radius1 = 150000000000
radius2 = 150000000000
ae = 3*149*10**9

tau = np.linspace(0, years*T, n)

# Определяем функцию для системы диф. уравнений
def move_func(s, t):
    x, v_x, y, v_y = s

    dxdt = v_x
    dv_xdt = - G * mc * (x - xc) / ((x - xc)**2 + (y - yc)**2)**1.5
    dydt = v_y
    dv_ydt = - G * mc * (y - yc) / ((x - xc)**2 + (y - yc)**2)**1.5

    return dxdt, dv_xdt, dydt, dv_ydt

# Определяем начальные значения и параметры, входящие в систему диф. уравнений
N = 3
p = np.zeros((N,4)) # Массив для координат и скоростей всех точек

# Массивы для записи итоговых координат на каждой итерации для итоговой анимации
x = np.zeros((N,n))
y = np.zeros((N,n))

p[0,0], p[0,1], p[0,2], p[0,3] = ae/3, 0, 0, 29000
p[1,0], p[1,1], p[1,2], p[1,3] = -ae/3, 0, 0, 29000
p[2,0], p[2,1], p[2,2], p[2,3] = ae/5, 0, 0, 40000

x[0,0], y[0,0] = p[0,0], p[0,1]
x[1,0], y[1,0] = p[1,0], p[1,1]
x[2,0], y[2,0] = p[2,0], p[2,1]

mc = 1.9 * 10**(30)
xc = 0
yc = 0

mass1 = 1
mass2 = 2
K = 0

G = 6.67 * 10**(-11)


# Решение задачи и проверка условий столковения
for k in range(n-1):  # Цикл перебора шагов временеи анимации
    t = [tau[k], tau[k+1]]

    for m in range(N):  # Цикл перебора частиц для столкновений со стенками
        s0 = p[m,0], p[m,2], p[m,1], p[m,3]
        sol = odeint(move_func, s0, t)

        # Перезаписываем положения частиц
        p[m,0] = sol[1,0]
        p[m,2] = sol[1,1]
        p[m,1] = sol[1,2]
        p[m,3] = sol[1,3]

        # Заноим новые положения в итоговый массив для анимации
        x[m,k+1], y[m,k+1] = p[m,0], p[m,1]

    # Циклы перебора частиц для столкновений друг с другом
    for i in range(N): # Базовая частица
        x1, y1, vx1, vy1 = p[i,0], p[i,1], p[i,2], p[i,3] # Запись текущих координат базовой частицы
        x10, y10 = x[i,k], y[i,k] # Запись координат предыдущего шага базовой частицы

        for j in range(i+1,N): # Запись текущих координат остальных частиц
            x2, y2, vx2, vy2 = p[j,0], p[j,1], p[j,2], p[j,3] # Запись текущих
            x20, y20 = x[j,k], y[j,k] # Запись координат предыдущего шага

            # Проверка условий столкновения
            r1 = np.sqrt((x1-x2)**2 + (y1-y2)**2)
            r0 = np.sqrt((x10-x20)**2 + (y10-y20)**2)

            if  r1 <= radius1 + radius2 and r0 > radius1 + radius2:
                res = collision(x1, y1, vx1, vy1, x2, y2, vx2, vy2, radius1, radius2, mass1, mass2, K)

                # Перезаписывание условий, в случае столкновения
                p[i,2], p[i,3] = res[0], res[1]
                p[j,2], p[j,3] = res[2], res[3]

# Графический вывод
fig = plt.figure()

bodys = []

for i in range(n):
    bodyc, = plt.plot([0], [0], 'o', color='y', ms=15)
    body1, = plt.plot(x[0,i], y[0,i], 'o', color='r', ms=5)
    body2, = plt.plot(x[1,i], y[1,i], 'o', color='g', ms=5)
    body3, = plt.plot(x[2,i], y[2,i], 'o', color='b', ms=5)
    bodys.append([bodyc, body1, body2, body3])

ani = ArtistAnimation(fig, bodys, interval=25)

plt.axis('equal')
plt.xlim(-ae, ae)
plt.ylim(-ae, ae)
# ani.save('results/brown.gif')
plt.show()
