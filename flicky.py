class FlickyManager:
    def __init__(self,screen,width,height,frames=0):
        self.flickies = []  # letters and its flicky frequency
        self.screen = screen
        self.width = width
        self.height = height
    def add(self,x,y,width,height,letter,freq):
        x = width * x + width/4
        y = height * (y + 1) + height/4
        f = Flicky(x,y,letter,freq) # letter image of all frames
        self.flickies.append(f)
    def process(self,frames):
        for f in self.flickies:
            f.process(frames)
    def draw(self):
        for n in range(len(self.flickies)):
            f = self.flickies[n]
            f.draw(self.screen)
        

class Flicky(object):
    def __init__(self,x,y,letter,freq):
        self.x = x
        self.y = y
        self.freq = freq
        self.letter = letter
        self.image = []
    def process(self,frames):
        self.image = self.letter[frames]
    def draw(self,screen):
        screen.blit(self.image, (self.x, self.y))