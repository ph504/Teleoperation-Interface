from pickle5 import pickle
from types import SimpleNamespace


tutorial_mode = None
bar_controller = True #true stop, false active #TODO


social_mode = None 

"""
It is always H-AI

"""

second_round = None # false is second round, true is first round

in_inspection = False #check whether in inspection screen or not

participant = None

is_code_list_2 = None #False is Red Papers, True is Blue Papers

second_round_diff = 0

ds1_scoreloss_nonsocial = 200
ds2_scoreloss_nonsocial = 250
ds3_scoreloss_nonsocial_ai = 150
ds3_scoreloss_nonsocial_h = 175

#Social - DS1 for Human and DS2 for AI
ds1_scoreloss_social = 250
ds2_scoreloss_social = 200
ds3_scoreloss_social_ai = 150
ds3_scoreloss_social_h = 175


jackalai_active = False

#Social | Non-Social
#===================
# Human    |    AI
#-------------------
# AI       |   Human
#-------------------

