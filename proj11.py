#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 17:44:56 2021

@author: Setty
"""

import csv
from place import Place

def apsp(g):
    '''All-Pairs Shortest Paths using the Floyd-Warshall algorithm.'''
    

    INFINITE = 2**63-1  

    # Initialize paths with paths for adjacent nodes
    paths = [[0 for j in range(len(g))] for i in range(len(g))]
    for i in range(len(g)):
        for j in range(len(g)):
            if g[i][j] != 0: 
                paths[i][j] = [i,j] # if two places are already adjacent then assign an initial path to them
            elif i != j:  # i == j means this is the same place so distance is zero
                g[i][j] = INFINITE # replacing zero by an "infinite" value
                # zero earlier meant that two places are not connected, now it will mean that they are not connected
                # initially, meaning that are "very-very" far ("virtually", for the sake of initialization)


    #apsp computation - floyd-warshall algorithm
    for k in range(len(g)):  # (for each) vertex k, to compare if i--k + k--j is shorter than i--j computed so far
        for i in range(len(g)): # (for each) vertex i of our interest
            for j in range(len(g)): # (for each) vertex j, to get the computed distance so far (between i and j)
                if g[i][j] > g[i][k] + g[k][j]: # determining if there is a shorter path (as per the above comment)
                    g[i][j] = g[i][k] + g[k][j] # updating the path-length value if there is a shorter path

                    # updating the path itself if there is a shorter path
                    paths[i][j] = paths[i][k][:]
                    paths[i][j].extend(paths[k][j][1:])

    # if a pair of places are still at infinite distance,
    # then assign them 0, to declare that they are not connected 
    for i in range(len(g)):
        for j in range(len(g)):
            if g[i][j] == INFINITE: 
                g[i][j] = 0

    return g,paths
#reads all the files that are inputted
def open_file():
    file_not_found = True
    while file_not_found:#while loop for user to input correct file
        file_name = input('Enter the file name: ')
        try:
            file_pointer = open(file_name,"r")
            file_not_found = False#boolean variable to determine the file 
        except FileNotFoundError:
            print('\nFile not found.! Try again.')
            file_not_found = True
    return file_pointer
    
#creates a list of tuples of three elements            
def read_file(fp):
    l=[]
    reader=csv.reader(fp)
    next(reader,None)
    for line in reader:
        
        city1=line[0]
        city2=line[1]
        dist1=line[2]
        l1=[city1,city2,int(dist1)]
        tup1=tuple(l1)
        l.append(tup1)
    return l    
#returns two matrices and a list of places in order
def adjacency_matrix(L):
    places_lst=[]
    for t in L:
        if t[0] not in places_lst:
            places_lst.append(t[0])
        if t[1] not in places_lst:
            places_lst.append(t[1])
    places_lst=sorted(places_lst)    
    n=len(places_lst)
    g=[]
    #creates a matrix of len of places_list with intialized values of zero
    for j in range(n):
        g.append([])
    for o in range(n):    
        for k in g:
            k.append(0)
    #dictionary to input values into matrix      
    matrixl={}
    for num,place1 in enumerate(places_lst):
        matrixl[place1]=num

    for ele in L:
        if ele[0] in places_lst and ele[1] in places_lst:
            g[matrixl[ele[0]]][matrixl[ele[1]]]=ele[2]
            g[matrixl[ele[1]]][matrixl[ele[0]]]=ele[2]
            
    return places_lst,g    
        
    
        
    
   
#use the class to return two dictionaries    
def make_objects(places_lst,g):
    g_path= apsp(g)
    by_city={}
    by_index={}
    for num,place1 in enumerate(places_lst):
        a_place=Place(place1,num)
        a_place.get_index()
        a_place.get_name()
        a_place.set_distances(g_path[0])
        a_place.set_paths(g_path[1])
        by_city[a_place.name]=a_place
        by_index[a_place.index]=a_place
    return by_city,by_index
    
      

      

        
        
    
#main function that prompts user to input directions and outputs total distance and shortest path
def main():
    BANNER = '\nBegin the search!'
    route_list=[]
    fp=open_file()
    L=read_file(fp)
    tup=adjacency_matrix(L)
    dicts=make_objects(tup[0], tup[1])
    city_D=dicts[0]
    index_D=dicts[1]
    print(BANNER)
    option=input("Enter starting place, enter 'q' to quit: ")
    
   #while loops to prompt user to enter places
    while option not in tup[0]:
        print('This place is not in the list!')
        option=input("Enter starting place, enter 'q' to quit: ")
    route_list.append(option)   
    while option.lower()!="q":
        dest_option=input('Enter next destination, enter "end" to exit: ')
        if dest_option==route_list[-1] and dest_option!="end":
            print("This destination is not valid or is the same as the previous destination!")
            dest_option=input('Enter next destination, enter "end" to exit: ')
            
        if dest_option in tup[0] and dest_option!="end":
            #create a list to get all the places user enters
            route_list.append(dest_option)
            
        if dest_option not in tup[0] and dest_option!="end":
            print("This destination is not valid or is the same as the previous destination!")
            dest_option=input('Enter next destination, enter "end" to exit: ')
            
        
        if dest_option=="end": 
            #for loop to use the get path and get distances given the index of the next route
            i=0
            j=1
            path_list=[]
            dist_list=[]
            error_list=[]
            for ele in  range (len(route_list)-1):
                option=route_list[i]
                dest_option=route_list[j]
                dest_index=tup[0].index(dest_option)
                op_i=tup[0].index(option)
                firstplace=city_D[option]
                firstplace.get_path(dest_index)
                firstplace.get_distance(dest_index)
                path_list.append(firstplace.get_path(dest_index))
                dist_list.append(firstplace.get_distance(dest_index))
                #create a list if two points are not connected
                if firstplace.get_path(dest_index)==0:
                    con_list=[option,dest_option]
                    error_list.append(con_list)
                i+=1
                j+=1
            
            if error_list==[]:
                t=0
                for thedis in dist_list:
                    thedis=int(thedis)
                    t+=thedis
                print("Your route is:")
                for path in path_list:
                    for p in path[:-1]:
                        print(tup[0][p])
                    if path_list[-1]==path:
                        print(tup[0][path[-1]])
                      
                print("Total distance =",t)    
            if error_list:
                for lists in error_list:
                    print("places {} and {} are not connected.".format(lists[0],lists[1]))
                   
                  
            # restarts the program when after user inputs end    
            route_list=[]
            print(BANNER)
            option=input("Enter starting place, enter 'q' to quit: ")
            route_list.append(option)
            
            
       
                 
            
            
        
        
    print('Thanks for using the software')
    
if __name__=='__main__':
    main()
