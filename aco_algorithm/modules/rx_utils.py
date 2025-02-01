#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 16:17:20 2025

@author: misticni
"""

import random
import rustworkx as rx
from modules import aco_utils as aco

def random_gen(n):
    #generates a graph with depot in the middle and x number of stores around
    #store is only connected to the depot
    graph = rx.generators.star_graph(n, multigraph=False)


    #depot coordinates
    graph[0] = {
        'lat' : 20.45,
        'lon' : 44.8
        }
    # random generation of store coordinates inside the square
    # rounded to 5 decimals
    for index in graph.node_indices()[1:]:
        graph[index] = {
            'lat' : round((random.random()*0.3)+20.3,5),
            'lon' : round((random.random()*0.2)+44.7,5)
            }
    
    #adds value to the edges between depot and the stores
    for ind in graph.node_indices()[:-1]:
        graph.add_edge(0, ind+1,aco.distance(graph[0],graph[ind+1]))
        
    return graph
