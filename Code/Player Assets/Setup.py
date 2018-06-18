import pygame, time

#
#IMPORT NECESSARY CLASSES HERE
#

#set the width and height
display_width = 800
display_height= 600

#init pygame
pygame.init()

#create reference to white screen
white = (255, 255, 255)

#load the game display, start the clock
gameDisplay = pygame.display.set_mode((display_height, display_width))
pygame.display.set_caption('Test')
clock = pygame.time.Clock()

#
#
#
#DEFINE AND DECLARE PLAYER OBJECTS, AI OBJECTS, ETC.
#
#
#

#Variables to handle the x and y change of the player
x_change = 0
y_change = 0

#loop control variable
crashed = False

#Game Loop Controller
while not crashed:

    #Event Handler
    for event in pygame.event.get():

        #Exit if quit
        if event.type == pygame.QUIT:
            crashed = True
        
        #Handle key pressing
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                x_change = -5
            if event.key == pygame.K_d:
                x_change = 5
            if event.key == pygame.K_w:
                y_change = -10
            if event.key == pygame.K_s:
                y_change = 10

        #Handle key release
        #This resets our change variables to 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                x_change = 0
            if event.key == pygame.K_d:
                x_change = 0
            if event.key == pygame.K_w:
                y_change = 0
            if event.key == pygame.K_s:
                y_change = 0
        
    #update the display
    gameDisplay.fill(white)
    player.update(x_change, y_change)
    player.draw(gameDisplay)
    pygame.display.update()
    clock.tick(30)     

#quit
pygame.quit()
quit()