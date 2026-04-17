# -*- coding: utf-8 -*-
"""
@author: Clément Hardy


"""

#%% 1. LOADING PACKAGES AND FUNCTIONS

import os
# os.chdir(r"D:\OneDrive -UQAM\OneDrive - UQAM\1 - Projets\Thèse - Chapitre 3\2_Projet_extension_REHARVEST\Examples")

print("Python script : Switching harvest parameter files !")

os.rename((os.getcwd() + "/inputs/disturbances/magicHarvest/biomass-harvest_SetUp_s2e1.txt"), (os.getcwd() + "/inputs/disturbances/magicHarvest/biomass-harvest_SetUp_s2e1_OLD.txt"))
os.rename((os.getcwd() + "/inputs/disturbances/magicHarvest/biomass-harvest_SetUp_s2e1_ALT.txt"), (os.getcwd() + "/inputs/disturbances/magicHarvest/biomass-harvest_SetUp_s2e1.txt"))
os.rename((os.getcwd() + "/inputs/disturbances/magicHarvest/biomass-harvest_SetUp_s2e1_OLD.txt"), (os.getcwd() + "/inputs/disturbances/magicHarvest/biomass-harvest_SetUp_s2e1_ALT.txt"))

print("Python script : Switching finished ! Ending...")
