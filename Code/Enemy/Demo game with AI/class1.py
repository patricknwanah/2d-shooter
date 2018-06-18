import pygame, math


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
red_c = (255,0,0)


class boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        height = 60
        self.movement = 'right'

        #Direction player is facing. Defaults to Right
        self.direction = "R"
        
        self.health = 100
        self.alive = True
        
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
    def update(self):
        
        if self.health <= 0:
            self.alive = false
        self.calc_grav()
        # Move left/right
        self.rect.x += self.change_x

        #Grab the players position
        pos = self.rect.x

        #Update the image loaded
        if self.direction == "L":
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
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .49
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
    def moveleft(self):       
        if self.rect.left < 0:
            self.rect.left = 0          
        else:
            self.change_x = -1.5
            self.direction = 'L'
    def moveright(self):
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH       
        else:

            self.change_x = 1.5
            self.direction = 'R'
    def movedown(self):
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = SCREEN_HEIGHT
        else:
            self.change_y = 1.5
    def moveup(self):
        if self.rect.y < 0:
            self.rect.y = 0
        else:
            self.change_y = -1.5
    def jump(self):
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10
    def follow(self, player,items):
        #right up
        if(player.rect.x > self.rect.x and player.rect.y < self.rect.y):
            self.moveright()
            self.moveup()
        #right
        elif(player.rect.x > self.rect.x and player.rect.y == self.rect.y):
            self.moveright()
        #right down
        elif(player.rect.x > self.rect.x and player.rect.y > self.rect.y):
            self.moveright()
            self.movedown()
        #down          
        elif(player.rect.x == self.rect.x and player.rect.y > self.rect.y):
            self.movedown()
        #up
        elif(player.rect.x == self.rect.x and player.rect.y < self.rect.y):
            self.moveup()
        #left up
        elif(player.rect.x < self.rect.x and player.rect.y < self.rect.y):
            self.moveleft()
            self.moveup()
        #left
        elif(player.rect.x < self.rect.x and player.rect.y == self.rect.y):
            self.moveleft()
        #left down
        elif(player.rect.x < self.rect.x and player.rect.y > self.rect.y):
            self.moveleft()
            self.movedown()
        


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

    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()
 
        # Move left/right
        self.rect.x += self.change_x

        #Grab the players position
        pos = self.rect.x

        #Update the image loaded
        if self.direction == "L":
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
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .49
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
            self.change_x = -2
            self.direction = 'L'
    def moveright(self):
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH       
        else:
            self.change_x = 2
            self.direction = 'R'
    

    def stop(self):
        self.change_x = 0
           
              
    def sight(self, gameDisplay):
        #pygame.draw.rect(screen, color, (x,y,width,height), thickness)     
        pygame.draw.rect(gameDisplay, red_c, (self.rect.x-30, self.rect.y-40, 200, 100), 0)

    def sight2(self, gameDisplay):
        #pygame.draw.rect(screen, color, (x,y,width,height), thickness)
        pygame.draw.rect(gameDisplay, red_c, (self.rect.x+30, self.rect.y-40, -200, 100), 0)

        
    def follow1(self, player, jumpl, counter, items):
        #left down check
        if self.rect.x > player.rect.x and self.rect.y < player.rect.y:
             if self.rect.x in range(player.rect.x - 13,player.rect.x + 13):
                self.stop()
             else:
                self.movement = 'left'
                self.moveleft()
                self.direction = 'L'
                if self.rect.x in range(player.rect.x - 10, player.rect.x) or self.rect.x in range(player.rect.x - 13,player.rect.x + 13):
                    self.stop()   
                else:          
                    for i in items:
                        if (self.rect.x in range(i[3],i[3]+55) or (self.rect.x in range(jumpl-15, jumpl) and jumpl != 0)) and self.rect.x not in range(player.rect.x-15,player.rect.x + 15):
                            self.jump()  
        #right down
        elif self.rect.x < player.rect.x and self.rect.y < player.rect.y:
            if self.rect.x in range(player.rect.x - 10, player.rect.x) or self.rect.x in range(player.rect.x - 13 ,player.rect.x + 13):
                self.stop()
            else:
                self.movement = 'right'
                self.moveright()
                self.direction = 'R'
                

        # left up check
        elif self.rect.x > player.rect.x and self.rect.y > player.rect.y:
            if self.rect.x in range(player.rect.x - 10, player.rect.x) or self.rect.x in range(player.rect.x - 15,player.rect.x + 15):
                self.stop()
            else:
                self.movement = 'left'
                self.moveleft()
                self.direction = 'L' 
                if self.rect.x in range(player.rect.x - 10, player.rect.x) or self.rect.x in range(player.rect.x - 15,player.rect.x + 15):
                    self.stop()   
                else:          
                    for i in items:
                        if (self.rect.x in range(i[3],i[3]+55) or (self.rect.x in range(jumpl-15, jumpl) and jumpl != 0)) and self.rect.x not in range(player.rect.x-15,player.rect.x + 15):
                            self.jump()                           
                           
        #move right up
        elif self.rect.x < player.rect.x and self.rect.y > player.rect.y:
            if self.rect.x in range(player.rect.x - 10, player.rect.x) or self.rect.x in range(player.rect.x-15,player.rect.x + 15):
                self.stop()
            else :
                self.movement = 'right'
                self.moveright()
                self.direction = 'R'
                if self.rect.x in range(player.rect.x - 15, player.rect.x) or self.rect.x in range(player.rect.x-15,player.rect.x + 15):
                    self.stop()  
                else:                                 
                    for i in items:
                        if (self.rect.x in range(i[3]-40,i[3]) or (self.rect.x in range(jumpl - 15,jumpl) and jumpl != 0)) and self.rect.x not in range(player.rect.x-15,player.rect.x + 15):
                            self.jump()
                        
        elif self.rect.x > player.rect.x:
            if self.rect.x in range(player.rect.x - 10, player.rect.x) or self.rect.x in range(player.rect.x-15,player.rect.x + 15):
                self.stop()
            else:
                self.movement = 'left'
                self.moveleft()
                self.direction = 'L'   
                if self.rect.x in range(player.rect.x - 10, player.rect.x) or self.rect.x in range(player.rect.x-15,player.rect.x + 15):
                    self.stop()    
                else:           
                    for i in items:
                        if (self.rect.x in range(i[3],i[3]+55) or (self.rect.x in range(jumpl-15, jumpl) and jumpl != 0)) and self.rect.x not in range(player.rect.x-15,player.rect.x + 15):
                            self.jump()                       
        elif self.rect.x < player.rect.x:
            self.movement = 'right'
            if self.rect.x in range(player.rect.x - 10, player.rect.x) or self.rect.x in range(player.rect.x-15,player.rect.x + 15):
                self.stop()
            else :
                self.movement = 'right'
                self.moveright()
                self.direction = 'R'    
                if self.rect.x in range(player.rect.x - 10, player.rect.x) or self.rect.x in range(player.rect.x-10,player.rect.x + 10):
                    self.stop()   
                else:                            
                    for i in items:
                        if (self.rect.x in range(i[3]-40,i[3]) or (self.rect.x in range(jumpl - 15,jumpl) and jumpl != 0)) and self.rect.x not in range(player.rect.x-15,player.rect.x + 15):
                            self.jump()
                               
        elif self.rect.x in range(player.rect.x - 10, player.rect.x) or self.rect.x in range(player.rect.x-15,player.rect.x + 15):
                self.stop()
     
        
    def patrol1(self,gameDisplay,player,jumpl,counter,items):  
        if self.movement == 'right':
            newcor = player.rect.y + 40
            if player.rect.x in range(self.rect.x-30, self.rect.x + 201) and (player.rect.y in range(self.rect.y-40, self.rect.y + 140) or newcor in range(self.rect.y-60, self.rect.y + 140)):
                self.follow1(player,jumpl,counter,items)  
               
            elif self.rect.x <= 600:
                self.moveright()
                self.direction = 'R'
                for i in items:
                    if self.rect.x in range(i[3]-40,i[3]) and self.rect.x not in range(player.rect.x-15,player.rect.x + 15):
                        self.jump()
            else:
                self.movement = 'left'
        elif self.movement == 'left':
            newcor = player.rect.y + 40
            if player.rect.x in range(self.rect.x - 201, self.rect.x+30) and (player.rect.y in range(self.rect.y-40, self.rect.y + 130) or newcor in range(self.rect.y-60, self.rect.y + 140)):
                self.follow1(player,jumpl, counter,items)
                
            elif self.rect.x != 0:
                self.moveleft()
                self.direction = 'L'
                for i in items:                                  
                    if self.rect.x in range(i[3],i[3]+55) and self.rect.x not in range(player.rect.x-15,player.rect.x + 15):                 
                        self.jump()
                        self.moveleft()
                        self.direction = 'L'
            if self.rect.x == 0:
                self.movement = 'right'

            
        
