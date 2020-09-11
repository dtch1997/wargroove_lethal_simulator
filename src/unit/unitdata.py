# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 15:02:57 2020

@author: Daniel Tan
"""

import numpy as np
import json
from src.utils import Index

class UnitDataProvider:
    
    def __init__(self, unit_index, movetype_index, 
                 damage_table, crit_table, counter_table, movement_table):
        self.unit_index = unit_index
        self.movetype_index = movetype_index
        
        self.damage_table = damage_table
        self.crit_table = crit_table
        self.counter_table = counter_table
        self.movement_table = movement_table
        
    @staticmethod
    def load(path):
        """
        path: Path to the json file of damage table
        """
        table_json = None
        with open(path, 'r') as jsonfile:
            table_json = json.load(jsonfile)
        
        
        unit_index = Index(table_json['soldier']['damage'].keys())
        movetype_index = Index([table_json[unit_name]['moveType'] for unit_name in unit_index.values])
            
        damage_table = np.ones(shape = (unit_index.size, unit_index.size), dtype=int) * -1
        crit_table = np.zeros(shape = unit_index.size, dtype=float)
        counter_table = np.zeros(shape = unit_index.size, dtype=bool)
        movement_table = np.zeros(shape = [unit_index.size, 2])
        
        for atk_unit_name in unit_index.values:
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
            
            movement_table[atk_idx, 0] = movetype_index.get_index(unit_info['moveType'])
            movement_table[atk_idx, 1] = unit_info['moveRange']
    
        return UnitDataProvider(unit_index, movetype_index,
                                damage_table, crit_table, counter_table, movement_table)
    
    def get_base_damage(self, atk_idx, def_idx) -> int:
        return self.damage_table[atk_idx, def_idx].item()
    
    def get_crit_multiplier(self, unit_idx) -> float:
        return self.crit_table[unit_idx].item()
    
    def can_counter(self, unit_idx) -> bool:
        return self.counter_table[unit_idx].item()
    
    def get_movement_type(self, unit_idx): 
        return self.movement_table[unit_idx, 0]
    
    def get_movement_range(self, unit_idx):
        return self.movement_table[unit_idx, 1]