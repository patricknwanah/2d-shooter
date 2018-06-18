import pygame, time

pygame.init()

#define width and height for the screen
display_width = 800
display_height = 600

#generate color
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

#set window, display title, and create clock
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Robots of Destruction')
clock = pygame.time.Clock()

#create image variable, and object variable
robotImg = pygame.image.load('robot2.png')
def robot(x, y):
    gameDisplay.blit(robotImg, (x, y))

#define the robots start
x = (display_width * 0.3)
y = (display_height * 0.4)

#Game loop variable
crashed = False

#Game loop
while not crashed:

    #variables for the change of position in x or y
    x_change = 0
    y_change = 0

    #Event handler
    for event in pygame.event.get():

        #handle the game quitting
        if event.type == pygame.QUIT:
            crashed = True

        #key handler
        key = pygame.key.get_pressed()
        pygame.mouse.set_visible = False

        if key[pygame.K_a]:
            x_change = -5
        if key[pygame.K_d]:
            x_change = 5
        if key[pygame.K_s]:
            y_change = 5
        if key[pygame.K_SPACE]:
            y_change = -50

    #Logic Loop
    if y < 450:

        #set the change in y, and add it to the y variable
        y_change = 10
        y += y_change
        time.sleep(.025)




    #update variables
    x += x_change
    y += y_change

    #Fill screen, draw robot, update clock
    gameDisplay.fill(white)
    robot(x, y)
    pygame.display.update()
    clock.tick(60)

#quit out of pygame
pygame.quit()
quit()




