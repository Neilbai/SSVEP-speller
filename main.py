import pygame 
import numpy as np
from flicky import FlickyManager
from keyboard import generate_font, writePhrase
# from keyboard import 

grid = ["ABCDEFGHI",
        "JKLMNOPQR",
        "STUVWXYZ0",
        "123456789"
        ]
phrase = "Result: " #this is used to store the string at the bottom of the interface

waittime = 1000   #milliseconds
frames = 0  #to caculate framse
saving_file = "D://KIT//semester_3//research_project//workspace//image//60Hz//"
image = []
grid = [''.join(s) for s in zip(*grid)]  #transpose
rows = len(grid)
columns = len(grid[0])      #save the rows and cols
grid = [y for x in grid for y in x]  # then flatten the grid
freq = [np.linspace(8,16,9),
        np.linspace(8.25,16.25,9),
        np.linspace(8.5,16.5,9),
        np.linspace(8.75,16.75,9)]
freq = np.array(freq).transpose()
freq = freq.flatten()
# print(freq)
pygame.init()
screen = pygame.display.set_mode((0, 0),pygame.FULLSCREEN)
pygame.display.set_caption("SSVEP_SPELLER")
screenrect = screen.get_rect()  #get the size of screen
width = screenrect.width / rows
height = screenrect.height / (columns + 1)
End_test = False
clock = pygame.time.Clock()
# generate image for all the frames
# Image = generate_font(freq,4,60,grid,saving_file) # draw the letter for all frames,freq*frames
# load the image
Image = [[] for i in range(len(freq))]
total_frames = 240
for i in range(len(freq)):
    for j in range(total_frames):
        file_name = grid[i]+str(freq[i])+'frame'+str(j)
        image = pygame.image.load(saving_file+file_name+'.bmp')
        Image[i].append(image)


#add all blocks    
flickymanager = FlickyManager(screen,width,height)


############for single letter####################
# m = 0; #selected letter
# flickymanager.add(4,1.5,width,height,Image[m],freq[m])
#################################################

#############for the 3*3 keyboard##############
# for n in range(3):
#     for m in range(3):
#         flickymanager.add(m+3,n+0.5,width,height,Image[columns*m+n],freq[columns*m+n])  
################################################

##############for the whole keyboard###############
for n in range(columns):
    for m in range(rows):
        flickymanager.add(m,n,width,height,Image[columns*m+n],freq[columns*m+n])  
##################################################
font = pygame.font.SysFont("None", 200)
text = font.render('Test Start', True, (255, 255, 255))
text_rect = text.get_rect()
screen.blit(text, (screenrect.width/2-text_rect.width/2,screenrect.height/2-text_rect.height/2))
pygame.display.flip()
pygame.time.wait(waittime)       
#iterations
while End_test==False:   
    for event in pygame.event.get():
        if (event.type == pygame.KEYUP) or (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_ESCAPE):
                End_test = True
        if event.type == pygame.QUIT:
            End_test = True
    screen.fill((0,0,0))    #backgroud color
    clock.tick(60) #  frames ~ 60FPS
    ###########################
    flickymanager.process(frames)
    flickymanager.draw()
    writePhrase(screen,phrase,width,height)
    pygame.display.flip()
    ##########################
    #above process should be finished in one frame
    frames += 1
    if frames == 240:   #60 framas per second, flickering for 4s
#        sleep(5)   #stop for certain seconds
        screen.fill((0,0,0))
        pygame.display.update()
        pygame.time.wait(5000)  #stop for certain milliseconds
        frames = 0
    ############ Analysis ####################
    
    #################################################
        
        
pygame.quit()