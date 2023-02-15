# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 15:54:32 2021

@author: sean
"""

import networkx as nx

g1=nx.complete_graph(9)
g2=nx.complete_graph(3)
g3=nx.complete_graph(4)
g4=nx.complete_graph(4)

g=nx.disjoint_union_all([g1,g2,g3,g4])

g.add_edge(1,10)
g.add_edge(13,10)
g.add_edge(16,14)

nx.write_graphml(g,'graph1.graphml')

g5=nx.complete_graph(7)
g6=nx.complete_graph(3)
g7=nx.complete_graph(5)
g8=nx.complete_graph(3)
g9=nx.complete_graph(2)

t=nx.disjoint_union_all([g5,g6,g7,g8,g9])
t.add_edge(1,8)
t.add_edge(1,12)
t.add_edge(1,19)
t.add_edge(8,12)
t.add_edge(12,4)
t.add_edge(12,5)
t.add_edge(8,5)
t.add_edge(13,16)

nx.write_graphml(t,'graph2.graphml')