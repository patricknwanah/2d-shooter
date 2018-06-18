import pygame
import random

from Title_Screen import *
 
# Global constants
 
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
        
        self.distance = 0 #Total distance traveled, used to determine which frame to display.

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
          

    def update(self, level):
        """ Move the player. """
        # Gravity
        self.calc_grav()
 
        # Move left/right
        self.rect.x += self.change_x

        #Grab the players position
        pos = self.rect.x
        
        self.distance += abs(self.change_x)

        #Update the image loaded
        if self.direction == "R":
            frame = (self.distance // 30) % len(self.right_frames)
            self.image = self.right_frames[frame]
        else:
            frame = (self.distance // 30) % len(self.left_frames)
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
        self.change_x = -6
        self.direction = "L"
 
    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6
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
            self.vel = 6
        else:
            self.vel = -6

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

 
class mob(pygame.sprite.Sprite):
    """description of class"""
    def __init__(self):
        super().__init__()
       # Call the parent's constructor
        
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        width = 40
        height = 60
        self.movement = 'right'

        #Direction player is facing. Defaults to Right
        self.direction = "R"
        
        #Get a list of images for animation
        self.left_frames = []
        self.right_frames = []

        #grab all images and add them to their respective lists
        image = pygame.image.load("enemy_stand.png")
        self.left_frames.append(image)
        image = pygame.image.load("enemy_walk_0.png")
        self.left_frames.append(image)
        image = pygame.image.load("enemy_walk_1.png")
        self.left_frames.append(image)
        image = pygame.image.load("enemy_walk_2.png")
        self.left_frames.append(image)
        image = pygame.image.load("enemy_walk_3.png")
        self.left_frames.append(image)

        #create the right frames by flipping the left frames
        for image in range(len(self.left_frames)):

            image = pygame.transform.flip(self.left_frames[image], True, False)
            self.right_frames.append(image)

        #starting image is the first in left frames
        self.image = self.left_frames[0]
 
        # Set a referance to the image rect.
        self.rect = self.image.get_rect()
 
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
 
        # List of sprites we can bump against
        self.level = None

    def update(self, level):
        """ Move the player. """
        # Gravity
        self.calc_grav()
 
        # Move left/right
        self.rect.x += self.change_x

        #Grab the players position
        pos = self.rect.x

        #Update the image loaded
        if self.direction == "R":
            frame = ((pos - level.level[0][3]) // 30) % len(self.right_frames)
            self.image = self.right_frames[frame]
        else:
            frame = ((pos - level.level[0][3]) // 30) % len(self.left_frames)
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
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
            # Stop our vertical movement
            self.change_y = 0

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .50
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
    def jump(self):
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10
    def moveleft(self):       
        if self.rect.left < 0:
            self.rect.left = 0          
        else:
            self.change_x = -3
            self.direction = 'L'
    def moveright(self):
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH       
        else:

            self.change_x = 3
            self.direction = 'R'

    def stop(self):
        self.change_x = 0
    def spawn(self,display):
        display.blit(self.image,(self.rect.x,self.rect.y))
           
              
    def sight(self, gameDisplay):
        #pygame.draw.rect(screen, color, (x,y,width,height), thickness)     
        pygame.draw.rect(gameDisplay, red_c, (self.rect.x+30, self.rect.y, 200, 100), 0)

    def sight2(self, gameDisplay):
        #pygame.draw.rect(screen, color, (x,y,width,height), thickness)
        pygame.draw.rect(gameDisplay, red_c, (self.rect.x, self.rect.y, -200, 100), 0)
    def newf(self,player,counter,jumpl,locationloop):
        print(counter)
        print(locationloop)
        counter += 1
    def follow1(self, player, jumpl, counter, items):
        if self.rect.x > player.rect.x and self.rect.y > player.rect.y:
            if self.rect.x in range(player.rect.x - 10, player.rect.x) or self.rect.x in range(player.rect.x,player.rect.x + 10):
                self.stop()
            else:
                self.moveleft()
                self.direction = 'L'              
                for i in items:
                    if self.rect.x in range(i[3],i[3]+55) or (self.rect.x in range(jumpl-15, jumpl) and jumpl != 0):
                        self.jump()
                        self.moveleft()
                        self.direction = 'L'
                        print('Jump left now girl!!!')
        if self.rect.x < player.rect.x and self.rect.y > player.rect.y:
            self.movement = 'right'
            if self.rect.x in range(player.rect.x - 10, player.rect.x) or self.rect.x in range(player.rect.x,player.rect.x + 10):
                self.stop()
            else :
                self.moveright()
                self.direction = 'R'                                   
                for i in items:
                    if self.rect.x in range(i[3]-40,i[3]) or (self.rect.x in range(jumpl - 15,jumpl) and jumpl != 0):
                        self.jump()
                        print('jump right now girl!!')
        if self.rect.x > player.rect.x:
            self.movement = 'left'
            if self.rect.x in range(player.rect.x - 10, player.rect.x) or self.rect.x in range(player.rect.x,player.rect.x + 10):
                self.stop()
            else:
                self.moveleft()
                self.direction = 'L'              
                for i in items:
                    if self.rect.x in range(i[3],i[3]+55) or (self.rect.x in range(jumpl-15, jumpl) and jumpl != 0):
                        self.jump()
                        self.moveleft()
                        self.direction = 'L'
        elif self.rect.x < player.rect.x:
            self.movement = 'right'
            if self.rect.x in range(player.rect.x - 10, player.rect.x) or self.rect.x in range(player.rect.x,player.rect.x + 10):
                self.stop()
            else :
                self.moveright()
                self.direction = 'R'                                   
                for i in items:
                    if self.rect.x in range(i[3]-40,i[3]) or (self.rect.x in range(jumpl - 15,jumpl) and jumpl != 0):
                        self.jump()
                               
        elif self.rect.x in range(player.rect.x - 10, player.rect.x) or self.rect.x in range(player.rect.x,player.rect.x + 10):
                self.stop()
     
        
    def patrol1(self,gameDisplay,player,jumpl,counter,items):  
        if self.movement == 'right':
            newcor = player.rect.y + 34
            if player.rect.x in range(self.rect.x, self.rect.x + 201) and (player.rect.y in range(self.rect.y, self.rect.y + 100) or newcor in range(self.rect.y, self.rect.y + 100)):
                self.follow1(player,jumpl,counter,items)  
                #print('Following '+ str(self.rect.x))
            elif self.rect.x <= 600:
                self.moveright()
                self.direction = 'R'
                for i in items:
                    if self.rect.x in range(i[3]-40,i[3]):
                        self.jump()
            else:
                self.movement = 'left'
        elif self.movement == 'left':
            newcor = player.rect.y + 34
            if player.rect.x in range(self.rect.x - 201, self.rect.x) and (player.rect.y in range(self.rect.y, self.rect.y + 100) or newcor in range(self.rect.y, self.rect.y + 100)):
                self.follow1(player,jumpl, counter,items)
                #print('Left Following: ' + str(self.rect.x))
            elif self.rect.x != 0:
                self.moveleft()
                self.direction = 'L'
                for i in items:                                  
                    if self.rect.x in range(i[3],i[3]+55):
                        print('Moveleft')  
                        print('Jump left here')
                        self.jump()
                        self.moveleft()
                        self.direction = 'L'
            if self.rect.x == 0:
                self.movement = 'right'

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
 
# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """
 
    def __init__(self, player):
        """ Create level 1. """
        numGen = random.randint(1,3)


        # Call the parent constructor
        Level.__init__(self, player)

        self.level_limit = -1000

        self.background = pygame.image.load("factory.png").convert()
        self.background.set_colorkey(WHITE)
        self.level = 0
 
        # Array with width, height, x, and y of platform
        if numGen == 1:
            # Boxes number top to bottom, left to right
            self.level = [
                    [50, 50, 2, 600, 450],# Cargo #1
                    [50, 50, 1, 700, 450],# Cargo #2
                    [300, 100, 4, 500, 500], # Crate #1
                    [50, 50, 1, 450, 550] # Cargo #3
                    ]

        elif numGen == 2:
            # Boxes number top to bottom, left to right
            self.level = [[50, 50, 2, 250, 500],# Box #1
                     [50, 50, 1, 350, 500],# Box #2
                     [50, 50, 2, 150, 550],# Box #3
                     [50, 50, 1, 250, 550],# Box #4
                     [50, 50, 2, 300, 550],# Box #5
                     [50, 50, 3, 350, 550],# Box #6
                     [50, 50, 3, 450, 550]# Box #7
                    ]

        elif numGen == 3:
            # Boxes number top to bottom, left to right
            self.level = [
                     [50, 50, 2, 600, 450], # Box #1
                     [100, 300, 4, 650, 400],# Cargo #1
                     [50, 50, 1, 250, 550], # Box #2
                     [50, 50, 1, 350, 550], # Box #3
                     [50, 50, 1, 450, 550], # Box #4
                     [100, 300, 5, 500, 500]# Cargo #2
                    ]
 
        # Go through the array above and add platforms
        for platform in self.level:
            block = Platform(platform[0], platform[1], platform[2])
            block.rect.x = platform[3]
            block.rect.y = platform[4]
            block.player = self.player
            self.platform_list.add(block)
 
 
def main():
    """ Main Program """
    pygame.init()
 
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("ADAM Test")
 
    # Create player
    player = Player()
 
    # Create all the levels
    level_list = []
    level_list.append( Level_01(player) )
 
    background = pygame.image.load("factory.png").convert()

    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]
 
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
 
    player.rect.x = 0
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)

 
    #Create the bullet list
    bullet_list = pygame.sprite.Group()
 
    # Loop until the user clicks the close button.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    #Mouse, used to detect events
    click = pygame.mouse.get_pressed()

    #call title screen
    intro(screen, clock) 

    # -------- Main Program Loop -----------
    while not done:
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
                    player.jump()

                #if the space key is hit, fire a shot
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(player, bullet_list, active_sprite_list, screen)
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()


        # Update all sprites
        active_sprite_list.update(current_level)
        
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
        
        #prints score which is a function within Title_Screen
        #Score will handle adding score
        Score(screen,SCREEN_WIDTH, SCREEN_HEIGHT)

         
        # Limit to 60 frames per second
        clock.tick(60)
 
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
        #pygame.display.update()

    pygame.quit()
 
if __name__ == "__main__":
    main()
