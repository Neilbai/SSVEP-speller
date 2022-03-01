import pygame 
import numpy as np

from flicky import FlickyManager
from keyboard import generate_font, writePhrase, hint
from CCA import CCA
from lab_stream_layer import lsl, write_marker
from pylsl import StreamInfo, StreamOutlet, resolve_stream

# grid = ["ABCDEFGHI",
#         "JKLMNOPQR",
#         "STUVWXYZ0",
#         "123456789"
#         ]

grid =  ["ABC",
          "DEF",
          "GHI"]
groudtruth = "groudtruth: "
phrase = "Result: " #this is used to store the string at the bottom of the interface
# defines samples per second
SAMPLES_PER_SECOND = 500
# defines the window size for the cca computation
window_size_in_seconds = 1
refreshing_rate = 60
total_frames = window_size_in_seconds * refreshing_rate
waittime = 1000   #milliseconds

# saving path for bmp file
saving_file = "D:/KIT/semester_3/research_project/workspace/image/33_new//"
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
# pygame.init()
# screen = pygame.display.set_mode((0, 0),pygame.FULLSCREEN)
# pygame.display.set_caption("SSVEP_SPELLER")
# screenrect = screen.get_rect()  #get the size of screen
# width = screenrect.width / rows
# height = screenrect.height / (columns + 1) # height of letter, or height of a column
# End_test = False
# clock = pygame.time.Clock()
# generate image for all the frames
Image = generate_font(freq,4,refreshing_rate,flat_grid,saving_file,grid_dimension = 1) # draw the letter for all frames,freq*frames
pygame.quit()