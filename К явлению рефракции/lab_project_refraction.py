# Лабораторная работа №6. Задание 3
import numpy as np
import matplotlib.pyplot as plt

s = 4 # Количество слоев вещества
t = 1 # Коэффициент при y

N = []

n = 1
y = 1

# Цикл расчитывает значения n
for i in range(1, s+2, 1):
    n = n*t*np.sqrt(y)
    y += 1
    N.append(n)

a = np.radians(float(input('Введите угол падения (от 0 до 90 градусов): ')))

# Построение луча
X = []
Y = []

x0 = -4
y0 = 0
y1 = 1
x1 = (y1 - y0)/np.tan(a) + x0

X.append(x0)
Y.append(y0)
X.append(x1)
Y.append(y1)

# Цикл расчитывает значения угла alpha
k = 0
alpha0 = []

for i in range(1, s+1, 1):
    sina = N[k]/N[k+1]*np.sin(a)
    alpha = np.arctan(sina/np.sqrt(1 - sina**2))
    alpha0.append(alpha)
    k += 1

# Расчёт координат для построения лучей
X0 = []
Y0 = []

x0 = (y1 - y0)/np.tan(a) + x0
y0 = 1
y1 = 2
x1 = (y1 - y0)/np.tan(alpha0[0]) + x0

X0.append(x0)
Y0.append(y0)
X0.append(x1)
Y0.append(y1)

# Расчёт координат для построения лучей (можно оформить как цикл)
X1 = []
Y1 = []

x0 = (y1 - y0)/np.tan(alpha0[0]) + x0
y0 = 2
y1 = 3
x1 = (y1 - y0)/np.tan(alpha0[1]) + x0

X1.append(x0)
Y1.append(y0)
X1.append(x1)
Y1.append(y1)


X2 = []
Y2 = []

x0 = (y1 - y0)/np.tan(alpha0[1]) + x0
y0 = 3
y1 = 4
x1 = (y1 - y0)/np.tan(alpha0[2]) + x0

X2.append(x0)
Y2.append(y0)
X2.append(x1)
Y2.append(y1)


X3 = []
Y3 = []

x0 = (y1 - y0)/np.tan(alpha0[2]) + x0
y0 = 4
y1 = 5
x1 = (y1 - y0)/np.tan(alpha0[3]) + x0

X3.append(x0)
Y3.append(y0)
X3.append(x1)
Y3.append(y1)

# Луч видимого объекта
A = []
B = []

x0 = -4
y0 = 0
y1 = 5
x1 = (y1 - y0)/np.tan(a) + x0

A.append(x0)
B.append(y0)
A.append(x1)
B.append(y1)


# Построение
plt.plot(A, B, color='red', linestyle='dashed')
plt.plot(X, Y, color='#ff8000')
plt.plot(X0, Y0, color='#ff8000')
plt.plot(X1, Y1, color='#ff8000')
plt.plot(X2, Y2, color='#ff8000')
plt.plot(X3, Y3, color='#ff8000')


plt.plot(-4, 0, color='black', marker="d", ms=12, label='Наблюдатель')
plt.plot(X3[1], Y3[1], color='#ff8000', marker="*", ms=12, label='Действительное положение объекта')
plt.plot(A[1], B[1], color='red', marker="*", ms=12, label='Видимое положение объекта')

plt.plot([-10, 10],[1, 1], color='black')
plt.plot([-10, 10],[2, 2], color='black')
plt.plot([-10, 10],[3, 3], color='black')
plt.plot([-10, 10],[4, 4], color='black')

plt.legend(loc=2, bbox_to_anchor=(0.4, 0.1))
plt.axis('off')
plt.savefig('results/Ход луча.png')
# plt.show()
