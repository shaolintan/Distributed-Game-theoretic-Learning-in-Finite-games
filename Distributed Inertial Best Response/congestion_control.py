# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 13:13:04 2021

@author: sean
"""

import numpy as np
import networkx as nx
import random as rd
#from math import exp,sqrt,ceil
#from functools import partial
from matplotlib import pyplot as plt
#from decimal import Decimal


def traffic_network():
    l=[1,2,3,4,5]
    a_1=[1,4]
    a_2=[2,5]
    a_3=[1,3,5]
    a_4=[2,3,4]
    s=[a_1,a_2,a_3,a_4]
    return l,s

def traffic_network_2():
    l=[1,2,3,4,5,6,7,8]
    a_1=[1,5]
    a_2=[1,3,6,8]
    a_3=[2,4,6,8]
    a_4=[2,7,8]
    s=[a_1,a_2,a_3,a_4]
    return l,s

def vehicle_number_1(y,s,l):
    t={}
    n={}
    for i in l:
        t[i]=0
        n[i]=0
    for j in range(len(y)):
        for k in s[y[j]]:
            t[k]+=0.01+0.02*j
            n[k]+=1
    cong=0
    for k in l:
        if k==1 or k==5:
            cong+=n[k]*t[k]/100
        elif k==2 or k==4:
            cong+=n[k]        
    return t,n,cong

def vehicle_number_2(y,s,l):
    t={}
    for i in l:
        t[i]=0
    for j in y:
        for k in s[j]:
            t[k]+=1
    cong=0
    for k in l:
        if k in [1,2,3,4,6,8]:
            cong+=t[k]*(t[k]**2+t[k]+1)
        elif k==5:
            cong+=3*t[k]*(t[k]**2+t[k]+1)  
        elif k==7:
            cong+=2*t[k]*(t[k]**2+t[k]+1)  
    return t,cong

def best_response_2(y,s,l,binary):
    t1,t2=vehicle_number_2(y,s,l)
    u={}
    for j in range(4):
        u[j]=0
        for k in s[j]:
            if k in [1,2,3,4,6,8]:
                if binary==1:
                    u[j]-=(t1[k]+1)**2+t1[k]+2
                elif binary==2:
                    u[j]-=(t1[k]+1)**2+t1[k]+2+t1[k]*(2*t1[k]+2)  
            elif k==5:
                if binary==1:
                    u[j]-=3*((t1[k]+1)**2+t1[k]+2)
                elif binary==2:
                    u[j]-=3*((t1[k]+1)**2+t1[k]+2+t1[k]*(2*t1[k]+2))
            elif k==7:
                if binary==1:
                    u[j]-=2*((t1[k]+1)**2+t1[k]+2)
                elif binary==2:
                    u[j]-=2*((t1[k]+1)**2+t1[k]+2+t1[k]*(2*t1[k]+2))                    
    best = [i for i in range(4) if u[i]==max(u.values())]
    return best

def best_response_1(y,identy,s,l,binary):
    t1,t2,t3=vehicle_number_1(y,s,l)
    u={}
    for j in range(4):
        u[j]=0
        for k in s[j]:
            if k==1 or k==5:
                if binary==1:
                    u[j]-=(t1[k]+0.01+0.02*identy)/100
                elif binary==2:
                    u[j]-=(t1[k]+(t2[k]+1)*(0.01+0.02*identy))/100 
            elif k==2 or k==4:
                u[j]-=1
    best = [i for i in range(4) if u[i]==max(u.values())]
    return best

def evolution(G,s,l,binary,iter_max,r_ini):
    n = G.number_of_nodes()
    nodes = list(G.nodes())
    r=[]
    for i in range(n):
        r.append(r_ini)
#    attri_dict={}
    for i in range(n):
        G.nodes[nodes[i]]['y']=[[0]*n]
        for j in range(n):
            G.nodes[nodes[i]]['y'][-1][j]=rd.choice([0,1,2,3])
#        G.nodes[nodes[i]]['y']=[[rd.choice([0,1,2,3])]*n]
#        if i<50:
#        G.nodes[nodes[i]]['y']=[[0]*50+[1]*50]
#        attri_dict[node] = 
#    nx.set_node_attributes(G,attri_dict,'y')
    tau = []
    for i in range(n):
        tmp = [0]*n
        tmp[i] = 1
        tau.append(tmp)   
    for iter_ in range(1,iter_max):
        y_next = []#y值以y[-1]记录上一次的值，在y_next和yi上更新，最后再加入到y里面
        tau_tmp = tau.copy()#tau值以tau_tmp记录上一次的值，直接在tau更新
        for i in range(n):        
            yi = []
            for j in range(n):
                if i!=j:
                    neighbors = list(nx.neighbors(G,nodes[i]))
                    tau[i][j] = max([tau_tmp[nei][j] for nei in neighbors])
                    nei_tau_max = [nei for nei in neighbors if tau_tmp[nei][j]==tau[i][j]]
                    yi.append(G.nodes[rd.choice(nei_tau_max)]['y'][-1][j])
                else:
                    if rd.random()<r[i]:
                        tau[i][i] = tau_tmp[i][i]+1
                        x=G.nodes[nodes[i]]['y'][-1].copy()
                        x.remove(x[i])
                        best = best_response_1(x,i,s,l,binary)
                        if G.nodes[i]['y'][-1][i] in best:
                            yi.append(G.nodes[i]['y'][-1][i])
                        else:
                            yi.append(rd.choice(best))
                    else:
                        tau[i][i] = tau_tmp[i][i]
                        yi.append(G.nodes[i]['y'][-1][i])
            y_next.append(yi)
        for i in range(n):
            G.nodes[nodes[i]]['y'].append(y_next[i])    
    y = []
    x=[]
    for i in range(iter_max):
        y.append([G.nodes[node]['y'][i] for node in G.nodes()])
        x.append([G.nodes[node]['y'][i][node] for node in nodes])
    return x, y


def evolution_2(G,s,l,binary,iter_max,r_ini):
    n = G.number_of_nodes()
    nodes = list(G.nodes())
    r=[]
    for i in range(n):
        r.append(r_ini)
#    attri_dict={}
    for i in range(n):
        G.nodes[nodes[i]]['y']=[[0]*n]
#        G.nodes[nodes[i]]['y']=[[rd.choice([0,1,2,3])]*n]
#        if i<50:
#        G.nodes[nodes[i]]['y']=[[0]*50+[1]*50]
#        attri_dict[node] = 
#    nx.set_node_attributes(G,attri_dict,'y')
    tau = []
    for i in range(n):
        tmp = [0]*n
        tmp[i] = 1
        tau.append(tmp)    
    for iter_ in range(1,iter_max):
        y_next = []#y值以y[-1]记录上一次的值，在y_next和yi上更新，最后再加入到y里面
        tau_tmp = tau.copy()#tau值以tau_tmp记录上一次的值，直接在tau更新
        for i in range(n):        
            yi = []
            for j in range(n):
                if i!=j:
                    neighbors = list(nx.neighbors(G,nodes[i]))
                    tau[i][j] = max([tau_tmp[nei][j] for nei in neighbors])
                    nei_tau_max = [nei for nei in neighbors if tau_tmp[nei][j]==tau[i][j]]
                    yi.append(G.nodes[rd.choice(nei_tau_max)]['y'][-1][j])
                else:
                    if rd.random()<r[i]:
                        tau[i][i] = tau_tmp[i][i]+1
                        x=G.nodes[nodes[i]]['y'][-1].copy()
                        x.remove(x[i])
                        best = best_response_2(x,s,l,binary)
                        if G.nodes[i]['y'][-1][i] in best:
                            yi.append(G.nodes[i]['y'][-1][i])
                        else:
                            yi.append(rd.choice(best))
                    else:
                        tau[i][i] = tau_tmp[i][i]
                        yi.append(G.nodes[i]['y'][-1][i])
            y_next.append(yi)
        for i in range(n):
            G.nodes[nodes[i]]['y'].append(y_next[i])    
    y = []
    x=[]
    for i in range(iter_max):
        y.append([G.nodes[node]['y'][i] for node in G.nodes()])
        x.append([G.nodes[node]['y'][i][node] for node in nodes])
    return x, y

def plot_evol(x,s,l):
    t={}
    cong=[]
    for i in l:
        t[i]=[]
    for j in range(len(x)):
        tmp1,tmp2,tmp3=vehicle_number_1(x[j],s,l)
        for i in l:
            t[i].append(tmp1[i])
        cong.append(tmp3)
    plt.figure()   
    for i in l:       
        plt.plot(range(len(x)),t[i])
    plt.figure()
    plt.plot(range(len(x)),cong)
    a=np.array(x)
    plt.figure()
    for i in range(99):
        plt.plot(range(len(x)),a[:,i])
    return


def plot_evol_2(x,s,l):
    t={}
    cong=[]
    for i in l:
        t[i]=[]
    for j in range(len(x)):
        tmp1,tmp2=vehicle_number_2(x[j],s,l)
        for i in l:
            t[i].append(tmp1[i])
        cong.append(tmp2)
    plt.figure()   
    for i in l:       
        plt.plot(range(len(x)),t[i])
    plt.figure()
    plt.plot(range(len(x)),cong)
    return
        
               
a,b=traffic_network()
G=nx.barabasi_albert_graph(99,2)
#G=nx.erdos_renyi_graph(100,0.05)


#y=[0]*700+[1]*100+[2]*100+[3]*100
#t=vehicle_number(y,b,a)
#best,u=best_response_1(y,b,a)
x,y=evolution(G,b,a,1,50,0.2)
#plt.figure(1)
plot_evol(x,b,a)
x1,y1=evolution(G,b,a,2,150,0.5)
#plt.figure(2)
plot_evol(x1,b,a)

