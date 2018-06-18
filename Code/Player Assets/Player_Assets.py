<<<<<<< HEAD
﻿import pygame
=======
import pygame
from Physics_Engine import *

#Create global physics reference
physics = Engine()
>>>>>>> origin/master

#Player class. Contains an x/y coordinate and a picture
class Player(pygame.sprite.Sprite):

    #initialization method
    def __init__(self, x, y, image, gameDisplay, group):

        #call superclass constructor
        pygame.sprite.Sprite.__init__(self)

        #init object attributes
        self.x = x
        self.y = y

        #delta x and delta y, for velocities on the x and y axes, respectively.
        self.dx = 0  
        self.dy = 0

        #maximum velocities on x and y axes.
        self.maxdx = 20  
        self.maxdy = 20

        #How much to accelerate by each frame.
        self.accelx = 2 
        self.accely = 2

        #rate of deceleration when no key is pressed.
        self.decelx = 1 
        self.decely = 1

        #load image and create a rectangle
        self.image = pygame.image.load(image).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.area = gameDisplay.get_rect()

        #Must add player to visible group so it gets updated.
<<<<<<< HEAD
        #self.add(visible)
        #added a health variable
        self.health = 100
=======
        self.add(group)
>>>>>>> origin/master

    #update will update the players position on the screen
    def update(self):
        
        #Store Keys in variable
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_a]:
            self.dx -= self.accelx
        if keys[pygame.K_d]:
            self.dx += self.accelx
        if keys[pygame.K_w]:
            self.dy -= self.accely
        if keys[pygame.K_s]:
            self.dy += self.accely

        #TODO: Add shift to sprint.
        #Player must slow down if no keys are pressed.
        if not (keys[pygame.K_a] or keys[pygame.K_d]):
            if (-self.accelx < self.dx < self.accelx): #Set to zero if below a threshold to avoid jittering.
                self.dx = 0
            elif self.dx > 0:
                self.dx -= self.decelx
            elif self.dx < 0:
                self.dx += self.decelx
        if not (keys[pygame.K_w] or keys[pygame.K_s]):
            if(-self.accely < self.dy < self.accely):
                self.dy = 0
            elif self.dy > 0:
                self.dy -= self.decely
            elif self.dy < 0:
                self.dy += self.decely
        
        #Trim values down to max speed.
        #else statements avoid unnecessary checks.
        if self.dx > self.maxdx:
            self.dx = self.maxdx
        elif self.dx < -self.maxdx:
            self.dx = -self.maxdx
        if self.dy > self.maxdy:
            self.dy = self.maxdy
        elif self.dy < -self.maxdy:
            self.dy = -self.maxdy

        #change position according to velocity values if the new position is within the screen.
        newpos = self.rect.move(self.dx, 0)
        if self.area.contains(newpos):
            self.x += self.dx
        newpos = self.rect.move(0, self.dy)
        if self.area.contains(newpos):
            self.y += self.dy

        #rect should always be at x,y (undoes the move above if movement failed).
        self.rect.x = self.x
        self.rect.y = self.y

        #Use the physics engine to handle collisions and gravity
        #We could end up using this method elsewhere
        #And it cleans up the code a bit.
        physics.handle_collisions(self)
        physics.gravity(self, 7, 500)



    #draw method draws the player to the screen
    #Method needs a reference to the game screen to function
    #The convert method simply speeds up the blitting process
    def draw(self, display):
        display.blit(self.image, (self.x, self.y))
        
    #Getters
    def getX(self):
        return self.x

    def getY(self):
        return self.y

<<<<<<< HEAD
    def getH():
        return self.health
=======
    def setY(self, amount):
        self.y += amount
>>>>>>> origin/master

    def setX(self, amount):
        self.x += amount