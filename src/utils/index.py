# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 00:12:36 2020

@author: Daniel Tan
"""

import json
import numpy as np

class Index:
    """
    A convenience class to convert hashable keys to indices
    """
    def __init__(self, values = []):
        self.val2idx = {}
        self.idx2val = {}
        self.next_index = 0
        for value in values:
            self.add(value)
    
    def add(self, val):
        self.idx2val[self.next_index] = val
        self.val2idx[val] = self.next_index
        self.next_index += 1
        
    def remove(self, val):
        idx = self.val2idx[val]
        del self.val2idx[val]
        del self.idx2val[idx]
        
    def get_index(self, val):
        if val not in self.val2idx:
            raise ValueError(val)
        return self.val2idx[val]
    
    def get_value(self, idx):
        if idx >= len(self.idx2val):
            raise ValueError(idx)
        return self.idx2val[idx]
    
    @property
    def values(self):
        return self.val2idx.keys()
        
    @property
    def size(self):
        return len(self.idx2val)
    

    
        