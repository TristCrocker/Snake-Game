import pygame
import random

pygame.init()
pygame.font.init()

win = pygame.display.set_mode((500,500))
pygame.display.set_caption("Snake Game")
#creating font object
myfont = pygame.font.SysFont("Comic Sans MS", 25)
#Load startwindow bg
startBG = pygame.image.load('Startwindowbg.jpg')
startcolor = (0,100,0)
quitcolor = (0,100,0)
class snake():
    
    def __init__(self, width, height, vel):
        self.x = 60
        self.y = 60
        self.width = width
        self.height = height
        self.vel = vel
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.rightpress = False
        self.leftpress = False
        self.downpress = False
        self.uppress = False
        self.blockpositions = [(self.x, self.y, self.width, self.height)]
        self.extrablocks = 0
        self.direction = ""
 
        
    
    def checkmovement(self):
        #All class methods must have self
        #self makes the variable specific to the class, dont use self if the variable is from outside the class.
        #use global to ensure the variable remains changed globally ie outside the class

        #CHECK MOVEMENT BELOW
        keys = pygame.key.get_pressed()
        #get keys which have been pressed and load into list keys
        if keys[pygame.K_RIGHT]:
            self.rightpress = True
            self.leftpress = False
            self.uppress = False
            self.downpress = False
            self.direction = "right"
        if keys[pygame.K_LEFT]:
            self.leftpress = True
            self.rightpress = False
            self.uppress = False
            self.downpress = False
            self.direction = "left"
        if keys[pygame.K_DOWN]:
            self.downpress = True
            self.leftpress = False
            self.uppress = False
            self.rightpress = False
            self.direction = "down"
        if keys[pygame.K_UP]:
            self.uppress = True
            self.leftpress = False
            self.rightpress = False
            self.downpress = False
            self.direction = "up"

        #MOVEMENT BELOW
        if self.rightpress and (self.x < 480):
        #Must use 450 not 500 to compensate for width of container
        #continous movement of container until edge
            #Change all positions to point to poisiton in front (Except head position)
            for pos in range(len(self.blockpositions) - 1, 0, -1):
                self.blockpositions[pos] = self.blockpositions[pos - 1] 
            
            self.x += self.vel
            self.blockpositions[0] = (self.x, self.y, self.width, self.height)

        if self.leftpress and (self.x > 0):
            for pos in range(len(self.blockpositions) - 1, 0, -1):  
                self.blockpositions[pos] = self.blockpositions[pos - 1] 

            self.x -= self.vel  
            self.blockpositions[0] = (self.x, self.y, self.width, self.height)
         
        if self.downpress and (self.y < 480):
            for pos in range(len(self.blockpositions) - 1, 0, -1):
                self.blockpositions[pos] = self.blockpositions[pos - 1] 

            self.y += self.vel 
            self.blockpositions[0] = (self.x, self.y, self.width, self.height)
      
        if self.uppress and (self.y > 0):
            for pos in range(len(self.blockpositions) - 1, 0, -1):
                self.blockpositions[pos] = self.blockpositions[pos - 1] 

            self.y -= self.vel
            self.blockpositions[0] = (self.x, self.y, self.width, self.height)

        #update hitbox to ensure it moves with box (As values in hitbox have been changed)
        self.hitbox = (self.x, self.y, self.width, self.height)

    def checkdeath(self):
        #Must use global so no new instance of run is created ie run will remain changed outside function
        global run
        #CHECK IF DEAD (HIT WALL OR BITE TAIL)
        if (self.x == 480 or self.x == 0) or (self.y == 480 or self.y == 0):
            run = False
    
    def drawsnake(self):
        #Drawing snake
        win.fill((0,0,0)) 
        #Draw hitbox with character to ensure it moves with character
        pygame.draw.rect(win, (0,0,255), (self.hitbox), 4)
        
        #Draws the extra length when food eaten (From the blockpositions list)
        for i in range(len(self.blockpositions)):
            pygame.draw.rect(win, (255, 0, 0), self.blockpositions[i])
            pygame.draw.rect(win, (0,0,255), (self.hitbox), 4)
     

class food():
        
    def __init__(self, width, height):
        self.x = 50
        self.y = 50
        self.width = width
        self.height = height
        self.eaten = True
        self.hitbox = (self.x, self.y, self.width, self.height)

    def eat(self):
        #CHECK IF FOOD EATEN
        if self.eaten == True:
            self.x = random.randint(2,500)
            self.y = random.randint(2,500)
            self.eaten = False
            self.hitbox = (self.x, self.y, self.width, self.height)
    
    def drawfood(self):
        #Drawing Food
        #Draw hitbox with food to ensure it moves with food
        pygame.draw.rect(win, (0,0,255), (self.hitbox), 8)
        pygame.draw.rect(win, (255, 0, 255), (self.x, self.y, self.width, self.height))
        
