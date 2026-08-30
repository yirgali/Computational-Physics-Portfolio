#collision system 1D
import numpy as np
import matplotlib.pyplot as plt


N=1000

class Ball:
    all_balls=[]
    dt=0.01
    t=np.linspace(0,N*dt,N)
    fig=plt.figure(figsize=(12,12))
    grid=plt.GridSpec(9,4,hspace=0.9,wspace=0.4)
    trajec_ax=fig.add_subplot(grid[:4,:])
    momentum_ax=fig.add_subplot(grid[4:7,:])
    kinetic_ax=fig.add_subplot(grid[7:,:])

    trajec_ax.set_xlabel("t")
    momentum_ax.set_xlabel("t")
    momentum_ax.set_ylabel("Momentum")
    kinetic_ax.set_xlabel("t")
    kinetic_ax.set_ylabel("Kinetic energy")
    
    def __init__(self,m,vx,x):
        Ball.all_balls.append(self)
        self.v=vx
        self.r=x
        self.ypos=np.full(N,Ball.all_balls.index(self))
        self.xpos=[]
        self.m=m
        self.R=1
        self.vf=0

    def collision(self):
        for other in Ball.all_balls:
            if other==self:
                continue
            else:
                dist=np.linalg.norm(self.r-other.r)
                relative_vel=self.v-other.v
                relative_pos=self.r-other.r
                if dist <= (self.R + other.R) and (relative_pos*relative_vel<0):
                    vxf= ((self.m-other.m)*self.v + 2*other.m*other.v) / (self.m+other.m)
                    self.vf=vxf
                    break
                else:
                    self.vf=self.v


    def move(self):
        self.xpos.append(self.r)
        self.r += self.dt*self.v

        
    def graph(self):
        self.trajec_ax.plot(Ball.t,self.xpos,label=f"Ball {Ball.all_balls.index(self)+1}")
        self.trajec_ax.grid(True, linestyle='--', alpha=0.6)
        self.trajec_ax.legend()

        
    
ball1=Ball(1,-3,5)     
ball2=Ball(1,4,0)
ball3=Ball(20,2,18)

t=np.linspace(0,N*Ball.dt,N)
momentum=[]
kinetic=[]

for i in range(N):
    ptotal=sum(b.m*b.v for b in Ball.all_balls)
    momentum.append(ptotal)

    ke=sum(0.5*b.m*(b.v**2) for b in Ball.all_balls)
    kinetic.append(ke)
    for b in Ball.all_balls:
        b.collision()
        
    for b in Ball.all_balls:
        b.move()
        b.v=b.vf


ball1.graph()
ball2.graph()
ball3.graph()

Ball.momentum_ax.plot(t,momentum)
Ball.kinetic_ax.plot(t,kinetic)

plt.show()
    