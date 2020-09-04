# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 23:39:53 2020

@author: Daniel Tan
"""


import numpy as np
import src.assets as assets

class RngProvider():
    def get_rng(self):
        return np.random.uniform(0.0, 1.0)

class Unit:
    def __init__(self, unit_type: int, unit_id, health=100):
        """
        unit_type: An integer. Constructed canonically by assets.utils.BaseDamageProvider
        unit_id: A unique id assigned to this particular unit instances
        health: An integer from 0 - 100
        """
        self.unit_type = unit_type
        self.unit_id = unit_id
        
    @property
    def movement_range(self):
        return 1
    
class CombatSimulator:
    def __init__(self, base_damage_provider: 'assets.utils.BaseDamageProvider',
                 rng_provider):
        self.base_damage_provider = base_damage_provider
        self.rng_provider = rng_provider

    def calculate_damage(self, 
                         base_damage: float, 
                         atk_health: int,
                         def_health: int,
                         terrain_defense: float,
                         crit_multiplier: float,
                         rng_val: float,) -> int:
        """
        terrain defense: a number from -0.2 to 0.4
        crit_multiplier: default 1.0
        rng_val: A numpy array of shape (num_trials,). Multiple entries = multiple calculations in parallel
        
        Note: this function is deterministic because we fix a luck value
        """
        
        rng_mul = 1.0 / np.maximum(1.0, crit_multiplier)
        rng_add = (1.0 - rng_mul) * 0.5
        rng_bonus = 0 + (10 - 0) * (rng_val * rng_mul + rng_add)

        effective_defense = (def_health / 100) * np.maximum(0,terrain_defense) \
                            - np.maximum(0, -terrain_defense)
        
        damage = (atk_health / 100) * (1 - effective_defense) * (base_damage + rng_val) * crit_multiplier
        whole_damage = np.floor(100 * damage + 0.5)
        whole_damage[np.logical_and(damage > 0.001, whole_damage < 1)] = 1
        
        return whole_damage
    
    
    def simulate_combat(self, atk_unit, atk_terrain_defense, is_atk_crit 
                        def_unit, def_terrain_defense, is_def_crit, 
                        trials=101):
        
        def_die = np.zeros(trials, dtype=bool)
        atk_die = np.zeros(trials, dtype=bool)
        
        rng_val = np.linspace(0.0, 1.0, trials)
        atk_dmg = self.calculate_damage(atk_unit, def_unit, def_terrain_defense, is_atk_crit, atk_rng)

            


class GameBoard:
    def __init__(self, terrain_layer: np.ndarray):
        self.terrain_layer = terrain_layer
        self.unit_layer = []
        
    def get_unit_move(self, unit):
        max_x = unit.movement_range
        max_y = unit.movement_range
    