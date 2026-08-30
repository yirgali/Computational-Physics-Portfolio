#collision with spring attached mass

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

#all springs are 1m long.
#this info is used in the "collision" event function
k=10 #N/m

#coming block from the left
m1=1 #kg
v10=10 #m/s
X1=1 #its initial coordinate in x-axis


#spring attached
m2=1
v20=5
X2=4

    
def springMotion_cm(t,dR): 
    x1,v1,x2,v2=dR
    u=(x2-x1)-1
    dx1dt=v1
    dv1dt=k/m1 * u
    
    dx2dt=v2
    dv2dt=-k/m2 * u
    
    return [dx1dt,dv1dt,dx2dt,dv2dt]

def springMotion_o(t,dr):
    X1,V1,X2,V2=dr
    u=(X2-X1)-1
    
    dX1dt=V1
    dV1dt= k/m1 *u
    
    dX2dt=V2
    dV2dt= -k/m2 *u
    return [dX1dt,dV1dt,dX2dt,dV2dt]

#x1 and x2 are the position vectors of the masses before the impact
def collision(t,R):
    x1,v1,x2,v2=R
    return x2-x1-1
    
collision.terminal=True

def motion(t,R):
    x1,v1,x2,v2=R
    dx1dt=v1
    dv1dt=0
    dx2dt=v2
    dv2dt=0
    return [dx1dt,dv1dt,dx2dt,dv2dt]

t0=0
tf=100

R0=[X1,v10,X2,v20]
before_impact=solve_ivp(motion,(t0,tf),R0,dense_output=True,events=collision)

t_current=before_impact.t[-1]

#updating the coordinates of the masses just before impact
X1_before=before_impact.y[0]
X2_before=before_impact.y[2]

x_cm=m1*X1_before/(m1+m2) + m2*X2_before/(m1+m2)

#common velocity after the impact
v_common=( (m1*v10)+(m2*v20) )/(m1+m2)

#define x10 and x20 initially.
#notice that the initial velocities are respect to the cm frame

x1_0=-(x_cm[-1] - X1_before[-1])
v1_0=v10- v_common

x2_0=-x_cm[-1] + X2_before[-1]
v2_0=v20-v_common

t_common=np.linspace(t_current,tf)

#solution respect to the cm frame
dR0=[x1_0,v1_0,x2_0,v2_0]
impact_cm=solve_ivp(springMotion_cm,(t_current,tf),dR0,dense_output=True)

x1=impact_cm.sol(t_common)[0]
x2=impact_cm.sol(t_common)[2]
v1=impact_cm.sol(t_common)[1]
v2=impact_cm.sol(t_common)[3]
    
#solutions respect to the O frame
dr0=[X1_before[-1],v10,X2_before[-1],v20]
impact_o=solve_ivp(springMotion_o,(t_current,tf),dr0,dense_output=True)

X1=impact_o.sol(t_common)[0]
X2=impact_o.sol(t_common)[2]
V1=impact_o.sol(t_common)[1]
V2=impact_o.sol(t_common)[3]

v_cm= (V1-v1)/2 + (V2-v2)/2
# actually, we do not need the extra term here. But in order to be sure V2 and V1 are valid,
# ı calculate the Vcm in a long way
valid=m1*x1+m2*x2

"""there are two conditions to justify our solutions
1. m1x1+m2x2=0
2. vcommon=vcm
which can be seen in variable explorer tab"""

if __name__=="__main__":
    #first image---------------------------
    
    plt.figure()
    plt.plot(t_common,x1,label="First mass")
    plt.plot(t_common,x2,label="Second mass")
    plt.legend()
    #---------------------------------------
    
    plt.figure()
    plt.plot(t_common,v1,label="First mass' velocity")
    plt.plot(t_common,v2,label="second mass' velocity")
    plt.legend()
    #--------------------------------------------------------
    
    plt.figure()
    plt.title("Velocity of CM")
    plt.axhline(v_common,color="red",label="Exact value")
    plt.plot(t_common,v_cm,color="blue",label="Numerical value")
    plt.legend()
    
    plt.show()