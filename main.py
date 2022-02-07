import pygame 
import numpy as np

from flicky import FlickyManager
from keyboard import generate_font, writePhrase
from CCA import CCA
from lab_stream_layer import lsl, write_marker, read_from_Enobio
from pylsl import StreamInfo, StreamOutlet, resolve_stream
# from keyboard import 
grid = ["ABCDEFGHI",
        "JKLMNOPQR",
        "STUVWXYZ0",
        "123456789"
        ]
phrase = "Result: " #this is used to store the string at the bottom of the interface
result = [] # to save the freq_index of each iteration, which is used to measure the correct rate 
# defines samples per second
SAMPLES_PER_SECOND = 500
# defines the window size for the cca computation
window_size_in_seconds = 3
refreshing_rate = 60
total_frames = window_size_in_seconds * refreshing_rate
waittime = 1000   #milliseconds
frames = 0  #to caculate framse
marker_number = 111111 # initial marker nunber
# saving path for bmp file
saving_file = "D://KIT//semester_3//research_project//workspace//image//60Hz//"
# saving path for eeg data
sourcefile = 'D:\\KIT\\semester_3\\research_project\\21_12_03_SSVEP_Speller_3\\20220201183108_lsl_test1.easy'
# saving path for cca result
savepath = 'C:/Users/MetisVidere/Desktop/Bai_measurement/'
# saving path for csv file
resultfile = 'D:\\KIT\\semester_3\\research_project\\21_12_03_SSVEP_Speller_3\\easy_result.csv'
# parameters for lab-streamig layer
info = StreamInfo('MarkerStream','Markers',1,0,'int32','AttentionLabels')
outlet = StreamOutlet(info)
# stream_name = 'MarkerStream'
# streams = resolve_stream('type', 'EEG')
# markers = resolve_stream('type', 'Markers')
# if not os.path.exists(savepath):
#     os.mkdir(savepath)
##########################################################    
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
for i in range(len(freq)):
    for j in range(total_frames):
        file_name = grid[i]+str(freq[i])+'frame'+str(j)
        image = pygame.image.load(saving_file+file_name+'.bmp')
        Image[i].append(image)

# data = lsl(sourcefile, num_of_lines = 3000)
# frq_index, data = CCA(data, SAMPLES_PER_SECOND, 2) # determine the frequency of EEG
# letters_to_be_typed = grid[frq_index]
# phrase = phrase + letters_to_be_typed
# print(frq_index)
# # print(phrase)

# add all blocks    
flickymanager = FlickyManager(screen,width,height)


############for single letter####################
m = 0; #selected letter
flickymanager.add(4,1.5,width,height,Image[m],freq[m])
#################################################

# ############for the 3*3 keyboard##############
# # for n in range(3):
# #     for m in range(3):
# #         flickymanager.add(m+3,n+0.5,width,height,Image[columns*m+n],freq[columns*m+n])  
# ###############################################

# # #############for the whole keyboard###############
# for n in range(columns):
#     for m in range(rows):
#         flickymanager.add(m,n,width,height,Image[columns*m+n],freq[columns*m+n])  
# # #################################################
font = pygame.font.SysFont("None", 200)
text = font.render('Test Start', True, (255, 255, 255))
text_rect = text.get_rect()
screen.blit(text, (screenrect.width/2-text_rect.width/2,screenrect.height/2-text_rect.height/2))
pygame.display.flip()
pygame.time.wait(waittime)     
# hint()  
#iterations
write_marker(marker_number,outlet) # marker for begin
marker_number += marker_number 
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
    frames += 1
    ##########################
    #above process should be finished in one frame
    if frames == total_frames:   #60 framas per second, flickering for 4s
#        sleep(5)   #stop for certain seconds
        screen.fill((0,0,0))
        pygame.display.update()
        write_marker(marker_number,outlet) #marker for ending
        marker_number += marker_number 
        # pygame.time.wait(1000)  #stop for certain milliseconds
        ############ Analysis ####################
        # lsl(sourcefile, resultfile)
        # samples = read_from_Enobio(stream_name, streams)
        # markers = read_from_Enobio(stream_name, markers)
        ##########################################
        # frq_index = CCA(resultfile, savepath, SAMPLES_PER_SECOND, 2) # determine the frequency of EEG
        # letters_to_be_typed = grid[frq_index[0]]
        # phrase = phrase + letters_to_be_typed
        # result.append(frq_index)
        #################################################
        write_marker(marker_number,outlet) # marker for begin
        marker_number += marker_number 
        frames = 0  
        # hint()
pygame.quit()