# SPRING COLLISION
Imagine a block with a spring attached and it is going in the +x direction, say m2. What happens if a mass, say m1, moving to +x direction, behind the block with mass m2, collide with the spring system?
## Condition and The Impact Moment
In order to observe a collision, the velocity of the mass m1 must be greater then the velocity of mass m2 assuming that there is no external force so that their velocities are constant before a collision. The below code in *springCollision.py* enables us to track of the collision event: 
```python
def collision(t,R):
    x1,v1,x2,v2=R
    return x2-x1-1
    
collision.terminal=True
```
with the help of the *solve_ivp* function from SciPy library:
````python
R0=[X1,v10,X2,v20]
before_impact=solve_ivp(motion,(t0,tf),R0,dense_output=True,events=collision)

t_current=before_impact.t[-1]

#updating the coordinates of the masses just before impact
X1_before=before_impact.y[0]
X2_before=before_impact.y[2]
````
R0 is the initial values for solve_ivp to solve the system equations where *v10* with *X1* and *v20* with *X2* are initial velocities and positions of mass m1 and m2, respectively. After the *before_impact* solver, we update the current time so that we can continue in collision including the spring force.
We need to solve the system with the spring force in both analytically and numerically to see whether they elapse.
### ANALYTICAL SOLUTION
***
To facilitate the process, we will solve in the center of mass(CM) frame first. Thus, we can easily transform the solution into a lab(O) coordinate system. 
We treat the CM as our origin. So the position vector of the masses in CM frame is $\vec{x_1}$  and $\vec{x_2}$ for mass $m_1$ and $m_2$ respectively. The denoted variables to these in the *springCollision.py* is **x1** and **x2**, respectively. Note that $\vec{x_1} < 0 $ initially because of our choice of the coordinate system(CM frame). As the spring is regarded as massless, the force on its each part must be the same, meaning that the force exerting on each mass is in same magnitude! In order for this to occur, we need to examine the total compression of the string since the both masses are not independent from each other.
We choose $+x$ is in the right direction:
1. Let us denote the compression of the spring as $u =  |\vec{x_2} + x_1| -L = (x_2-x_1)-L$ in any time as $x_1$ is in the $-x$ direction.
2. Thus, the force equations become $$m_2\ddot{x_2}= -ku$$  and $$m_1\ddot{x_1}= ku$$ 
because of our choice of coordinate system.
To justify our sign in differential equations, assume $x_2-x_1>L \rightarrow u>0$ so the spring is stretched. Hence, the spring must pull the mass $m_2$ to the $-x$ whereas it pulls the mass $m_1$ to the $+x$ as the differential equations above shows.
3. $\ddot{u} = \ddot{x_2} - \ddot{x_1}$ which becomes by isolating the each term in the right side,
    * $\ddot{u} = -\frac{k}{m_2}u -\frac{k}{m_1}u=-k(\frac{1}{m_1} + \frac{1}{m_2})u$
    * Denoting $\omega=\sqrt{k(\frac{1}{m_1} + \frac{1}{m_2})}$,
    * $u(t)=A\sin{\omega t}+B\cos{\omega t}$. We need to solve this to find the coefficients *A* and *B*.
        * $u(t=0)=0 \rightarrow B=0$ since the compression/stretch of the spring is 0 just before(t=0) the impact. Thus $u(t)= A\sin{wt}$
        * $\dot{u}=Aw\cos{wt} = \dot{x_2}(t)-\dot{x_1}(t)$
            * at t=0, $\dot{u}(0)=v_{20}-v_{10}$ where $v_{20}$ and $v_{10}$ are initial velocities of masses $m_2$ and $m_1$ just before the impact, respectively. To see the why, let $X_1$ and $X_2$ be the position vectors of the mass $m_1$ and $m_2$ in the lab frame, as denoted in the code snippet in *springCollision.py*
        * One can realize that $x_{cm} = X_1-x_1=X_2-x_2$ by drawing the system with coordinates. Thus, $\dot{x_2}(t=0)-\dot{x_1}(t=0)=\dot{X_2}(0)-\dot{X_1}(0)=v_{20}-v_{10}$
        * Thus $\dot{u}(0)=v_{20}-v_{10}= A\omega \cos{0} \Rightarrow A=\frac{v_{20}-v_{10}}{\omega}$
4. Consequently, $u(t)=\frac{v_{20}-v_{10}}{\omega}\sin{\omega t}$
5. By substituing this into $x_1=\frac{k}{m_1}\frac{v_{20}-v_{10}}{\omega^3}\sin{\omega t} + x_{10}$ and $x_2=-\frac{k}{m_2}\frac{v_{20}-v_{10}}{\omega^3}\sin{\omega t} + x_{20}$ where both $x_{10}$ and $x_{20}$ are initial positions of masses in CM frame due to the integration constant.
### NUMERIC SOLUTION
***
By using the code below in *springCollision.py*, we so