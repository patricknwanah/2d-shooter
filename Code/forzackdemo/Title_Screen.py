import pygame
import time
pygame.font.init()

#loads pygame
pygame.init()

#image files
title = pygame.image.load('title.png')
pauseScreen = pygame.image.load('pause.png')
start = pygame.image.load('start.png')
quit = pygame.image.load('quit.png')
resume = pygame.image.load ('resume.png')

#color values
BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (200,0,0)
GREEN = (0,200, 0)
BRIGHT_GREEN = (0,255,0)
BRIGHT_RED = (255,0,0)

#text values
largeText = pygame.font.Font('freesansbold.ttf', 85)
smallText = pygame.font.Font('freesansbold.ttf', 20)

#score
score = 0

#sets health amount
health = 30

#loads the health images
global health_pics
health_pics = []
for i in range(health + 1):
    health_pics.append(pygame.image.load('health' + str(i) + '.png'))

#gameDisplay = pygame.display.set_mode((display_width,display_height))
#pygame.display.set_caption('Title')
#clock = pygame.time.Clock()

#function that takes a string text and font type
#returns textSurface with the info
def text_objects(text, font):
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()
#button function used in title screen
def button(gameDisplay, msg, x, y, width, height, acolor, icolor):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+width > mouse[0] > x and y+height > mouse[1] > y:
        #pygame.draw.rect(gameDisplay,acolor, (x,y,width,height))
        if click[0] == 1:
            return True
    """else:
        pygame.draw.rect(gameDisplay,icolor,(x,y,width,height))
   
    textSurf, textRect = text_objects(msg, smallText)
    textRect = ( (x + (width/6)), (y + (height/3)) )
    gameDisplay.blit(textSurf, textRect) """
    return False

    
#function that runs the title screen
def intro(gameDisplay, clock):
    intro = True
    
    #screen display size
    display_width = pygame.display.get_surface().get_width()
    display_height = pygame.display.get_surface().get_height()
    
    while intro:
        for event in pygame.event.get():
            print(event) #I used this to show mouse events 
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
        
        gameDisplay.blit(title, (0,0))
        #pygame.display.flip()
        gameDisplay.blit(start, (150,450))
        #pygame.display.flip()
        gameDisplay.blit(quit, (550,450))
        #pygame.display.flip()
        
        if button(gameDisplay, "START", 150,450,100,50,BRIGHT_GREEN, GREEN):
            intro = False
          
        if button(gameDisplay, "QUIT", 550,450,100,50, BRIGHT_RED, RED):
            pygame.quit()       
        
        pygame.display.flip()
        clock.tick(30)

def pause(gameDisplay):
    paused = True
    clock = pygame.time.Clock()
    
    #screen display size
    #display_width = pygame.display.get_surface().get_width()
    # display_height = pygame.display.get_surface().get_height()
    
    while paused:
        for event in pygame.event.get():
            print(event) #I used this to show mouse events 
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
        
        gameDisplay.blit(pauseScreen, (0,0))
        gameDisplay.blit(resume, (150,500))
        gameDisplay.blit(quit, (550,500))
        pygame.display.flip()
        
        if button(gameDisplay, "RESUME", 150,500,100,50,BRIGHT_GREEN, GREEN):
            paused = False
          
        if button(gameDisplay, "QUIT", 550,500,100,50, BRIGHT_RED, RED):
            pygame.quit()
        


        pygame.display.update()
        clock.tick(30)
    return

def setScore(int):
    global score
    score = int

def Score(display, display_width, display_height):
    width = (display_width / 2) + 50
    height = 10
    #click = pygame.mouse.get_pressed()
    label = smallText.render('SCORE', True, WHITE)
    display.blit(label, (width, height))
    value = smallText.render(str(score), True, WHITE)
    display.blit(value, (width + 15, height + 20))
    #pygame.display.update()

def setHealth(int):
    global health
    health = int

def getHealth():
    return health

def drawHealth(screen):
    screen.blit(health_pics[health], (10,10))

def minusHealth( screen):
#subtracts 1 health from player
    setHealth(health-1)
    screen.blit(health_pics[health],(10,10))
    if health < 0:
        setHealth(0)
    #mouse = pygame.mouse.get_pressed()
    """if (mouse[0] == 1 or player_rect == True):
        print('hit')
        #subtracts 1 health from player
        setHealth(health-1)
        """
    if (health == 0):
        print('dead. X_X')
        #player.kill()
        setHealth(30)
        setScore(0)
        return False