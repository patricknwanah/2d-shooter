import pygame

#color variables
black = (0,0,0)
green = (0,200, 0)

#health varibale starting at health
health = 100

# starts pygame draws screen
pygame.init()
gamedisplay = pygame.display.set_mode((800,600),0,32)
gamedisplay.fill(black)

pygame.draw.rect(gamedisplay,green,(50,50, 10, health))
pygame.display.update()

def minusHealth():
    #if player is hit by projectile/enemy
    if ():
        #subtracts 10 health from player
        health-10
        pygame.draw.rect(gamedisplay,50,50,10,health)
        pygame.display.update()
        if (health == 0):
            #kill player
     

#function that can be used to add health if we decide to add health pick-up
def addHealth():
    #if pickup health 
    if():
        #adds 
        health + 10
        pygame.draw.rect(gamedisplay,50,50,10,health)
        pygame.display.update()
    #handles overflow of health
        if(health > 100):
            health = 100
            pygame.draw.rect(gamedisplay,50,50,10,health)
            pygame.display.update()


    