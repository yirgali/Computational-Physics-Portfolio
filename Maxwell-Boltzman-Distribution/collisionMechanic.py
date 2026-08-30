# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 16:02:12 2026

@author: İRGALİ
"""


import numpy as np


L=5
#R is the radius of one particle
R=0.08
shot=100 #we record every 'shot' steps.
def collision(particles,dt,tf,M):
    steps=int(tf/dt)
    
    xpos=np.array([p.r[-2] for p in particles])
    ypos=np.array([p.r[-1] for p in particles])
    vx=np.array([p.v[-2] for p in particles])
    vy=np.array([p.v[-1] for p in particles])
    N=len(particles)
    
    #to use them conveniently
    vx=vx.reshape(N,1)
    vy=vy.reshape(N,1)
    xpos=xpos.reshape(N,1)
    ypos=ypos.reshape(N,1)
    
    
    
    v=np.zeros(steps//shot * N)
    #for wall updating
    totalCol=0
    row,col=np.indices((N,N))
    ke=np.zeros(steps//shot)
    for step in range(steps):

        
        #instead of collecting all data, we use some of them for optimization
        if step%shot==0:
            ke[step//shot]=np.sum(M/2 * (vx**2+vy**2))
            i=(step//shot)*N
            v[i:i+N]=np.sqrt(vx**2+vy**2).flatten()
            
        #updating the positions
        xpos += vx*dt
        ypos += vy*dt
        
        #checking for the walls
        # after each collision with the wall, the loop itself updates the positions
        #thus we do not update manually
        hitLeft=xpos-R<0
        vx[hitLeft] *= -1
        
        hitRight=xpos+R>L
        vx[hitRight] *= -1
        
        hitUp=ypos+R>L
        vy[hitUp] *= -1
        
        hitBottom=ypos-R<0
        vy[hitBottom] *= -1
        
        
        #to update their velocity for particle collisions
        while True:
            totalCol+=1
            dx=np.transpose(xpos)-xpos
            dy=np.transpose(ypos)-ypos
            dr=np.sqrt(dx**2+dy**2)
            
            dvx=np.transpose(vx)-vx
            dvy=np.transpose(vy)-vy
            
            vDOTr=dx*dvx+dy*dvy
            
            pCol= (dr <= 2*R) & (row<col) & (vDOTr<0)
            #the second condition is for self destruction    
            #third condition is to determine whether we examine for particles getting closer or further
            #results return the index of the satisfied elements in tuple by row and column index accordingly
            
            if not pCol.any():break
            
        
            i,j=np.argwhere(pCol)[0]

            v1=np.hstack((vx[[i]], vy[[i]]))
            r1=np.hstack((xpos[[i]], ypos[[i]]))
            
            
            v2=np.hstack((vx[[j]], vy[[j]]))
            r2=np.hstack((xpos[[j]], ypos[[j]]))
            
            rij=(r1-r2)/np.linalg.norm(r1-r2,axis=1,keepdims=True)
        
            
            dot=np.sum((v1-v2)*rij,axis=1,keepdims=True)
            
            
            P=-2*M*M/(2*M) * dot*rij
                
            dv1 = P/M
            dv2 = -P/M
            
            
        
            vx[i] += dv1[:,0]
            vy[i] += dv1[:,1]
            
            vx[j] += dv2[:,0]
            vy[j] += dv2[:,1]

    print("Total collision is",totalCol)
    return v,ke
    