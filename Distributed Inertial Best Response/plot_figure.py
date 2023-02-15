# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 10:22:45 2021

@author: sean
"""

import numpy as np
from matplotlib import pyplot as plt

#y1=np.load('y_1.npy')
#y2=np.load('y_2.npy')
#y3=np.load('y_3.npy')
#z1=np.load('z_1.npy')
#z2=np.load('z_2.npy')
#z3=np.load('z_3.npy')
#
#plt.figure()
#
#plt.subplot(2,1,1)
#plt.plot(range(100),y1,'ro-',label=r"$r_i=0.9$")
#plt.plot(range(100),y2,'bs-',label=r"$r_i=0.5$")
#plt.plot(range(100),y3,'g<-',label=r"$r_i=0.1$")
#plt.legend(loc=4)
#plt.ylabel('Coordination level',family='Arial',fontweight="heavy",fontsize="12")
#plt.text(1,0.9,'(a)',family='Arial',fontweight="heavy",fontsize="12")
#
#plt.subplot(2,1,2)
#plt.plot(range(100),z1,'ro-',label=r"$r_i=0.9$")
#plt.plot(range(100),z2,'bs-',label=r"$r_i=0.5$")
#plt.plot(range(100),z3,'g<-',label=r"$r_i=0.1$")
#plt.legend(loc=4)
#plt.xlabel('Time',family='Arial',fontweight="heavy",fontsize="12")
#plt.ylabel('Coordination level',family='Arial',fontweight="heavy",fontsize="12")
#plt.text(1,0.9,'(b)',family='Arial',fontweight="heavy",fontsize="12")

x=np.load('cong_x.npy')
y=np.load('cong_y.npy')

plt.figure()

ax=plt.subplot(2,1,1)
for i in range(99):
    plt.plot(range(len(x)),x[:,i])
ax.set_yticks((0,1,2,3))
labels = ax.set_yticklabels((r"$a_1$", r"$a_2$", r"$a_3$", r"$a_4$"))
#plt.legend(loc=4)
plt.ylabel('Routing ID',family='Arial',fontweight="heavy",fontsize="12")
plt.text(-2,2.7,'(a)',family='Arial',fontweight="heavy",fontsize="12")

ax1=plt.subplot(2,1,2)
for i in range(99):
    plt.plot(range(len(y)),y[:,i])
ax1.set_yticks((0,1,2,3))
labels = ax1.set_yticklabels((r"$a_1$", r"$a_2$", r"$a_3$", r"$a_4$"))
#plt.legend(loc=4)
plt.xlabel('Time',family='Arial',fontweight="heavy",fontsize="12")
plt.ylabel('Routing ID',family='Arial',fontweight="heavy",fontsize="12")
plt.text(-6,2.7,'(b)',family='Arial',fontweight="heavy",fontsize="12")
