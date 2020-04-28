#  Проект: К явлению радуги

import numpy as np
import matplotlib.pyplot as plt

# Начальные параметры R0-радиус, менять нельзя
# Прицельный параметр ro должен от 0 и до 1
R0 = 1
ro = 0.895

# Функция расчитывающая углы
def func(R=R0, ro0=1, n0=1):
    alpha = np.arctan(ro0/np.sqrt(R**2 - ro0**2))
    k = np.sin(alpha)/n0
    beta = np.arctan(k/np.sqrt(1 - k**2))
    phi = 4*beta - 2*alpha
    return phi, beta, alpha

# Массив значений коэффициента преломления
n = np.arange(1.30, 1.41, 0.016)

# Построения падающего луча
xl = []
yl = []

xl0 = -2
yl0 = ro

xl.append(xl0)
yl.append(yl0)

xl1 = -np.sqrt(R0 - ro**2)
yl1 = ro

xl.append(xl1)
yl.append(yl1)

# Построения первых отражённый лучей
xlr = []
ylr = []

for i in n:
    h = np.tan(np.pi - func(R0, ro, n0=i)[2] + func(R0, ro, n0=i)[1])

    xlr0 = - np.sqrt(R0 - ro**2)
    ylr0 = ro
    ylr1 = (ylr0 - h*xlr0 - np.sqrt((-ylr0 + h*xlr0)**2 - (1 + h**2)*(ylr0**2 + h**2*xlr0**2
                                 - 2*ylr0*h*xlr0 - h**2*R0**2)))/(1 + h**2)
    xlr1 = np.sqrt(R0 - ylr1**2)

    xlr.append(xlr0)
    ylr.append(ylr0)
    xlr.append(xlr1)
    ylr.append(ylr1)

# Построения вторых отражённый лучей
XL = []
YL = []
k = 1

for i in n:
    h = np.tan(3*func(R0, ro, n0=i)[1] - func(R0, ro, n0=i)[2])

    xlr0 = xlr[k]
    ylr0 = ylr[k]
    ylr1 = (ylr0 - h*xlr0 - np.sqrt((-ylr0 + h*xlr0)**2 - (1 + h**2)*(ylr0**2 + h**2*xlr0**2
                                 - 2*ylr0*h*xlr0 - h**2*R0**2)))/(1 + h**2)
    xlr1 =np.sqrt(R0 - ylr1**2)

    XL.append(xlr0)
    YL.append(ylr0)
    XL.append(xlr1)
    YL.append(ylr1)
    k += 2

# Построения третьих отражённый лучей
XL1 = []
YL1 = []
k = 1

for i in n:
    h = np.tan(func(R0, ro, n0=i)[0])

    xlr0 = XL[k]
    ylr0 = YL[k]
    ylr1 = -1.5
    xlr1 = (ylr1 - ylr0)/h + xlr0

    XL1.append(xlr0)
    YL1.append(ylr0)
    XL1.append(xlr1)
    YL1.append(ylr1)
    k += 2

# Задание окружности
x = np.arange(-1.2, 1.2, 0.01)
y = np.arange(-1.2, 1.2, 0.01)
X, Y = np.meshgrid(x, y)
fxy = X**2 + Y**2
plt.contour(X, Y, fxy, colors='black', levels=[R0])

# Отображение падающего луча
plt.plot(xl,yl, color='black')

# Отображение преломленных лучей
plt.plot(xlr[0:2], ylr[0:2], color='#ff0000')
plt.plot(XL[0:2], YL[0:2], color='#ff0000')
plt.plot(XL1[0:2], YL1[0:2], color='#ff0000')

plt.plot(xlr[2:4], ylr[2:4], color='#ff8000')
plt.plot(XL[2:4], YL[2:4], color='#ff8000')
plt.plot(XL1[2:4], YL1[2:4], color='#ff8000')

plt.plot(xlr[4:6], ylr[4:6], color='#ffff00')
plt.plot(XL[4:6], YL[4:6], color='#ffff00')
plt.plot(XL1[4:6], YL1[4:6], color='#ffff00')

plt.plot(xlr[6:8], ylr[6:8], color='#00ff00')
plt.plot(XL[6:8], YL[6:8], color='#00ff00')
plt.plot(XL1[6:8], YL1[6:8], color='#00ff00')

plt.plot(xlr[8:10], ylr[8:10], color='#00ffff')
plt.plot(XL[8:10], YL[8:10], color='#00ffff')
plt.plot(XL1[8:10], YL1[8:10], color='#00ffff')

plt.plot(xlr[10:12], ylr[10:12], color='#0000ff')
plt.plot(XL[10:12], YL[10:12], color='#0000ff')
plt.plot(XL1[10:12], YL1[10:12], color='#0000ff')

plt.plot(xlr[12:14], ylr[12:14], color='#8000ff')
plt.plot(XL[12:14], YL[12:14], color='#8000ff')
plt.plot(XL1[12:14], YL1[12:14], color='#8000ff')

plt.axis('equal')
plt.axis('off')
plt.savefig('results/rainbow.png')
plt.show()
