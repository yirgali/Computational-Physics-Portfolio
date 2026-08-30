
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 13:49:24 2026

@author: İRGALİ
"""

#Maxwell-Boltzman Distribution

import numpy as np
from collisionMechanic import collision,L
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import functools
from matplotlib.animation import FuncAnimation

T=300 #K
k_b=1.38e-23 #J/K

R=8.314
M=1.67e-27 #kg
N=300



class Particle:
    E_kTotal=k_b*T*N
    
    
    mass=[]
    def __init__(self,m):
        self.m=m
        Particle.mass.append(self.m)
        
        #to choose the components randomly, we define a random number between -1 and 1 as follows:
        theta=np.random.uniform(0,2*np.pi)
        self.lambda_x=np.cos(theta)
        self.lambda_y=np.sin(theta)
        
        #denoting the random components
        self.v=0 #for now
        self.x=np.random.rand()*L
        self.y=np.random.rand()*L
        self.r=np.array([self.x,self.y])
        
    
        
        
#to create N particle
particles=[]
for i in range(N):
    atom=Particle(M)
    particles.append(atom)
    
def update_vel(particles):
    #initial velocity array
    vi=np.zeros(len(particles))
    E_k=0
    vp=(k_b*T/M)**0.5
    #%99.999 of the particles
    vmax=3.5*vp
    for i in particles:
        
        i.v=np.array([i.lambda_x,i.lambda_y]) * np.random.rand()*vmax
        E_k+=0.5*i.m*np.linalg.norm(i.v)**2
    
    #correction to fit the system to the total E
    e=Particle.E_kTotal/E_k 
    for k,i in enumerate(particles):
        i.v *= np.sqrt(e)
        vi[k]=np.linalg.norm(i.v)
    return vi,vmax
        
vi,vmax=update_vel(particles)

tf=250
dt=5.0e-4

#we get the final velocities and the kinetic energy from the collision process
vf,ke=collision(particles, dt, tf,M)


def F(u,M):
    return M/(k_b*T) * u * np.exp(-M*u**2 / (2*k_b*T))



fig=plt.figure(figsize=(6,6))
grid=plt.GridSpec(7, 6,wspace=5)
main_ax=fig.add_subplot(grid[:4,:])
energy_ax=fig.add_subplot(grid[5:,:])

main_ax.set_xlabel("Velocities(m/s)")
main_ax.set_ylabel("Probability Density")
main_ax.set_title("Maxwell-Boltzman Distribution")
main_ax.yaxis.set_major_formatter(plt.NullFormatter())

#theoretical curve 
n=100
u=np.linspace(0,np.max(vf),n)
y=F(u,M)
main_ax.plot(u,y,color="black",label="Theoretical Curve")
vrms_theo=(2*k_b*T/M)**0.5 #root mean squared
y_rms=F(vrms_theo, M)
main_ax.scatter(vrms_theo,y_rms,color="red",label="$v_{rms}$")



#hist pre-animation

bins=50
_,_,barContainers=main_ax.hist(vf[0:N],bins=bins,density=True,edgecolor="black",alpha=0.4)

stride=1
frameNum=int((len(vf)/N)/stride)
count=np.zeros((frameNum,bins))
for i in range(frameNum):
    actualStep=stride*i
    c,_=np.histogram(vf[actualStep:actualStep+N],bins=bins,density=True)
    count[i,:]=c
    
#experimental curve pre-animation
xval=np.linspace(0, np.max(vf),N)
yval=np.zeros((frameNum,N))
expData=(xval,yval)
expCurve=main_ax.plot([],[],color="red",label="Experimental")[0]
rms_exp=np.sqrt(2*ke/M)[::stride]
sizeVal=len(rms_exp)//stride
rms_exp=rms_exp.reshape(sizeVal,1)
yrms_exp=F(rms_exp,M)
rms_scatter=main_ax.scatter([],[],color="red")

sizeVal=len(rms_exp)/stride
offset=np.hstack((rms_exp,yrms_exp))

for i in range(frameNum):
    step=stride*i
    currentSpeed=vf[step:step+N]
    
    jitter=np.random.normal(0,1e-6,N)
    kde=gaussian_kde(currentSpeed+jitter)
    yval[i,:]=kde(xval)

#animation function for the histogram and the experimental curve
def animateHist(frame,barContainers,count,expData,expCurve):
    #for hist animation
    for c,rect in zip(count[frame],barContainers.patches):
        rect.set_height(c)
    
    #to animate the experimental Curve
    expCurve.set_data(expData[0],expData[1][frame])
    rms_scatter.set_offsets(offset[frame])
    return [*barContainers.patches, expCurve,rms_scatter]

anim=functools.partial(animateHist, barContainers=barContainers,count=count,
                       expData=expData,expCurve=expCurve)
animation_hist=FuncAnimation(fig, anim,frames=frameNum, blit=True)
main_ax.legend()

#for the kinetic energy plot
energy_ax.plot(ke,label="Experimental Kinetic Energy")
energy_ax.set_yscale("log")
energy_ax.set_ylabel("Energy(log)")
energy_ax.set_ylim(bottom=1e-20,top=1e-17)
energy_ax.xaxis.set_major_formatter(plt.NullFormatter())
energy_ax.yaxis.set_major_formatter(plt.NullFormatter())
energy_ax.legend()

path="C:\\Users\\yusuf\\Desktop\\phys-projects\\Maxwell-Boltzman-Distribution\\"
file=path+"simulation.mp4"
videoLen=20 #seconds
fps=frameNum//videoLen
animation_hist.save(filename=file,writer="ffmpeg",fps=fps)

plt.show()