# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 12:31:38 2020

@author: Daniel Tan
"""


from src.assets.utils import BaseDamageProvider
from src.unit import Unit, CombatSimulator

base_damage_provider = BaseDamageProvider.load("src/assets/damagetables/mindmg_2.0.json")

atk_mage = Unit.from_name('mage', base_damage_provider)
def_sword = Unit.from_name('soldier', base_damage_provider)
atk_terrain_defense = 0.2
def_terrain_defense = 0.1

results = CombatSimulator.simulate_combat(atk_mage, 0.2, False,
                                          def_sword, 0.1, False)

print(results)