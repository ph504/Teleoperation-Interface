import pygame
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((400, 300))
done = False
white = (255,255,255)
bg = (127,127,127)
sound=pygame.mixer.Sound("src/test/src/sounds/bleep_sliced.wav")
font = pygame.font.SysFont("Arial", 14)
text1=font.render(" SHOOT ", True, bg)
rect1 = text1.get_rect(midbottom=(200,300))
img=pygame.image.load("src/test/src/images/happy.png")
rect2=img.get_rect(midtop=(200, 270))
kup=0
psmode=True
screen = pygame.display.set_mode((400,300))
screen.fill(white)
y=265


while not done:

   for event in pygame.event.get():
      screen.blit(text1, rect1)
      pygame.draw.rect(screen, (255,0,0),rect1,2)
      if event.type == pygame.QUIT:
         sound.stop()
         done = True
      if event.type == pygame.KEYDOWN:
         if event.key == pygame.K_SPACE:
            print ("space")
            if kup==0:
               screen.blit(img, (190,y))
               kup=1
   if kup==1:
      y=y-1
      screen.blit(img, (190,y))
      sound.play()
      if y<=0:
         kup=0
         y=265
   pygame.display.update()