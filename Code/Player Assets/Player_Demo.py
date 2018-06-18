import pygame, time
#init pygame
pygame.init()
from Player_Assets import *
from Title_Screen import *
from Physics_Engine import *

#color values
black = (0,0,0)
white = (255, 255, 255)
red = (200,0,0)
green = (0,200, 0)
bright_green = (0,255,0)
bright_red = (255,0,0)

#load the game display to fullscreen, start the clock
gameDisplay = pygame.display.set_mode((800, 600)) 
pygame.display.set_caption('Test')
clock = pygame.time.Clock()

#create sprite groups and add player.
visible = pygame.sprite.Group()

#Create reference to engine
physics = Engine()

#loop control variable
crashed = False

#Create blocks
rect = Block(200, 500, 40, 40)
rect2 = Block(300, 200, 40, 80)

#Add them to a list and pass them to the player
block_list = pygame.sprite.Group()
block_list.add(rect)
block_list.add(rect2)

#add all objects to visible group
visible.add(rect2)
visible.add(rect)

#Create player reference, load the image
#Assign the collision list to the player
player = Player(300, 300, 'main_player.png', gameDisplay, visible)
player.collide_list = block_list

#call title screen
intro(gameDisplay, clock)

#Game Loop 
while not crashed:
    #Event Handler
    for event in pygame.event.get():

        #Exit if quit
        if event.type == pygame.QUIT:
            crashed = True

    #update all objects.
    visible.update()
    
    #update the display
    gameDisplay.fill(black)

    #draw all visible sprites.
    visible.draw(gameDisplay)

    pygame.display.update()
    clock.tick(30)     

#quit
pygame.quit()
quit()