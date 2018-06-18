import pygame
import random
import time
import threading

from Title_Screen import *
from class1 import *
 
# Global constants
listofmobs = []

# Colors
BLACK = (0,0,0)
WHITE = (255, 255, 255)
GREEN = (0,255,0)
red_c = (255,0,0)
tempspeed = 3.5

 
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


 
 
class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
        controls. """
 
    # -- Methods
    def __init__(self):
        """ Constructor function """
 
        # Call the parent's constructor
        super().__init__()
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        width = 40
        height = 60

        #Direction player is facing. Defaults to Right
        self.direction = "R"
        
        #Get a list of images for animation
        self.left_frames = []
        self.right_frames = []

        #grab all images and add them to their respective lists
        image = pygame.image.load("main_player.png")
        self.right_frames.append(image)
        image = pygame.image.load("main_walk_0.png")
        self.right_frames.append(image)
        image = pygame.image.load("main_walk_1.png")
        self.right_frames.append(image)
        image = pygame.image.load("main_walk_2.png")
        self.right_frames.append(image)
        image = pygame.image.load("main_walk_3.png")
        self.right_frames.append(image)

        #create the right frames by flipping the left frames
        for image in range(len(self.right_frames)):

            image = pygame.transform.flip(self.right_frames[image], True, False)
            self.left_frames.append(image)

        #starting image is the first in left frames
        self.image = self.right_frames[0]
 
        # Set a referance to the image rect.
        self.rect = self.image.get_rect()
 
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
 
        # List of sprites we can bump against
        self.level = None

        #sets health amount
        global health
        health = 30

        #loads the health images
        global health_pics
        health_pics = []
        for i in range(health + 1):
            health_pics.append(pygame.image.load('health' + str(i) + '.png'))

    def setHealth(self, int):
        health = int

    def getHealth():
        return health

    def minusHealth(self, screen, mouse):
    #subtracts 1 health from player
            #if player is hit by enemy
        mouse = pygame.mouse.get_pressed()
        if (mouse[0] == 1):
            #subtracts 1 health from player
            self.setHealth(health-1)
            screen.blit(health_pics[health],(10,10))
          

    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()
 
        # Move left/right
        self.rect.x += self.change_x

        #Grab the players position
        pos = self.rect.x

        #Update the image loaded
        if self.direction == "R":
            frame = (pos // 30) % len(self.right_frames)
            self.image = self.right_frames[frame]
        else:
            frame = (pos // 30) % len(self.left_frames)
            self.image = self.left_frames[frame]

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
              
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
                
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
                assert(self.rect.bottom == block.rect.top)
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
                assert(self.rect.top == self.rect.bottom)
 
            # Stop our vertical movement
            self.change_y = 0
 
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
 
        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
 
    def jump(self):
        """ Called when user hits 'jump' button. """
 
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
 
        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -6

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -4
        self.direction = "L"
 
    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 4
        self.direction = "R"
 
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0
    
    def getX(self):
        return self.x
    
    def gety(self):
        return self.y

#Bullet class is used for firing bullets
class Bullet(pygame.sprite.Sprite):

    #create player reference
    gamePlayer = None

    #Call superclass constructor, will take a player reference
    def __init__(self, player, bullet_list, sprite_list, screen):
        super().__init__()

        #playe reference
        self.player = player

        #x and y coords
        self.x = player.rect.x + 6
        self.y = player.rect.y + 16
        
        if self.player.direction == "R":
            self.vel = 10
        else:
            self.vel = -10

        #create shot image and shot rectangle
        #self.ellipse = pygame.draw.ellipse(screen, GREEN, (self.x, self.y, 2, 2), 1)
        self.image = pygame.Surface([10, 10])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
   
        #add bullets to both groups
        bullet_list.add(self)
        sprite_list.add(self)

    #update will move the bullet
    def update(self):

        self.rect.x += self.vel


class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """
 
    def __init__(self, width, height, integer):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        super().__init__()
 
        if integer == 1:
            self.image = pygame.image.load("crate1.png")
        elif integer == 2:
            self.image = pygame.image.load("crate2.png")
        elif integer == 3:
            self.image = pygame.image.load("crate3.png")
        elif integer == 4:
            self.image = pygame.image.load("cargo1.png")
        elif integer == 5:
            self.image = pygame.image.load("cargo2.png")
        elif integer == 6:
            self.image = pygame.image.load("cargo3.png")
        elif integer == 7:
            self.image = pygame.image.load("cargo4.png")

        self.rect = self.image.get_rect()
 
 
