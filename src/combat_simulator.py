# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 23:39:53 2020

@author: Daniel Tan
"""


import numpy as np
import collections
    
class CombatSimulator:

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
    
    @staticmethod
    def calculate_probabilities(base_damage: int, 
                                atk_health: int,
                                def_health: int,
                                terrain_defense: float,
                                crit_multiplier: float,
                                depth=4):
        """
        Find the possible damage outcomes as well as the probability of each damage outcome
        Use binary search to reduce number of trials
        
        Return: 
            A dict of whole-number damage values and the corresponding 
            min RNG value needed to reach the rounding breakpoint
         
        """
        # Note that dmg is an increasing function of rng_val     
    
        def calculate_thresholds_helper_( base_damage: int, 
                                        atk_health: int,
                                        def_health: int,
                                        terrain_defense: float,
                                        crit_multiplier: float,
                                        rng_low = 0.0,
                                        rng_high = 1.0,
                                        num_branches = 10,
                                        depth=4):
            """
            Find the threshold luck values for each damage outcome
            """
            rng_val = np.linspace(rng_low, rng_high, num_branches+1)
            dmg = CombatSimulator.calculate_damage(base_damage, atk_health, def_health, terrain_defense, crit_multiplier, rng_val)
            if depth == 0:
                return {dmg[-1].item(): rng_high}
            
            thresholds = {}
            for i in range(rng_val.shape[0] - 1):
                dmg_low, dmg_high = dmg[i].item(), dmg[i+1].item()
                rng_low, rng_high = rng_val[i].item(), rng_val[i+1].item()
                
                if dmg_high > dmg_low:
                    thresholds.update(calculate_thresholds_helper_(base_damage, atk_health, def_health, terrain_defense, crit_multiplier, rng_low, rng_high, num_branches, depth-1))
            return thresholds
        
        thresholds = calculate_thresholds_helper_(base_damage,
                                                 atk_health,
                                                 def_health, 
                                                 terrain_defense,
                                                 crit_multiplier,
                                                 rng_low=0.0,
                                                 rng_high=1.0,
                                                 num_branches = 10,
                                                 depth=depth)
        # Manually add in the minimum damage that gets skipped
        min_dmg = min(thresholds.keys())
        if thresholds[min_dmg] > 0:
            thresholds[min_dmg-1] = 0
            
        # Calculate the probabilities of each outcome
        probs = {}
        dmgs = sorted(thresholds.keys())
        for dmg in dmgs:
            threshold = thresholds[dmg]
            next_threshold = thresholds[dmg+1] if (dmg+1) in thresholds else 1.0
            probability = np.around(next_threshold - threshold, decimals= depth)
            probs[dmg] = probability
            
        return probs
    
    @staticmethod 
    def simulate_combat(atk_unit, atk_terrain_defense, is_atk_crit, 
                        def_unit, def_terrain_defense, is_def_crit,
                        depth = 4):
        """
        Simulate a combat between atk_unit and def_unit 
        deoth: Number of decimal places with which to calculate raw probabilities
        
        Returns:
            Dictionary of (final_atk_health, final_def_health) : probability 
        """
        
        # Dict[(final_atk_health, final_deF_health)]: probability
        results = collections.defaultdict(int)
        
        atk_outcomes = CombatSimulator.calculate_probabilities(
            base_damage = atk_unit.get_base_damage(def_unit),
            atk_health = atk_unit.health,
            def_health = def_unit.health,
            terrain_defense = def_terrain_defense,
            crit_multiplier = atk_unit.crit_multiplier if is_atk_crit else 1,
            depth = depth
        )
        
        for atk_dmg, atk_prob in atk_outcomes.items():
            final_def_health = max(0, def_unit.health - atk_dmg)
            if final_def_health == 0 or not def_unit.can_counter:
                results[(atk_unit.health, final_def_health)] += atk_prob
            else:
                conditional_def_outcomes = CombatSimulator.calculate_probabilities(
                    base_damage = def_unit.get_base_damage(atk_unit),
                    atk_health = final_def_health,
                    def_health = atk_unit.health,
                    terrain_defense = atk_terrain_defense,
                    crit_multiplier = def_unit.crit_multiplier if is_def_crit else 1,
                    depth = depth
                )    
                for def_dmg, def_prob in conditional_def_outcomes.items():
                    final_atk_health = max(0, atk_unit.health - def_dmg)
                    results[(final_atk_health, final_def_health)] += atk_prob * def_prob
                    
        return results
    