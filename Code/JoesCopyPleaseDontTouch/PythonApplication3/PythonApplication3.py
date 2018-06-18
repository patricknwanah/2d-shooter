import pygame
import random

# Global constants

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
 
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
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
            # Stop our vertical movement
            self.change_y = 0
 
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .55
 
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
            self.change_y = -10
 
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
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

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
        numGen1 = random.randint(3,3)
        numGen2 = random.randint(3,3)

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
 
 
def main():
    """ Main Program """
    pygame.init()
 
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("Joe's Copy Test")
 
    # Create player

    player = Player()
 
    # Create all the levels
    level_list = []
    level_list.append( Level_01(player) )
 
    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]
 
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
 
    player.rect.x = 0
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)
 
    # Loop until the user clicks the close button.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
 
    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()


        #Apply test cases

        #This code tests the players x and y coordinates in relation to various platforms
        block_hit_list = pygame.sprite.spritecollide(player, player.level.platform_list, False)
        for block in block_hit_list:

            if player.change_x > 0:

                print("Player right X assertion = "),
                assert(player.rect.right == block.rect.left)

            elif player.change_x < 0:

                print("Player left X assertion = "),
                assert(player.rect.left == block.rect.right)

        # Update the player.
        active_sprite_list.update()
 
        # Update items in the level
        current_level.update()
 
        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right >= 500:
            diff = player.rect.right - 500
            player.rect.right = 500
            current_level.shift_level(-diff)
 
        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left < 0:
            player.rect.left = 0
 
        # Draw everything
        current_level.draw(screen)
        active_sprite_list.draw(screen)
        
         
        # Limit to 60 frames per second
        clock.tick(60)
 
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    pygame.quit()
 
if __name__ == "__main__":
    main()