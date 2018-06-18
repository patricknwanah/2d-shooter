import pygame
from Player_Assets import *

#Create group for physical entities
entities = pygame.sprite.Group()

#Physical Entities will be created and added to a group.
#This will make it so the Physics_Engine acts on a cluster of objects.
class Physical_Entity(pygame.sprite.Sprite):

    #init method will initialize a physical entity
    #It will store the objects x and y position to use later
    def __init__(self, p_object):

        #Call superclass constructor, with a reference to the entities group
        #Physical objects will automatically be stored in the group
        pygame.sprite.Sprite.__init__(self, entities)

        #init other attributes
        self.p_object = p_object
        self.x = p_object.getX()
        self.y = p_object.getY()

        #In order to handle collisions we need access to the entities rect attribute
        self.rect = p_object.rect
        self.rect.x = p_object.rect.x
        self.rect.y = p_object.rect.y
        self.area = p_object.area

    #Getters for the class
    def getY(self):
        return self.y

    def getX(self):
        return self.x

    #Setters for the class
    def setY(self, y_change):
        self.y += y_change

    def setY(self, x_change):
        self.x += x_change

class Engine(object):

    #init function
    #Takes the fall speed of gravity, and a player/AI object
    #We will nedd the moving objects position in space
    def __init__(self):
        self.clock = pygame.time.Clock()

    #gravity function will take a physical entity and translate its y_coordinate
    def gravity(self, character, fall_speed, maxY):

        #if the characters Y value is less than the max Y, proceed
        if character.getY() < maxY:
            character.setY(fall_speed)

    #Collide dictates what happens when two characters hit each other
    def collideLeft(self, p_object1, p_object2):

        #Handle collision of two objects
        if pygame.sprite.collide_rect(p_object1, p_object2):

            #move the first object to the left
            p_object1.move_left(20)

    #Function to handle collisions
    #Figured to put this in a function to use later.
    def handle_collisions(self, player):

        #Determine if the player has collided with anything
        #For each object in the list, determine if the player made contact
        hit_list = pygame.sprite.spritecollide(player, player.collide_list, False)
        for object in hit_list:

            #Handle moves to the right or left
            if player.dx > 0:
                player.dx = 0
                player.rect.right = object.rect.left
            else:
                player.dx = 0
                player.rect.left = object.rect.right

        #Determine if the player collides with anything
        hit_list = pygame.sprite.spritecollide(player, player.collide_list, False)
        for object in hit_list:
 
            if player.dy > 0:
                player.dy = 0
                self.rect.top = object.rect.bottom
            else:
                player.dy = 0
                player.rect.bottom = object.rect.top


#Block class for standard physical objects
class Block(pygame.sprite.Sprite):
    
    #init method
    def __init__(self, x, y, width, height):

        #Call super class constructor
        super().__init__()

        #set object attributes
        self.x = x
        self.y = y
        
        #create image
        self.image = pygame.Surface([width, height])
        self.image.fill((255, 255, 255))

        #Create rect
        self.rect = self.image.get_rect()
        self.rect.y = self.y
        self.rect.x = self.x

    #Draw method for this class blits the object to the screen
    def draw(self, gameDisplay):
        gameDisplay.blit(self.image, (self.x, self.y))