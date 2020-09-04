# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 23:39:53 2020

@author: Daniel Tan
"""


import numpy as np
# import src.assets as assets

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

    @staticmethod
    def calculate_damage(base_damage: float, 
                         atk_health: int,
                         def_health: int,
                         terrain_defense: float,
                         crit_multiplier: float,
                         rng_val: 'np.ndarray of type float') -> 'np.ndarray of type int':
        """
        terrain defense: a number from -0.2 to 0.4
        crit_multiplier: default 1.0
        rng_val: A numpy array of shape (num_trials,). Multiple entries = multiple calculations in parallel
        
        Note: this function is deterministic because we fix a luck value
        """
        
        rng_mul = 1.0 / np.maximum(1.0, crit_multiplier)
        rng_add = (1.0 - rng_mul) * 0.5
        rng_bonus = 0 + (0.1 - 0) * (rng_val * rng_mul + rng_add)

        offense = base_damage / 100 + rng_bonus
        defense = 1.0 - ((def_health / 100) * np.maximum(0,terrain_defense) \
                            - np.maximum(0, -terrain_defense))
        damage = (atk_health / 100) * defense * offense * crit_multiplier
        whole_damage = np.floor(100 * damage + 0.5).astype(int)
        whole_damage[np.logical_and(damage > 0.001, whole_damage < 1)] = 1
        
        return whole_damage
    
    # TODO: missing the lowest damage value
    @staticmethod
    def calculate_thresholds( base_damage: int, 
                            atk_health: int,
                            def_health: int,
                            terrain_defense: float,
                            crit_multiplier: float,
                            rng_low = 0.0,
                            rng_high = 1.0,
                            num_branches = 10,
                            depth=4):
        """
        Find the threshold luck values for each whole-number damage result.
        Use binary search to reduce number of trials
        
        Return: 
            A dict of whole-number damage values and the corresponding 
            min RNG value needed to reach the rounding breakpoint
         
        """
        # Note that dmg is an increasing function of rng_val     
        rng_val = np.linspace(rng_low, rng_high, num_branches+1)
        dmg = CombatSimulator.calculate_damage(base_damage, atk_health, def_health, terrain_defense, crit_multiplier, rng_val)
        if depth == 0:
            return {dmg[-1].item(): rng_high}
        
        thresholds = {}
        for i in range(rng_val.shape[0] - 1):
            dmg_low, dmg_high = dmg[i].item(), dmg[i+1].item()
            rng_low, rng_high = rng_val[i].item(), rng_val[i+1].item()
            
            if dmg_high > dmg_low:
                thresholds.update(CombatSimulator.calculate_thresholds(base_damage, atk_health, def_health, terrain_defense, crit_multiplier, rng_low, rng_high, num_branches, depth-1))
        return thresholds
    
    def simulate_combat(self, atk_unit, atk_terrain_defense, is_atk_crit, 
                        def_unit, def_terrain_defense, is_def_crit, 
                        trials=101):

        
        base_damage = self.base_damage_provider.get_base_damage(atk_unit.unit_type, def_unit.unit_type)
        def_die = np.zeros(trials, dtype=bool)
        atk_die = np.zeros(trials, dtype=bool)
        


class GameBoard:
    def __init__(self, terrain_layer: np.ndarray):
        self.terrain_layer = terrain_layer
        self.unit_layer = []
        
    def get_unit_move(self, unit):
        max_x = unit.movement_range
        max_y = unit.movement_range
        
        
if __name__ == "__main__":
    #damage = CombatSimulator.calculate_damage(55, 100, 100, 0, 1, np.linspace(0,1,11))
    #print(damage)
    thresholds = CombatSimulator.calculate_thresholds(55, 100, 100, 0, 1, depth=2)
    print(thresholds)
    