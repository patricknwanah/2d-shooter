import pygame
import time


#loads pygame
#pygame.init()

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

#gameDisplay = pygame.display.set_mode((display_width,display_height))
#pygame.display.set_caption('Title')
#clock = pygame.time.Clock()

#function that takes a string text and font type
#returns textSurface with the info
def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()
#button function used in title screen
def button(gameDisplay, msg, x, y, width, height, acolor, icolor):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+width > mouse[0] > x and y+height > mouse[1] > y:
        pygame.draw.rect(gameDisplay,acolor, (x,y,width,height))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(gameDisplay,icolor,(x,y,width,height))
   
    textSurf, textRect = text_objects(msg, smallText)
    textRect = ( (x + (width/6)), (y + (height/3)) )
    gameDisplay.blit(textSurf, textRect)
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
            
        
        gameDisplay.fill(black)
        
        TextSurf, TextRect = text_objects('Low Rez Studios', largeText)
        TextRect.center = ((display_width/2), (display_height/2))
        gameDisplay.blit(TextSurf, TextRect)
        
        if button(gameDisplay, "START", 150,450,100,50,bright_green, green):
            intro = False
          
        if button(gameDisplay, "QUIT", 550,450,100,50, bright_red, red,):
            pygame.quit()
        


        pygame.display.update()
        clock.tick(30)



