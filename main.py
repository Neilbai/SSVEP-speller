import pygame 
import numpy as np

from flicky import FlickyManager
from keyboard import generate_font, writePhrase, hint
from CCA import CCA
from lab_stream_layer import lsl, write_marker
from pylsl import StreamInfo, StreamOutlet, resolve_stream

grid =  ["ABC",
          "DEF",
          "GHI"]
groudtruth = "groudtruth: "
phrase = "Result: " #this is used to store the string at the bottom of the interface
letter_to_be_printed = []
result = [] # to save the freq_index of each iteration, which is used to measure the correct rate 
# defines samples per second
SAMPLES_PER_SECOND = 500
# defines the window size for the cca computation
window_size_in_seconds = 4
refreshing_rate = 60
total_frames = window_size_in_seconds * refreshing_rate
waittime = 1000   #milliseconds
frames = 0  #to caculate framse
marker_start = 111111 # initial marker nunber
marker_end = 222222

# saving path for bmp file
saving_file = "D:/KIT/semester_3/research_project/workspace/image/33_new_grid//"
# saving path for eeg data
sourcefile = 'D:/KIT/semester_3/research_project/workspace/main/src/11.75.easy'
# saving path for cca result
savepath = 'C:/Users/MetisVidere/Desktop/Bai_measurement/'
# parameters for lab-streamig layer
info = StreamInfo('MarkerStream','Markers',1,0,'int32','AttentionLabels')
outlet = StreamOutlet(info)

##########################################################    
image = []
grid = [''.join(s) for s in zip(*grid)]  #transpose
rows = len(grid)
columns = len(grid[0])      #save the rows and cols
flat_grid = [y for x in grid for y in x]  # then flatten the grid

freq_33 = [np.linspace(8,10,3),
        np.linspace(11,13,3),
        np.linspace(14,16,3)]
freq = np.array(freq_33).transpose()
freq = freq.flatten()

pygame.init()
screen = pygame.display.set_mode((0, 0),pygame.FULLSCREEN)
pygame.display.set_caption("SSVEP_SPELLER")
screenrect = screen.get_rect()  #get the size of screen
width = screenrect.width / rows
height = screenrect.height / (columns + 1) # height of letter, or height of a column
End_test = False
clock = pygame.time.Clock()
# generate image for all the frames
# Image = generate_font(freq,4,refreshing_rate,flat_grid,saving_file) # draw the letter for all frames,freq*frames
# load the image
Image = [[] for i in range(len(freq))]
for i in range(len(freq)):
    for j in range(total_frames):
        file_name = flat_grid[i]+str(freq[i])+'frame'+str(j)
        image = pygame.image.load(saving_file+file_name+'.bmp')
        Image[i].append(image)


# add all blocks    
flickymanager = FlickyManager(screen,width,height)


############for single letter####################
# m = 0; #selected letter
# flickymanager.add(1,0.5,width,height,Image[m],freq[m])
#################################################

# ############for the 3*3 keyboard##############
# for n in range(3):
#     for m in range(3):
#         flickymanager.add(m,n,width,height,Image[columns*m+n],freq[columns*m+n])  
# ###############################################

# # #############for the whole keyboard###############
for n in range(columns):
    for m in range(rows):
        flickymanager.add(m,n,width,height,Image[columns*m+n],freq[columns*m+n])  
# # #################################################
font = pygame.font.SysFont("None", 200)
text = font.render('Test Start', True, (255, 255, 255))
text_rect = text.get_rect()
screen.blit(text, (screenrect.width/2-text_rect.width/2,screenrect.height/2-text_rect.height/2))
pygame.display.flip()
pygame.time.wait(waittime)   
screen.fill((0,0,0))  
# num_of_red_letter = np.random.randint(0,35)
# letter_to_be_printed.append(num_of_red_letter) 
#############################################################
letter = ["ABC",
          "DEF",
          "GHI"]
letter = [''.join(s) for s in zip(*letter)]  #transpose
flat_letter = [y for x in letter for y in x]  # then flatten the grid
num_of_red_letter = np.random.randint(0,8)
letter_to_be_printed.append(num_of_red_letter) 
groudtruth = groudtruth + flat_letter[num_of_red_letter]
# hint(screen, letter, num_of_red_letter, width,height) 
hint(screen, grid, num_of_red_letter, width, height) 
pygame.display.flip()
pygame.time.wait(waittime)  
#iterations
write_marker(marker_start,outlet) # marker for begin
marker_start += 1 
while End_test==False: 
    for event in pygame.event.get():
        if (event.type == pygame.KEYUP) or (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_ESCAPE):
                End_test = True
        if event.type == pygame.QUIT:
            End_test = True
    screen.fill((0,0,0))    #backgroud color
    clock.tick(refreshing_rate) #  frames ~ 240FPS
    ###########################
    flickymanager.process(frames)
    flickymanager.draw()
    writePhrase(screen,phrase,height/4)
    writePhrase(screen,groudtruth, 3*height/4)
    hint(screen, grid, num_of_red_letter, width, height) 
    pygame.display.flip()
    frames += 1
    ##########################
    #above process should be finished in one frame
    if frames == total_frames:   #60 framas per second, flickering for 4s
        screen.fill((0,0,0))
        pygame.display.update()
        write_marker(marker_end,outlet) #marker for ending
        marker_end += 1 
        writePhrase(screen,phrase,height/4)
        writePhrase(screen,groudtruth, 3*height/4)
        pygame.display.flip()
        pygame.time.wait(3000)  #stop for certain milliseconds
        ############ Analysis ####################
        # data = lsl(sourcefile)
        # #########################################
        # freq33 = np.array(freq_33)
        # frqeucies = freq33.flatten()
        # frq_index, data = CCA(data, frqeucies, SAMPLES_PER_SECOND, 4) # determine the frequency of EEG
        # # letters_to_be_typed = flat_grid[frq_index]
        # letters_to_be_typed = flat_letter[frq_index]
        # phrase = phrase + letters_to_be_typed
        # result.append(frq_index)
        ################################################
        write_marker(marker_start,outlet) # marker for begin
        marker_start += 1 
        frames = 0  
        num_of_red_letter = np.random.randint(0,8)
        # num_of_red_letter = np.random.randint(0,35)
        letter_to_be_printed.append(num_of_red_letter) 
        groudtruth = groudtruth + flat_letter[num_of_red_letter]
        hint(screen, grid, num_of_red_letter, width, height) 
        pygame.display.flip()
        pygame.time.wait(waittime)
pygame.quit()