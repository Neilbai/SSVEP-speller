import pygame
import numpy as np
# from flicky import FlickyManager

# we will use this function to write the letters
def write(msg, stim_ints):    
        myfont = pygame.font.SysFont("None", 200)
        pygame.display.set_mode()
        color = (stim_ints*255,stim_ints*255,stim_ints*255)
        mytext = myfont.render(msg, True, color)
        mytext = mytext.convert_alpha()
        return mytext

#Generate font of all frames in advance n_letters*frames
def generate_font(freq,duration,refresh_freq,letter,saving_file): 
    Image = [[] for i in range(len(freq))]
    total_frames = duration*refresh_freq    #total_framse = duruation*refresh_freq 
    for i in range(len(freq)):
        for j in range(total_frames):
            stim_ints = 1/2*(1 + np.sin(2*np.pi*freq[i]*(j/refresh_freq)))
            file_name = letter[i]+str(freq[i])+'frame'+str(j)
            letter_image = write(letter[i],stim_ints)
            pygame.image.save(letter_image,saving_file+file_name+'.bmp')
            Image[i].append(letter_image)
    return Image
            
def writePhrase(screen,phrase,width,height):
    myfont = pygame.font.SysFont("None", 200)
    mytext = myfont.render(phrase, True, (255,255,255))
    mytext = mytext.convert_alpha()
    text_rect = mytext.get_rect()
    screen.blit(mytext, (0, height/5))

# mark the letter in red as a hint for the tester
# def hint():
    # myfont = pygame.font.SysFont("None", 200)
    # mytext = myfont.render(phrase, True, (255,255,255))
    # mytext = mytext.convert_alpha()
    # text_rect = mytext.get_rect()
    # screen.blit(mytext, (0, height/5))