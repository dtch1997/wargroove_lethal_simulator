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
    def __init__(self):
        self.val2idx = {}
        self.idx2val = []
    
    def add(self, val):
        next_idx = self.size
        self.idx2val.append(val)
        self.val2idx[val] = next_idx
        
    def get_index(self, val):
        if val not in self.val2idx:
            raise ValueError(val)
        return self.val2idx[val]
    
    def get_value(self, idx):
        if idx >= len(self.idx2val):
            raise ValueError(idx)
        return self.idx2val[idx]
    
    def values(self):
        return self.val2idx.keys()
        
    @property
    def size(self):
        return len(self.idx2val)

class BaseDamageProvider:
    
    def __init__(self, unit_index, damage_table, crit_table, counter_table):
        self.unit_index = unit_index
        self.damage_table = damage_table
        self.crit_table = crit_table
        self.counter_table = counter_table
        
    @staticmethod
    def load(path):
        """
        path: Path to the json file of damage table
        """
        table_json = None
        with open(path, 'r') as jsonfile:
            table_json = json.load(jsonfile)
        
        
        unit_index = Index()
        for i, unit in enumerate(table_json['soldier']['damage'].keys()):
            unit_index.add(unit)
            
        damage_table = np.ones(shape = (unit_index.size, unit_index.size), dtype=int) * -1
        crit_table = np.zeros(shape = unit_index.size, dtype=float)
        counter_table = np.zeros(shape = unit_index.size, dtype=bool)
        
        for atk_unit_name in unit_index.values():
            atk_idx = unit_index.get_index(atk_unit_name)
            if atk_unit_name not in table_json.keys():
                continue
            
            unit_info = table_json[atk_unit_name]
            damage_dict = unit_info['damage']
            for def_unit_name, dmg in damage_dict.items():
                if dmg is None: dmg = -1
                def_idx = unit_index.get_index(def_unit_name)
                damage_table[atk_idx, def_idx] = dmg    
            crit_table[atk_idx] = unit_info['crit']
            counter_table[atk_idx] = unit_info['canCounter']
    
        return BaseDamageProvider(unit_index, damage_table, crit_table, counter_table)
    
    def get_base_damage(self, atk_idx, def_idx) -> int:
        return self.damage_table[atk_idx, def_idx].item()
    
    def get_crit_multiplier(self, unit_idx) -> float:
        return self.crit_table[unit_idx].item()
    
    def can_counter(self, unit_idx) -> bool:
        return self.counter_table[unit_idx].item()
        
        
        
if __name__ == "__main__":
    table = BaseDamageProvider.load('damagetables/mindmg_2.0.json')

    
        