#Declare sprites
anaconda = snake(20, 20, 20)
mouse = food(30, 30)
clock = pygame.time.Clock()

def drawgamewindow():
    anaconda.drawsnake()
    mouse.drawfood()
    pygame.display.update()

def drawstartwindow():

    win.fill((0,0,0))
    win.blit(startBG, (0,0))
    startsurface = myfont.render('Start', True, startcolor)
    win.blit(startsurface,(50,200))
    
    quitsurface = myfont.render('Quit', True, quitcolor)
    win.blit(quitsurface,(360,200))
    pygame.display.update()

run = True
startwindow = True

#MAINLOOP
while run:
    clock.tick(20)

    #STARTWINDOW LOOP
    while startwindow and run:

        #Get event from queue and load into var event, then check if a specific event has occured (Use event to check if events occured)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = pygame.quit()
        drawstartwindow()

        mousepos = pygame.mouse.get_pos()
        #Change color of startbutton when hovering
        if (mousepos[0] >= 50 and mousepos[0] <= 116) and (mousepos[1] >= 200 and mousepos[1] <= 235):
            startcolor = (0,200,0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                startwindow = False
                
        else:
            startcolor = (0, 100, 0)

        if (mousepos[0] >= 360 and mousepos[0] <= 426) and (mousepos[1] >= 200 and mousepos[1] <= 235):
            quitcolor = (0,200,0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit()
        else:
            quitcolor = (0, 100, 0)
        

        
         




    mouse.eat()
      
    for event in pygame.event.get():
        #Get event from queue and load into var event, then check if a specific event has occured
        if event.type == pygame.QUIT:
            pygame.quit()

    #Check if snake touching food (Collision)
    for i in range(anaconda.width):
        
        #for loop check if any point on the snake if within the same area as food (Not just top left corner)
        if ((anaconda.hitbox[0] + i >= mouse.hitbox[0]) and (anaconda.hitbox[0] + i <= mouse.hitbox [0] +  mouse.hitbox[2])) and ((anaconda.hitbox[1] + i >= mouse.hitbox[1]) and (anaconda.hitbox[1] + i <= mouse.hitbox [1] +  mouse.hitbox[3])):
            #Check if x-value (top-left point of box) is in the same x-value region as the food (Horizontally)
            #same for y-value
            #Two checks must happen at same time
            #increase size of snake
            #Add position of new block which has been added to the tail, to the list blockpositions (Check which direction facing to know where to add new block)
            if anaconda.direction == "up":
                anaconda.blockpositions.append((anaconda.blockpositions[anaconda.extrablocks][0], anaconda.blockpositions[anaconda.extrablocks][1] + 20, anaconda.blockpositions[anaconda.extrablocks][2], anaconda.blockpositions[anaconda.extrablocks][3]))
            if anaconda.direction == "down":
                anaconda.blockpositions.append((anaconda.blockpositions[anaconda.extrablocks][0], anaconda.blockpositions[anaconda.extrablocks][1] - 20, anaconda.blockpositions[anaconda.extrablocks][2], anaconda.blockpositions[anaconda.extrablocks][3]))
            if anaconda.direction == "right":
                anaconda.blockpositions.append((anaconda.blockpositions[anaconda.extrablocks][0] - 20, anaconda.blockpositions[anaconda.extrablocks][1], anaconda.blockpositions[anaconda.extrablocks][2], anaconda.blockpositions[anaconda.extrablocks][3]))
            if anaconda.direction == "left":
                anaconda.blockpositions.append((anaconda.blockpositions[anaconda.extrablocks][0] + 20, anaconda.blockpositions[anaconda.extrablocks][1], anaconda.blockpositions[anaconda.extrablocks][2], anaconda.blockpositions[anaconda.extrablocks][3]))
                
            anaconda.extrablocks += 1
            mouse.eaten = True
            break
        



    anaconda.checkdeath()
    drawgamewindow()
    anaconda.checkmovement()
    
  

#rendering and displaying font
textsurface = myfont.render('You Died', True, (255, 255, 0))
win.blit(textsurface,(200,200))
pygame.display.update()
pygame.time.delay(2000)
pygame.quit()
