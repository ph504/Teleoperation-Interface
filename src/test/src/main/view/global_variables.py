from pickle5 import pickle
from types import SimpleNamespace
import pygame

tutorial_mode = None
practice_mode = None # if true, start state machine and no binding, if false then it is pure tutorial
bar_controller = True #true stop, false active. only for tutorial, in practice mode not training session


social_mode = None 

"""
It is always H-AI

"""

second_round = False # false is second round, true is first round

in_inspection = False #check whether in inspection screen or not

participant = None

is_code_list_2 = False #False is Red Papers, True is Blue Papers

second_round_diff = 0

task_advance = 0
tuto_miss = 0

pygame.init()
pygame.mixer.init()


beep_sound = pygame.mixer.Sound("/home/pouya/catkin_ws/src/test/src/sounds/beep.wav")
beep_sliced_sound = pygame.mixer.Sound("/home/pouya/catkin_ws/src/test/src/sounds/bleep_sliced.wav")
danger_alarm_sound = pygame.mixer.Sound("/home/pouya/catkin_ws/src/test/src/sounds/danger-alarm.wav")
error_sound = pygame.mixer.Sound("/home/pouya/catkin_ws/src/test/src/sounds/error.wav")
inspect_succ_sound = pygame.mixer.Sound("/home/pouya/catkin_ws/src/test/src/sounds/inspect_succ.wav")



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
danger_mode = False

#Social | Non-Social
#===================
# Human    |    AI
#-------------------
# AI       |   Human
#-------------------