class Level(object):

    world_shift = 0

    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
         
        # Background image
        self.background = pygame.image.load("factory.png").convert()
 
    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()
 
    def draw(self, screen):
        """ Draw everything on this level. """
 
        # Draw the background
        screen.fill(WHITE)

        screen.blit(self.background, (self.world_shift // 3,0))


        #screen.blit(self.background, (0,0))

 

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)

    def shift_level(self, shift_x):
        #scrolls the world

        # Keep track of the shift amount
        self.world_shift += shift_x

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x
        for enemy in listofmobs:
            enemy.rect.x += shift_x
 
# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """
 
    def __init__(self, player):
        """ Create level 1. """
        numGen1 = random.randint(1,3)
        numGen2 = random.randint(1,3)

        # Call the parent constructor
        Level.__init__(self, player)

        self.level_limit = -1000

        self.background = pygame.image.load("factory.png").convert()
        self.background.set_colorkey(WHITE)
 
        # Array with width, height, x, and y of platform
        if numGen1 == 1:
            # Boxes number top to bottom, left to right
            level1 = [
                    [50, 50, 2, 600, 450],# Cargo #1
                    [50, 50, 1, 700, 450],# Cargo #2
                    [300, 100, 4, 500, 500], # Crate #1
                    [50, 50, 1, 450, 550] # Cargo #3
                    ]

        elif numGen1 == 2:
            # Boxes number top to bottom, left to right
            level1 = [[50, 50, 2, 250, 500],# Box #1
                     [50, 50, 1, 350, 500],# Box #2
                     [50, 50, 2, 150, 550],# Box #3
                     [50, 50, 1, 250, 550],# Box #4
                     [50, 50, 2, 300, 550],# Box #5
                     [50, 50, 3, 350, 550],# Box #6
                     [50, 50, 3, 450, 550]# Box #7
                    ]
        elif numGen1 == 3:
            # Boxes number top to bottom, left to right
            level1 = [
                     [50, 50, 2, 600, 450], # Box #1
                     [100, 300, 4, 650, 400],# Cargo #1
                     [50, 50, 1, 250, 550], # Box #2
                     [50, 50, 1, 350, 550], # Box #3
                     [50, 50, 1, 450, 550], # Box #4
                     [100, 300, 5, 500, 500],# Cargo #2
                     [300, 100, 6, 800, 500]
                    ]
        if numGen2 == 1:
            level2 = [
                     [50, 50, 1, 1100, 550],
                     [300, 100, 4, 1150, 500],
                     [300, 100, 6, 1450, 500],
                     [50, 50, 2, 1200, 450],
                     [300, 100, 7, 1250, 400],
                     [50, 50, 3, 1400, 350],
                     [50, 50, 2, 1500, 350], 
                     ]
        elif numGen2 == 2:
            level2 = [
                     [300, 100, 4, 1200, 450],
                     [50, 50, 1, 1125, 500],
                     [50, 50, 2, 1125, 550],
                     [50, 50, 3, 1200, 550],
                     [50, 50, 3, 1325, 550],
                     [50, 50, 3, 1450, 550],
                     [50, 50, 2, 1325, 400]           

                     ]
        elif numGen2 == 3:
            level2 = [
                     [50, 50, 2, 1300, 550],
                     [300, 100, 5, 1350, 500],
                     [50, 50, 3, 1400, 450],
                     [300, 100, 6, 1450, 400],
                     [50, 50, 2, 1800, 450],
                     [300, 100, 4, 1800, 500],
                     [50, 50, 2, 2100, 550]
                     ]
        if numGen2 != 3:
            level3 = [
                     [300,100, 5, 2400, 500],
                     [300,100, 4, 2400, 400],
                     [300,100, 6, 2400, 300],
                     [300,100, 7, 2400, 200],
                     [300,100, 5, 2400, 100],
                     [300,100, 6, 2400, 0],
                     ]
        else:
            level3 = [
                     [300,100, 5, 2700, 500],
                     [300,100, 4, 2700, 400],
                     [300,100, 6, 2700, 300],
                     [300,100, 7, 2700, 200],
                     [300,100, 5, 2700, 100],
                     [300,100, 6, 2700, 0],
                     ]
 
        # Go through the array above and add platforms
        for platform in level1:
            block = Platform(platform[0], platform[1], platform[2])
            block.rect.x = platform[3]
            block.rect.y = platform[4]
            block.player = self.player
            self.platform_list.add(block)
        for platform in level2:
            block = Platform(platform[0], platform[1], platform[2])
            block.rect.x = platform[3]
            block.rect.y = platform[4]
            block.player = self.player
            self.platform_list.add(block)
        for platform in level3:
            block = Platform(platform[0], platform[1], platform[2])
            block.rect.x = platform[3]
            block.rect.y = platform[4]
            block.player = self.player
            self.platform_list.add(block)

    def returnlevel(self):
        return self.levellist

def spawnnew(listofmobs,level_list,current_level,active_sprite_list):
    listofmobs.append(mob())
    listofmobs[-1].rect.x = 200
    listofmobs[-1].rect.y = 0
    level_list.append(Level_01(listofmobs[-1]))
    listofmobs[-1].level = current_level
    active_sprite_list.add(listofmobs[-1])
    threading.Timer(10.0,spawnnew,(listofmobs, level_list,current_level,active_sprite_list)).start()

def spawnmobs(listofmobs, level_list,current_level,active_sprite_list):
    count3 = 0
    for i in range(0,1):
        listofmobs.append(mob())
    for i in listofmobs:
        count3 = count3 + 200
        i.rect.x = 20 + count3
        i.rect.y = 0
        level_list.append(Level_01(i))
        i.level = current_level
        active_sprite_list.add(i)
    #threading.Timer(5.0,spawnmobs,(listofmobs, level_list,current_level,active_sprite_list)).start()

def main():
    
    """ Main Program """
    pygame.init()
 
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("ADAM Test")
 
    # Create player
    #list of mobs
    
    player = Player()
    
    boss1 = boss()
    boss1.rect.y = 0
    boss1.rect.x = 300
 
    
    # Create all the levels
    level_list = []
    #at mob to the level
    
    level_list.append( Level_01(player) )
    
    level_list.append(Level_01(boss1))
 
    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]
 
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
    
    boss1.level = current_level
    #add mobs to level
    

    player.rect.x = 0
    
    player.rect.y = SCREEN_HEIGHT - player.rect.height

    #spawnmobs(listofmobs,level_list,current_level,active_sprite_list)
    
    #add mobs to activity sprite
    

    active_sprite_list.add(player)
    
    active_sprite_list.add(boss1)


    
    #Create the bullet list
    bullet_list = pygame.sprite.Group()
 
    # Loop until the user clicks the close button.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    jumpl = 0
    counter = 0
    intervals = 0
    intervals1 = 0


    #Mouse, used to detect events
    click = pygame.mouse.get_pressed()

    #call title screen
    intro(screen, clock) 


    # -------- Main Program Loop -----------
    spawnmobs(listofmobs,level_list,current_level,active_sprite_list)
    spawnnew(listofmobs,level_list,current_level,active_sprite_list)

    items = current_level.returnlevel()
    shot1 = 'false'
    TimetoKillPlayer = 0
    while not done:
        if TimetoKillPlayer == 15:
                active_sprite_list.remove(TimetoKillPlayer)
                pygame.quit()

        else:       
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pause(screen)
                    if event.key == pygame.K_LEFT:
                        player.go_left()
                    if event.key == pygame.K_RIGHT:
                        player.go_right()
                    if event.key == pygame.K_UP:
                        jumpl = player.rect.x
                        player.jump()

                    #if the space key is hit, fire a shot
                    if event.key == pygame.K_SPACE:
                        bullet = Bullet(player, bullet_list, active_sprite_list, screen)
 
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT and player.change_x < 0:
                        player.stop()
                    if event.key == pygame.K_RIGHT and player.change_x > 0:
                        player.stop()

        
        
            boss1.follow(player,items)
            # Update all sprites
        
            for i in listofmobs:
                i.patrol1(screen,player,jumpl,counter, items, bullet_list, active_sprite_list,screen,shot1)
                if i.movement == 'right':
                    newcor = player.rect.y + 40
                    #set when to start shoting
                    if player.rect.x in range(i.rect.x-30, i.rect.x + 400) and (player.rect.y in range(i.rect.y-40, i.rect.y + 140) or newcor in range(i.rect.y-60, i.rect.y + 140)):
                        intervals += 1
                        #every 2 seconds shot
                        if intervals % 60 == 0 and intervals == 120:
                            intervals = 0
                            #print(intervals)
                            bullet1 = Bullet(i, bullet_list, active_sprite_list, screen)
                            for bullet1 in bullet_list:

                                #see if a bullet hits a platform
                                block_hit_list = pygame.sprite.spritecollide(bullet1, i.level.platform_list, False)
                                for block in block_hit_list:

                                    #update both lists
                                    bullet_list.remove(bullet1)
                                    active_sprite_list.remove(bullet1)

                                if bullet1.rect.x < 0 or bullet1.rect.x > SCREEN_WIDTH + 1:
                                    bullet_list.remove(bullet1)
                                    active_sprite_list.remove(bullet1)
                                if bullet1.rect.x in range(player.rect.x-10, player.rect.x+10) and bullet1.rect.y in range(player.rect.y,player.rect.y+50):
                                    bullet_list.remove(bullet1)
                                    active_sprite_list.remove(bullet1)
                                    TimetoKillPlayer += 1
                                    print(TimetoKillPlayer)
                        
                                                        
                elif i.movement == 'left':
                    #set when to start shoting
                    if player.rect.x in range(i.rect.x - 400, i.rect.x+30) and (player.rect.y in range(i.rect.y-40, i.rect.y + 130) or newcor in range(i.rect.y-60, i.rect.y + 140)):
                        intervals1 += 1
                        #every 2 seconds shot
                        if intervals1 % 60 == 0 and intervals1 == 120:
                            intervals1 = 0
                            bullet1 = Bullet(i, bullet_list, active_sprite_list, screen)
                            for bullet1 in bullet_list:

                                #see if a bullet hits a platform
                                block_hit_list = pygame.sprite.spritecollide(bullet1, i.level.platform_list, False)
                                for block in block_hit_list:

                                    #update both lists
                                    bullet_list.remove(bullet1)
                                    active_sprite_list.remove(bullet1)

                                if bullet1.rect.x < 0 or bullet1.rect.x > SCREEN_WIDTH + 1:
                                    bullet_list.remove(bullet1)
                                    active_sprite_list.remove(bullet1)
                                if bullet1.rect.x in range(player.rect.x-10, player.rect.x+10) and bullet1.rect.y in range(player.rect.y,player.rect.y+50):
                                    bullet_list.remove(bullet1)
                                    active_sprite_list.remove(bullet1)
                                    TimetoKillPlayer += 1
                                    print(TimetoKillPlayer)
                            
            
        
            active_sprite_list.update()

        
            current_level.update()
 
            # If the player gets near the right side, shift the world left (-x)
            if player.rect.right >= 500:
                diff = player.rect.right - 500
                player.rect.right = 500
                current_level.shift_level(-diff)
 
            # If the player gets near the left side, shift the world right (+x)
            if player.rect.left < 0:
                player.rect.left = 0

        

            #calculate bullet mechanics
            for bullet in bullet_list:

                #see if a bullet hits a platform
                block_hit_list = pygame.sprite.spritecollide(bullet, player.level.platform_list, False)
                for block in block_hit_list:

                    #update both lists
                    bullet_list.remove(bullet)
                    active_sprite_list.remove(bullet)

                if bullet.rect.x < 0 or bullet.rect.x > SCREEN_WIDTH + 1:
                    bullet_list.remove(bullet)
                    active_sprite_list.remove(bullet)
                for i in listofmobs:
                    if bullet.rect.x in range(i.rect.x,i.rect.x+40) and bullet.rect.y in range(i.rect.y,i.rect.y+50):
                       bullet_list.remove(bullet)
                       active_sprite_list.remove(bullet)
                       active_sprite_list.remove(i)
                       #level_list.remove(i)
                       listofmobs.remove(i) 
            
            
 
            # Update items in the level
            current_level.update()
 
            # If the player gets near the right side, shift the world left (-x)
            if player.rect.right > SCREEN_WIDTH:
                player.rect.right = SCREEN_WIDTH
 
            # If the player gets near the left side, shift the world right (+x)
            if player.rect.left < 0:
                player.rect.left = 0
 


            # Draw everything
            current_level.draw(screen)
            active_sprite_list.draw(screen)
            screen.blit(health_pics[health], (10,10))
            #listofmobs[0].sight(screen)
            #minusHealth(player, screen)
            #Minus Health
            #player.minusHealth(screen, click)
 
            # Limit to 60 frames per second
            clock.tick(60)
 
            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
            #pygame.display.update()
        


    pygame.quit()
 
if __name__ == "__main__":
    main()