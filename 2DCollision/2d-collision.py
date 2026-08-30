#Vectoral collisions

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from itertools import combinations



class Balls:
    allBalls=[]
    fig=plt.figure(figsize=(12,12))
    grids=plt.GridSpec(9,5,hspace=0.9)#for trajectories-momentum-
    trajectory=fig.add_subplot(grids[:6,:])
    momentum=fig.add_subplot(grids[6:,:])
    
    trajectory.set_xlabel("x")
    trajectory.set_ylabel("y")
    momentum.set_xlabel("t")
    momentum.set_ylabel("Total momentum")
    
    t0=0 
    tf=25
    N=200
    t=np.linspace(t0,tf,N)
    p_total=[]
    t_for_p=[] #for the momentum graph
    #force,r and v_initial is the vector array
    def __init__(self,mass,r,v_initial,force):
        self.m=mass
        self.v=[v_initial[0],v_initial[1]]
        self.F=np.array(force)
        self.p=[]
        self.r=np.array(r) #r is the vector for any moment
        self.pos=[]
        self.radius=0.5 
        Balls.allBalls.append(self)
        
    @classmethod
    def calMomentum(cls,current_R):
        #calculating the total momentum at a moment
        p=0
        for i,balls in enumerate(cls.allBalls):
            p+=balls.m*current_R[4*i+2:4*i+4]
        cls.p_total.append(np.linalg.norm(p))
    
    @classmethod
    def Fx(cls,t,R): #R=[rx1,ry1,vx1,vy1...]
        dRdt=np.zeros_like(R)
        
        for i,ball in enumerate(Balls.allBalls):
            di=4*i
            drdt=R[di+2:di+4]
            dvdt=ball.F/ball.m
            dRdt[di:di+2]=drdt
            dRdt[di+2:di+4]=dvdt
        return dRdt
    
    @classmethod
    def motion(cls):
        t_current=cls.t0
        t_after=cls.tf
        events=[]
        for ball1,ball2 in combinations(cls.allBalls,2):
            events.append(cls.make_collision(ball1, ball2))
            
        while t_current<t_after:
            
            R0=[]
            for ball in Balls.allBalls:
                R0.extend([ball.r[0],ball.r[1],ball.v[0],ball.v[1]])
            solution=solve_ivp(cls.Fx,(t_current,t_after),R0,dense_output=True,events=events)
            
            for step in range(len(solution.t)):
                cls.t_for_p.append(solution.t[step])
                cls.calMomentum(solution.y[:,step])
            for i,ball in enumerate(cls.allBalls):
                ball.pos.extend(solution.y[4*i:4*i+2,:].flatten(order="F"))
                
            if solution.status==1:
                t_current=solution.t[-1]
                impact_moment=solution.y[:,-1]
                cls.impact(impact_moment) #update velocities 
            else:
                break
            
    @classmethod
    def impact(cls,impact_moment):
        for ball1,ball2 in combinations(cls.allBalls,2):
            i1=cls.allBalls.index(ball1)
            i2=cls.allBalls.index(ball2)
            v1_0=impact_moment[4*i1+2:4*i1+4].copy()
            v2_0=impact_moment[4*i2+2:4*i2+4].copy()
            ball1.v = 2*ball2.m*v2_0/(ball1.m+ball2.m) + (ball1.m-ball2.m)*v1_0/(ball1.m+ball2.m)
            ball2.v= (ball2.m-ball1.m)*v2_0/(ball1.m+ball2.m) + 2*ball1.m*v1_0/(ball1.m+ball2.m)
            
            ball1.r= impact_moment[4*i1:4*i1+2].copy()+ball1.v*0.01
            ball2.r= impact_moment[4*i2:4*i2+2].copy()+ball2.v*0.01
                    
    @classmethod
    def make_collision(cls,b1,b2):
        def event(t,R):
            R=np.array(R)
            i_1=cls.allBalls.index(b1)
            i_2=cls.allBalls.index(b2)
            dist=np.linalg.norm(R[4*i_1:4*i_1+2]-R[4*i_2:4*i_2+2])-(b1.radius+b2.radius)
            return dist
        event.terminal=True
        return event
    
    def trajectory_graph(self):
        #pos=[x(t0),y(t0),x(t1),y(t1),...]
        self.trajectory.plot(self.pos[::2],self.pos[1::2],label=f"Ball {Balls.allBalls.index(self)}")
        self.trajectory.grid(True,linestyle="--",alpha=0.6)
        self.trajectory.legend()
        
    @classmethod
    def momentum_graph(cls):
        cls.momentum.plot(cls.t_for_p,cls.p_total)
        
    

ball1=Balls(mass=2, r=[1,2], v_initial=[1,2], force=[0,0])
ball2=Balls(mass=3, r=[-1,-2], v_initial=[-2,2], force=[0,0])

ball1.motion()
ball1.trajectory_graph()
ball2.trajectory_graph()
Balls.momentum_graph()

plt.show()


###correct the math part