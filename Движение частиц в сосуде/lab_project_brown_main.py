# Лабораторная работа №6. Задание 3
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation
from lab_project_brown_func_collisoin import collision
from lab_project_brown_func_collisoin import collision_with_wall
from lab_project_brown_func_collisoin import collision_in_box

radius = 0.5  # Радиус шариков
mass = 0.5  # Масса шариков

# Границы стенок коробки
Lx = 10
Ly = 10

K = 1 # Коэффициент столкновений между шариками
K1 = 1 # Коэффициент столкновений со стенками

T = 200 # Общее время анимации
n = 1000 # Количество итераций / кадров
tau = np.linspace(0,T,n) # Массив для одного шага анимации
dT = T / n # Время одного шага итерации

N = 8 # Количество чатсиц
p = np.zeros((N,4)) # Массивы для текущих значений положений и скоростей частиц

# Массивы для записи итоговых координат на каждой итерации для итоговой анимации
x = np.zeros((N,n))
y = np.zeros((N,n))

# Массивы для записи х, y, vx, vy для каждой частицы
p[0,0], p[0,1], p[0,2], p[0,3] = -1, 2.5, 1.5, 0.5
p[1,0], p[1,1], p[1,2], p[1,3] = -2, 6, -1, -1
p[2,0], p[2,1], p[2,2], p[2,3] = -3, 3, 1, 1
p[3,0], p[3,1], p[3,2], p[3,3] = -4, 0, 0.5, -1

x[0,0], y[0,0] = p[0,0], p[0,1]
x[1,0], y[1,0] = p[1,0], p[1,1]
x[2,0], y[2,0] = p[2,0], p[2,1]
x[3,0], y[3,0] = p[3,0], p[3,1]

# Массивы для записи х, y, vx, vy для каждой частицы
p[4,0], p[4,1], p[4,2], p[4,3] = 1, -4, -2, 1
p[5,0], p[5,1], p[5,2], p[5,3] = 2, -8, 1, -1
p[6,0], p[6,1], p[6,2], p[6,3] = 3, -4, -2, 1
p[7,0], p[7,1], p[7,2], p[7,3] = 4, -8, 1, -1

x[4,0], y[4,0] = p[4,0], p[4,1]
x[5,0], y[5,0] = p[5,0], p[5,1]
x[6,0], y[6,0] = p[6,0], p[6,1]
x[7,0], y[7,0] = p[7,0], p[7,1]

g = 0.00  # Ускорение свободного падения

def move_func(s, t):
    x, v_x, y, v_y = s

    dxdt = v_x
    dv_xdt = 0

    dydt = v_y
    dv_ydt = - g + g*np.heaviside(-y-Ly,1)

    return dxdt, dv_xdt, dydt, dv_ydt


for k in range(n-1):  # Цикл перебора шагов временеи анимации
    t = [tau[k],tau[k+1]]

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

        # Проверка условий столкновения с первой перегородкой
        res = collision_with_wall(p[m,0],p[m,1],p[m,2],p[m,3],0,-10,-2.5,1,radius,K1)
        p[m,2], p[m,3] = res[0], res[1] # Пересчет скоростей

        # Проверка условий столкновения со второй перегородкой
        res=collision_with_wall(p[m,0],p[m,1],p[m,2],p[m,3],0,2.5,10,1,radius,K1)
        p[m,2], p[m,3] = res[0], res[1] # Пересчет скоростей

        # Проверка условий столкновения с граничными стенками
        res = collision_in_box(p[m,0],p[m,1],p[m,2],p[m,3],Lx,Ly,radius,K1)
        p[m,2], p[m,3] = res[0], res[1] # Пересчет скоростей


    # Циклы перебора частиц для столкновений друг с другом
    for i in range(N): # Базовая частица
        x1, y1, vx1, vy1 = p[i,0], p[i,1], p[i,2], p[i,3] # Запись текущих координат базовой частицы
        x10, y10 = x[i,k], y[i,k] # Запись координат предыдущего шага базовой частицы

        for j in range(i+1,N): # Запись текущих координат остальных частиц
            x2, y2, vx2, vy2 = p[j,0], p[j,1], p[j,2], p[j,3] # Запись текущих
            x20, y20 = x[j,k], y[j,k] # Запись координат предыдущего шага

            # Проверка условий столкновения
            r1 = np.sqrt((x1-x2)**2+(y1-y2)**2)
            r0 = np.sqrt((x10-x20)**2+(y10-y20)**2)
            if  r1 <= radius*2 and r0 > 2*radius:
                res = collision(x1,y1,vx1,vy1,x2,y2,vx2,vy2,radius,mass,mass,K)

                # Перезаписывание условий, в случае столкновения
                p[i,2], p[i,3] = res[0], res[1]
                p[j,2], p[j,3] = res[2], res[3]

# Графический вывод
fig = plt.figure()

plt.plot([Lx, Lx], [-Ly, Ly], '-', color='b')
plt.plot([-Lx, -Lx], [-Ly, Ly], '-', color='b')
plt.plot([-Lx, Lx], [Ly, Ly], '-', color='b')
plt.plot([-Lx, Lx], [-Ly, -Ly], '-', color='b')

plt.plot([0, 0],[-10, -2.5], '-', color='b')
plt.plot([0, 0],[2.5, 10], '-', color='b')

bodys = []

for i in range(n):
    body1, = plt.plot(x[0,i], y[0,i], 'o', color='r', ms=5)
    body2, = plt.plot(x[1,i], y[1,i], 'o', color='r', ms=5)
    body3, = plt.plot(x[2,i], y[2,i], 'o', color='r', ms=5)
    body4, = plt.plot(x[3,i], y[3,i], 'o', color='r', ms=5)
    body5, = plt.plot(x[4,i], y[4,i], 'o', color='b', ms=5)
    body6, = plt.plot(x[5,i], y[5,i], 'o', color='b', ms=5)
    body7, = plt.plot(x[6,i], y[6,i], 'o', color='b', ms=5)
    body8, = plt.plot(x[7,i], y[7,i], 'o', color='b', ms=5)
    bodys.append([body1,body2,body3,body4,body5,body6,body7,body8])

ani = ArtistAnimation(fig, bodys, interval=25)

plt.axis('equal')
plt.xlim(-Lx, Lx)
plt.ylim(-Ly, Ly)
ani.save('results/brown.gif')
# plt.show()
