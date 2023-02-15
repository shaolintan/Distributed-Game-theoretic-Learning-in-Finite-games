# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 13:23:18 2021

@author: fang
"""

import numpy as np
import networkx as nx
import random as rd
from math import exp,sqrt,ceil
from functools import partial
from matplotlib import pyplot as plt


def func1(G=nx.erdos_renyi_graph(100,0.03),iter_max=200,r=[],attri_dict={}):
    n = G.number_of_nodes()
    nodes = list(G.nodes())
    if len(r)!=n:
        for i in range(n):
            r.append(0.5)
    if len(attri_dict)!=n:
        for node in G.nodes():
            attri_dict[node] = [rd.choice([-1,1])]
        nx.set_node_attributes(G,attri_dict,'x')
    else:
        for i in range(n):
            G.nodes[nodes[i]]['x'] = [attri_dict[nodes[i]]]
    
    for iter_ in range(1,iter_max):
        x_next = []
        for i in range(n):
            if rd.random()<r[i]:
                tmp = sum([ G.nodes[nei]['x'][-1] for nei in nx.neighbors(G,nodes[i])])               
                if tmp>0:
                    x_next.append(1)
                elif tmp<0:
                    x_next.append(-1)
                else:
                    x_next.append(rd.choice([-1,1]))
            else:
                x_next.append(G.nodes[nodes[i]]['x'][-1])
        for i in range(n):
            G.nodes[nodes[i]]['x'].append(x_next[i])    
#    x = []
#    for i in range(iter_max):
#        x.append([G.nodes[node]['x'][i] for node in G.nodes()])
#    sum_x=[]
#    for i in range(iter_max):
#        a=0
#        for d in G.nodes():
#            for d2 in G.neighbors(d):
#                a+=G.nodes[d]['x'][i]*G.nodes[d2]['x'][i]
#        sum_x.append(a/nx.number_of_edges(G)/2)
    return G


def func2(G=nx.erdos_renyi_graph(100,0.05),iter_max=100,r=[],attri_dict={}):
    n = G.number_of_nodes()
    nodes = list(G.nodes())
    if len(r)!=n:
        for i in range(n):
            r.append(0.5)
    if len(attri_dict)!=n:
        for node in G.nodes():
            attri_dict[node] = [[rd.choice([-1,1])]*n]
        nx.set_node_attributes(G,attri_dict,'y')
    else:
        for node in attri_dict.keys():
            G.nodes[node]['y'] = [[attri_dict[node]]*n]
    tau = []
    for i in range(n):
        tmp = [0]*n
        tmp[i] = 1
        tau.append(tmp)
    
    for iter_ in range(1,iter_max):
        y_next = []#y值以y[-1]记录上一次的值，在y_next和yi上更新，最后再加入到y里面
        tau_tmp = tau.copy()#tau值以tau_tmp记录上一次的值，直接在tau更新
        for i in range(n):
            if rd.random()<r[i]:
                yi = []
                for j in range(n):
                    if i!=j:
                        neighbors = list(nx.neighbors(G,nodes[i]))
                        tau[i][j] = max([tau_tmp[nei][j] for nei in neighbors])
                        nei_tau_max = [nei for nei in neighbors if tau_tmp[nei][j]==tau[i][j]]
                        yi.append( G.nodes[rd.choice(nei_tau_max)]['y'][-1][j] )#########
                    else:
                        tau[i][i] = tau_tmp[i][i]+1
                        tmp = sum( G.nodes[nodes[i]]['y'][-1] )-G.nodes[nodes[i]]['y'][-1][i]
                        if tmp>0:
                            yi.append(1)
                        elif tmp<0:
                            yi.append(-1)
                        else:
                            yi.append(rd.choice([-1,1]))
            else:
                yi = G.nodes[nodes[i]]['y'][-1]
            y_next.append(yi)
        for i in range(n):
            G.nodes[nodes[i]]['y'].append(y_next[i])    
    y = []
    for i in range(iter_max):
        y.append([G.nodes[node]['y'][i] for node in G.nodes()])
    sum_y=[]
    for i in range(iter_max):
        a=0
        for j in range(n):
            for k in range(n):
                a+=G.nodes[nodes[j]]['y'][i][j]*G.nodes[nodes[k]]['y'][i][k]
        a=a-n
        sum_y.append(a/(n*(n-1)))
    return sum_y, y

#G=nx.barabasi_albert_graph(1000,2)

sum_z_1,z_1 = func2(iter_max=100,r=r,attri_dict=attri_dict)

#g5=nx.complete_graph(7)
#g6=nx.complete_graph(3)
#g7=nx.complete_graph(5)
#g8=nx.complete_graph(3)
#g9=nx.complete_graph(2)
#
#t=nx.disjoint_union_all([g5,g6,g7,g8,g9])
#t.add_edge(1,8)
#t.add_edge(1,12)
#t.add_edge(1,19)
#t.add_edge(8,12)
#t.add_edge(12,4)
#t.add_edge(12,5)
#t.add_edge(8,5)
#t.add_edge(13,16)
#
#g1=nx.complete_graph(9)
#g2=nx.complete_graph(3)
#g3=nx.complete_graph(4)
#g4=nx.complete_graph(4)
#
#g=nx.disjoint_union_all([g1,g2,g3,g4])
#
#g.add_edge(1,10)
#g.add_edge(13,10)
#g.add_edge(16,14)
#
#attri_dict = {0:1,1:1,2:1,3:1,4:1,5:1,6:1,7:-1,8:-1,9:-1,10:-1,11:-1,12:-1,13:-1,14:-1,15:1,16:1,17:1,18:1,19:1}
##g1 = func1(G=g1,iter_max=20,attri_dict=attri_dict)
##plt.figure()
##for d in g1.nodes():
##    plt.plot(range(20),g1.node[d]['x'])
#r=[]
#for i in range(nx.number_of_nodes(g)):
#    r.append(0.1)
#sum_z_1,z_1 = func2(G=t,iter_max=100,r=r,attri_dict=attri_dict)
#
#r=[]
#for i in range(nx.number_of_nodes(g)):
#    r.append(0.5)
#sum_z_2,z_2 = func2(G=t,iter_max=100,r=r,attri_dict=attri_dict)
#
##r=[]
##for i in range(nx.number_of_nodes(g)):
##    r.append(0.7)
##sum_y_3,y_3 = func2(G=g,iter_max=100,r=r,attri_dict=attri_dict)
#
#r=[]
#for i in range(nx.number_of_nodes(g)):
#    r.append(0.9)
#sum_z_3,z_3 = func2(G=t,iter_max=100,r=r,attri_dict=attri_dict)
#
#plt.figure()
#plt.plot(range(100),sum_z_1,'ro-')
#plt.plot(range(100),sum_z_2,'bs-')
#plt.plot(range(100),sum_z_3,'g<-')

#''' 1 '''
#iter_max = 200
##G = nx.erdos_renyi_graph(n,0.6)
#
#G = nx.Graph()
#G.add_nodes_from([i for i in range(7)])
#G.add_edges_from([(0,1),(0,2),(1,2),(2,3),(3,4),(4,5),(5,6),(3,6)])
#attri_dict = {0:1,1:1,2:1,3:-1,4:-1,5:-1,6:-1}
#
#sum_x,x = func1(G=G,iter_max=200,attri_dict=attri_dict)
#plt.figure()
#plt.plot(range(iter_max),sum_x)
#
#
#
#
#
#
#
#''' 2 '''
#iter_max = 100
##G = nx.erdos_renyi_graph(100,0.6)
#
#G = nx.Graph()
#G.add_nodes_from([i for i in range(7)])
#G.add_edges_from([(0,1),(0,2),(1,2),(2,3),(3,4),(4,5),(5,6),(3,6)])
#attri_dict = {0:1,1:1,2:1,3:-1,4:-1,5:-1,6:-1}
#
#sum_y, y = func2(G=G,iter_max=iter_max,attri_dict=attri_dict)
#n = G.number_of_nodes()
#n = min(n,10)
#sum_y = np.array(sum_y)
#for i in range(n):
#    plt.figure()
#    plt.plot(range(iter_max),sum_y[:,i])

















