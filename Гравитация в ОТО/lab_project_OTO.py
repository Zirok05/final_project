# Гравитация в ОТО

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def f(r, t, params):
    r1, r2, r3 = r
    l = params
    return [r2, -1/(2*r1**2)+l**2/r1**3-1*1.5*l**2/r1**4, l/r1**2]

# МОЖНО ИССЛЕДОВАТЬ параметры: r0, params
r0 =[20, 0, 0] # В единицах гравитационного радиуса
N = 300

L1 = np.sqrt(r0[0]/2) # момент импульса для круговой орбиты
params = 1.3 * L1 # если взять больше, то орбита еще вытянется
time = 2 * np.pi * r0[0]**2 / L1 # период обращения по круговой орбите

t = np.linspace(0, 15*time, N)

sol = odeint(f, r0, t, args=(params,))

radius = sol[:,0]
angle = sol[:,2]

X = radius * np.cos(angle)
Y = radius * np.sin(angle)

fig = plt.figure()
plt.xlim(-30,30)
plt.ylim(-30,30)
plt.plot([0], [0], 'o', ms=10, color='k')

plt.plot(X, Y,'r',alpha=0.05)

def func_anim(i):
    plt.plot(X[:i], Y[:i],'g')

ani = animation.FuncAnimation(fig, func_anim, frames=np.arange(0,N,1),interval=100)

plt.axis('equal')
# plt.show()

ani.save('results/name.gif')
