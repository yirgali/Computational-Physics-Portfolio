import sys
sys.path.append(r"C:\Users\yusuf\Desktop\phys-projects\mass-collisions\springCollision")

import springCollision
import numpy as np
from scipy.optimize import curve_fit

x1=springCollision.x1
x2=springCollision.x2
v10=springCollision.v10
v20=springCollision.v20

m2=springCollision.m2
m1=springCollision.m1
k=springCollision.k

w=np.sqrt(k*(1/m1 + 1/m2))

def x2_guess(t,A,w,c2,d2):
    return A*np.sin(w*t) + c2*t + d2

w0=w
A0=-k/m2 * (v10-v20)/w**3
c20=0
d20=x2[0]

X20=[A0,w0,c20,d20]


def x1_guess(t,B,w,c1,d1):
    return B*np.sin(w*t) + c1*t + d1

B0= k/m1 * (v10-v20)/w**3
c10=0
d10=x1[0]

X10=[B0,w0,c10,d10]

#☺shifting the t value so that we do not deal with phi shifting in sine wave
t=springCollision.t_common-springCollision.t_current

popt1,pcov1=curve_fit(x1_guess, t, x1, X10)
y1=x1_guess(t,*popt1)

popt2,pcov2=curve_fit(x2_guess, t, x2, X20)
y2=x2_guess(t,*popt2)

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

fig=plt.figure(figsize=(6,6))
grid=gridspec.GridSpec(4,8)

graph_x1=fig.add_subplot(grid[:,:4])

graph_x2=fig.add_subplot(grid[:,4:],sharey=graph_x1)

y1_org=lambda t:k/m1 * (v10-v20)/(w**3) * np.sin(w*t) + x1[0]
graph_x1.plot(t,y1,linestyle="-",label="Numerical Value")
graph_x1.plot(t,y1_org(t),linestyle="--",label="Exact value")
graph_x1.set_title("Mass 1 in CM frame")
graph_x1.legend()

y2_org=lambda t:-k/m2 * (v10-v20)/(w**3) * np.sin(w*t) + x2[0]
graph_x2.plot(t,y2,linestyle="-",label="Numerical value")
graph_x2.plot(t,y2_org(t),linestyle="--",label="Exact")
graph_x2.set_title("Mass 2 in CM frame")
graph_x2.legend()