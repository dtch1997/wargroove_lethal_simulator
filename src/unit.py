# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 23:39:53 2020

@author: Daniel Tan
"""


import numpy as np
import collections

class Unit:
    """
    Unit info data class, plus a high-level wrapper around BaseDamageProvider
    """
    
    def __init__(self, unit_type: int, unit_data_provider, health=100, unit_id=None):
        """
        unit_type: An integer. Constructed canonically by assets.utils.BaseDamageProvider
        unit_id: A unique id assigned to this particular unit instances
        health: An integer from 0 - 100
        base_damage_provider: An instance of BaseDamageProvider
        """
        self.unit_type = unit_type
        self.unit_id = unit_id
        self.health = health
        self.unit_data_provider = unit_data_provider
        
    @staticmethod
    def from_name(unit_name, unit_data_provider, health=100, unit_id = None):
        unit_type = unit_data_provider.unit_index.get_index(unit_name)
        return Unit(unit_type, unit_data_provider, health, unit_id)
        
        
    @property
    def crit_multiplier(self):
        return self.unit_data_provider.get_crit_multiplier(self.unit_type)
    
    @property
    def can_counter(self):
        return self.unit_data_provider.can_counter(self.unit_type)
    
    def get_base_damage(self, other_unit):
        return self.unit_data_provider.get_base_damage(self.unit_type, other_unit.unit_type)
        
    @property
    def movement_range(self):
        return self.unit_data_provider.get_movement_range(self.unit_type)
    
    @property
    def movement_type(self):
        return self.unit_data_provider.get_movement_type(self.unit_type)
    