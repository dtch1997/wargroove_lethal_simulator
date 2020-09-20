# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 12:31:38 2020

@author: Daniel Tan
"""


from src.combat_simulator import CombatSimulator
from src.unit import Unit, UnitDataProvider

def simulate_combat_example():
    print("Simulating combat between a Mage on flagstone and Soldier on plains")
    provider = UnitDataProvider.load("assets/unitdata_2.0.json")
    
    atk_mage = Unit.from_name('mage', provider)
    def_sword = Unit.from_name('soldier', provider)
    atk_terrain_defense = 0.2
    def_terrain_defense = 0.1
    
    results = CombatSimulator.simulate_combat(atk_mage, 0.2, False,
                                              def_sword, 0.1, False)
    
    for (final_atk_health, final_def_health), prob in results.items():
        print(f"Attacker {final_atk_health}, defender {final_def_health}: probability {100 * prob}%")      

def simulate_combat_test():
    print("Testing mysterious bug")
    provider = UnitDataProvider.load("assets/unitdata_2.0.json")
    
    atk_unit = Unit.from_name('giant', provider, health=100)
    def_unit = Unit.from_name('commander', provider, health=52)
    atk_terrain_defense = 0.1
    def_terrain_defense = 0.0
    
    results = CombatSimulator.simulate_combat(atk_unit, atk_terrain_defense, False,
                                              def_unit, def_terrain_defense, False, depth=4)
    
    for (final_atk_health, final_def_health), prob in results.items():
        print(f"Attacker {final_atk_health}, defender {final_def_health}: probability {100 * prob}%")      


def simulate_combat_sequence_example():
    print("Simulating attacks on Commander by a variety of units")
    provider = UnitDataProvider.load("assets/unitdata_2.0.json")
    
    defend_instance = (Unit.from_name('commander', provider), 0.0, False)
    attack_instances = [
        (Unit.from_name('mage', provider), 0.1, False, False),
        (Unit.from_name('soldier', provider), 0.1, False, False),
        (Unit.from_name('giant', provider), 0.1, False, False)
    ]
    
    state_dist_history = CombatSimulator.simulate_combat_sequence(defend_instance, attack_instances)
    final_state_dist = state_dist_history[-1]
    prob_def_death = final_state_dist[0]
    percentiles = {}
    expected_final_health = 0
    states = sorted(final_state_dist.keys())
    
    cum_prob = 0
    for state in states:
        if state < 0:
            continue
        prob = final_state_dist[state]
        cum_prob += prob
        expected_final_health += state * prob
        

    print(f"Probability of lethal: {prob_def_death:.4f}")
    print(f"Expected final health: {expected_final_health}")

    
if __name__ == "__main__":
    # simulate_combat_test()
    simulate_combat_sequence_example()