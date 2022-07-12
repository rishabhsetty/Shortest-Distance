#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 17:47:15 2021

@author: Setty
"""
#Class of objects used in make_objects and in main on the proj11 file
class Place:
    def __init__(self, name, i):
        self.name=name
        self.index= i
        self.dist=None
        self.paths=None

    def get_index(self):
        return int(self.index)
        

    def get_name(self):
        return str(self.name)
       

    def set_distances(self, g):
        self.dist=g[self.index][:]
        

    def set_paths(self, paths):
        self.paths=paths[self.index][:]
 
    def get_distance(self, j):
        return self.dist[j]
        
        

    def get_path(self, j):
        return self.paths[j]
         
        

    def __str__(self):
        l1= [self.index,self.name,self.dist,self.paths]
        self.tup1=tuple(l1)
        self.tup1=self.tup1[:]
        str1= "Node {}, {}: distances {}, paths {}".format(self.tup1[0],self.tup1[1],self.tup1[2],self.tup1[3])
        return str1
        

    def __repr__(self):
        l2= [self.index,self.name,self.dist,self.paths]
        self.tup2=tuple(l2)
        return str(self.tup2)
        
        