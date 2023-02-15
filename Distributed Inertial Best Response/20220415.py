# -*- coding: utf-8 -*-


import numpy as np
import random
import networkx as nx
import matplotlib.pyplot as plt


def graph2list(g):
    nodes = list(g.nodes())
    nei_list = []
    if nx.is_directed(g):
        func_nei = g.predecessors
    else:
        func_nei = g.neighbors
    for u in g.nodes():
        nei_list.append([nodes.index(v) for v in func_nei(u)])
    return nei_list


def func1(g,r=0.5,s=['a','b','c'],n_loops=100,using_seed=False):
    if isinstance(g,list):
        nei_list1 = graph2list(g[0])
        nei_list2 = graph2list(g[1])
        n = g[0].number_of_nodes()
    else:
        nei_list = graph2list(g)
        n = g.number_of_nodes()
    T = []
    for i_l in range(n_loops):
        ### 随机数种子 ###
        if using_seed:
            seed = i_l
        else:
            seed = None
        random.seed(seed)
        
        ### 初始化 ###
        y = []
        for i in range(n):
            tmp = []
            for j in range(n):
                tmp.append(random.choice(s))
            y.append(tmp)
        y = np.array(y)
        tao = np.eye(n)
        
        ### 迭代 ###
        t = 1
        # y_list = [y.copy()]
        # tao_list = [tao.copy()]
        while True:
            ## 判断是否图3 ##
            if isinstance(g,list):
                if t%2==0:
                    nei_list = nei_list1
                else:
                    nei_list = nei_list2
            
            for i in range(n):
                p = random.random()
                if p<r:
                    others = [ii for ii in range(n) if ii!=i]
                    ## 更新y[i][j],tao[i][j], (i!=j) ##
                    if len(nei_list[i])>0:#i个体有邻居，则更新y和tao
                        for j in others:
                            tao_nei = tao[nei_list[i],j]
                            idx_max = list(np.where(tao_nei==np.max(tao_nei))[0])
                            idx_sampled = random.choice(idx_max)
                            k = nei_list[i][idx_sampled]
                            tao[i][j] = tao[k][j]
                            y[i][j] = y[k][j]
                    ## 更新y[i][j],tao[i][j], (i==j) ##
                    count = {}
                    for ss in s:
                        count[ss] = 0
                    for y_other in y[i][others]:
                        count[y_other] +=1
                    val_array = np.array(list(count.values()))
                    idx_max = list(np.where(val_array==np.max(val_array))[0])
                    idx_sampled = random.choice(idx_max)
                    k = idx_sampled
                    y[i][i] = s[k]
                    tao[i][i] +=1
            ## 判断收敛，结束循环 ##
            if np.sum(y.reshape(-1)==y[0][0])==np.size(y):
                break
            t = t+1
            # y_list.append(y.copy())
            # tao_list.append(tao.copy())
        T.append(t)
    return T


def func2(n=4,r=0.5,s=['a','b','c'],n_loops=100,using_seed=False):
    T = []
    for i_l in range(n_loops):
        ### 随机数种子 ###
        if using_seed:
            seed = i_l
        else:
            seed = None
        random.seed(seed)
        
        ### 初始化 ###
        x = []
        for i in range(n):
            x.append(random.choice(s))
        x = np.array(x)
        b_bar = x.copy()
        u_bar = [np.sum(x==x[i])-1 for i in range(n)]
        
        ### 迭代 ###
        t = 1
        # x_list = [x.copy()]
        # b_bar_list = [b_bar.copy()]
        # u_bar_list = [u_bar.copy()]
        while True:
            ## 更新x ##
            p_list = [random.random() for i in range(n)]
            for i in range(n):
                #p<epsilon,x[i](t)随机取值；p>=epsilon,x[i](t)取b_bar[i]
                if p_list[i]<r: 
                    x[i] = random.choice(s)
                else:
                    x[i] = b_bar[i]
            
            ## 更新u ##
            u = [np.sum(x==x[i])-1 for i in range(n)]
            
            ## 更新u_bar,b_bar ##
            for i in range(n):
                if p_list[i]<r and u[i]>u_bar[i]:
                    b_bar[i] = x[i]
                    u_bar[i] = u[i]
                elif p_list[i]>=r:
                    u_bar[i] = u[i]
                else:
                    pass
            # x_list.append(x.copy())
            # b_bar_list.append(b_bar.copy())
            # u_bar_list.append(u_bar.copy())
            
            ## 判断收敛，结束循环 ##
            if np.sum(b_bar==b_bar[0])==np.size(b_bar):
                break
            t += 1
        # xx=np.vstack(x_list)
        # uu=np.vstack(u_bar_list)
        # bb=np.vstack(b_bar_list)
        T.append(t)
    return T


#### 横坐标 ####
r_list = [0.01]+[i/10 for i in range(1,10)]

#### 定义graph ####
g1 = nx.Graph()
g1.add_edges_from([[0,1],[1,2],[2,3],[3,0]])

g2 = nx.DiGraph()
g2.add_edges_from([[0,1],[1,2],[2,3],[3,0]])

gt1 = nx.DiGraph()
gt1.add_nodes_from([0,1,2,3])
gt1.add_edges_from([[0,1],[2,3]])
gt2 = nx.DiGraph()
gt2.add_nodes_from([0,1,2,3])
gt2.add_edges_from([[3,0],[1,2]])
g3 = [gt1,gt2]

#### 参数初始化 ####
using_seed=False #True #False
n_loops = 500

#### 纵坐标 ####
line1 = []
line2 = []
line3 = []
line4 = []
for r in r_list:
    T = func1(g1,r=r,n_loops=n_loops,using_seed=using_seed)
    line1.append(sum(T)/n_loops)
    
    T = func1(g2,r=r,n_loops=n_loops,using_seed=using_seed)
    line2.append(sum(T)/n_loops)

    T = func1(g3,r=r,n_loops=n_loops,using_seed=using_seed)
    line3.append(sum(T)/n_loops)
    
    T = func2(n=4,r=r,n_loops=n_loops,using_seed=using_seed)
    line4.append(sum(T)/n_loops)

#### 画折线图 ####
plt.figure()
plt.plot(r_list,line1,label='g1')
plt.plot(r_list,line2,label='g2')
plt.plot(r_list,line3,label='g3')
plt.plot(r_list,line4,label='--')
plt.xlabel('r')
plt.ylabel('average iterations')

plt.legend()
plt.show()

