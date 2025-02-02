#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 16:12:41 2025

@author: misticni
"""

import math
import numpy as np
import rustworkx as rx

class Ants:
    def __init__(self, NO_ANTS, MAX_ROUTE_LENGTH):
        #initial path traveresed by ant is 0
        self.costs = np.zeros(shape = NO_ANTS)
        self.routes = np.ones((NO_ANTS,MAX_ROUTE_LENGTH), dtype=np.int16)*-1
        self.routes[:,0] = 0
        self.route_length = np.zeros(shape = NO_ANTS, dtype=np.int8)

def distance(first: dict(), second:dict()) -> float:
    lat_diff = abs(first.get('lat') - second.get('lat'))
    lon_diff = abs(first.get('lon') - second.get('lon'))
    #distance using the Pythagorean theorem
    #one degree of lon and lat equals to 110km distance in real world
    dist = (math.sqrt(lat_diff) + math.sqrt(lon_diff))* 110
    #round distance to 2 decimals
    return round(dist,2)

def get_distance_matrix(graph):
    distance_m = np.eye(len(graph.node_indices()))
    for i in graph.node_indices():
        for j in graph.node_indices():
            distance_m[i][j] =  distance(graph[i],graph[j])
    return distance_m
#finds nodes nearest to each node and connects them
def closest_neighbors(graph, no_of_neighbors):
    for ind in graph.node_indices()[1:]:
        #list of distances of node
        ls = []
        ls_indices_of_nodes = []
        #assign max value to distances
        for no in range(no_of_neighbors):
            ls.append(float('inf'))
        #nodes that are not filed
        for no in range(no_of_neighbors):
            ls_indices_of_nodes.append(-1)
        #find distance to the node and 
        #add to the list if closer that the current furthest one
        #doesn't check any previous nodes
        for j in graph.node_indices()[1:]:
            if(distance(graph[ind],graph[j])) < max(ls):
                #zato sto ce najveci element biti zamenjen
                #treba da nadjemo gde je on tacno
                #jer ove dve liste sadrze informacije o razdaljini i broju cvora
                #da bi radilo treba da su na istim mestima
                ls_indices_of_nodes[ls.index(max(ls))] = j
                #changes the element with the highest value with the new one
                ls[ls.index(max(ls))] = distance(graph[ind], graph[j])
                
        for i, element in enumerate(ls):
            #if there is no close neighbhor for whatever reason
            if(ls_indices_of_nodes[i]) == -1: continue
            graph.add_edge(ls_indices_of_nodes[i], ind, element)
        
def heuristic_value(distance):
    return 1/distance

def get_heuristic_matrix(distance_matrix):
    np.fill_diagonal(distance_matrix, 'inf')
    heuristic_matrix = 1/distance_matrix
    return heuristic_matrix

def get_choice_matrix(pheromone_matrix, heuristic_matrix):
    choice_matrix = pheromone_matrix * heuristic_matrix
    return choice_matrix
     
def visit(ants, unvisited_nodes, choice_matrix):
    
    rng = np.random.default_rng()
    
    chosen_ant = np.argmin(ants.costs)
    
   
    current_node = ants.routes[chosen_ant][ants.route_length[chosen_ant]]
    
    
    choice_array = np.array(choice_matrix[current_node][unvisited_nodes])
    
    
    prob_array = choice_array / choice_array.sum()
    
    
    next_node = rng.choice(unvisited_nodes, p=prob_array)
   
    return (current_node, next_node, chosen_ant)
 
def evaporate(t,EVAPORATION_RATE):
    return (1-EVAPORATION_RATE)*t

""" chooses 3 best ants, so make sure that you have at least 3 ants"""
def dump_pheromone(t, EVAPORATION_RATE, PHEROMONE_DELTA, ants):
    min_inds = np.argsort(ants.costs)
    for i in range(3):
        for j in (range(ants.route_length[min_inds[i]])):
            frm, to = ants.routes[min_inds[i]][j], ants.routes[min_inds[i]][j+1]
            t[frm,to] += PHEROMONE_DELTA*2 / ants.costs[min_inds[i]]
        
    
    return t
def update_pheromone(t, EVAPORATION_RATE, PHEROMONE_DELTA, ants):
    t = evaporate(t, EVAPORATION_RATE)
    t = dump_pheromone(t,EVAPORATION_RATE, PHEROMONE_DELTA, ants)
    return t

    

def evaluate_solution(no_ants,cost_matrix, distance_matrix):
    sum = 0
    for i in range(no_ants):
        sum += cost_matrix[i]**2
    return round(sum,2)

def aco_tour(graph, NO_STORES, NO_ANTS, ants, distance_matrix, cm):
    unvisited_nodes = np.arange(1,NO_STORES)
   
    while len(unvisited_nodes) > 0:
        (current_node, next_node, chosen_ant) = visit(ants, unvisited_nodes, cm)
        #print(sum(ants.route_length))
        
        
        ants.costs[chosen_ant] += distance(graph[current_node], graph[next_node])
        ants.route_length[chosen_ant] += 1
        ants.routes[chosen_ant][ants.route_length[chosen_ant]] = next_node
        unvisited_nodes = np.delete(unvisited_nodes,np.where(unvisited_nodes == next_node))
    
    
        
        
        #all ants have to go home at the end of the run
        #add 0 as a last node in the route
        #add cost of going there
        if(len(unvisited_nodes) == 0):
            for i, ant in enumerate(ants.costs):
                index = np.where(ants.routes[i] == -1)[0][0]
                last_node = ants.routes[i][index-1]
                ants.costs[i] += distance(graph[last_node], graph[0])
                ants.route_length[i] +=1
                ants.routes[i][index] = 0
          
        
    return (evaluate_solution(NO_ANTS, ants.costs, distance_matrix), ants)


#def criteria:
    
#def get_probability_matrix(choice_array):  
    #def update_pheromone(ants):
    #def deposit_pheromone()