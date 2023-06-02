import pygame

def init():
    pygame.init()
    window = pygame.display.set_mode((480,480))

def getKey(keyname):
    answer = False
    for event in pygame.event.get():pass
    keyinput = pygame.key.get_pressed()
    currentKey = getattr(pygame, 'K_{}'.format(keyname))
    if keyinput[currentKey]:
        answer = True
    pygame.display.update()
    return answer



if __name__ == "__main__":
    init()
