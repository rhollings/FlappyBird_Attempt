import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()
fps = 50

width = 500
height = 800

screen = pygame.display.set_mode((500, 800))
pygame.display.set_caption("Nappy")

#score
font = pygame.font.SysFont('Bauhaus 93', 63)
white = (255, 255, 255)

#define game variables
ground_scroll = 0
scroll_speed = 3
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1650 #miliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False

#load images
player = pygame.image.load('gallery/pics/bird2.png')
bg = pygame.image.load('gallery/pics/background.png')
ground = pygame.image.load('gallery/pics/base.png')
button_img = pygame.image.load('gallery/pics/rob.png')

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(height / 2)
    score = 0
    return score
 
#adding the bird
class Bird(pygame.sprite.Sprite):   #using sprite to add bird
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1,3):
            img = pygame.image.load(f'gallery/pics/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel = 0
        self.clicked = False

    def update(self):

        if flying == True:

            self.vel += 0.5  #player gravity
            if self.vel > 7:
                self.vel = 7
            if self.rect.bottom < 690:
                self.rect.y += int(self.vel)

            if game_over == False:
            #jump
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    self.vel = -10
                if pygame.mouse.get_pressed()[0] == 0:
                    self.clicked = False

            #animation
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                    self.counter = 0
                    self.index += 1
                    if self.index >= len(self.images):
                        self.index = 0
            self.image = self.images[self.index]

            #rotation
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], self.vel -90)

#class for creating pipes
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('gallery/pics/pipe.png')
        self.rect = self.image.get_rect()
        #position 1 is top/ -1 is btm
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):

        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action
           

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()
                                       
flappy = Bird(100, int(height / 2))

bird_group.add(flappy)

btm_pipe = Pipe(300, int(height / 2), -1)#add pipe
top_pipe = Pipe(300, int(height / 2.2), 1)
pipe_group.add(btm_pipe)
pipe_group.add(top_pipe)

#button
button = Button(width // 2 - 180, height // 2 - 100, button_img)


run = True
while run:

    clock.tick(fps)

    screen.blit(bg, (0, 0)) #background

    bird_group.draw(screen) #adding bird to loop
    bird_group.update()
    pipe_group.draw(screen) #adding pipes to loop

    

    screen.blit(ground, (ground_scroll,690)) #draw ground

    #score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
           and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
           and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False

    draw_text(str(score), font, white, int(width / 2), 20)
    

    #collisions
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True
    #true for delete
    #bird hit ground
    if flappy.rect.bottom >= 690:
        game_over = True
        flying = False

    if game_over == False and flying == True:

        #make new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(width, int(height / 2) + pipe_height, -1)#add pipe
            top_pipe = Pipe(width, int(height / 2.3) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

            
            
        ground_scroll -= scroll_speed #scroll speed
        if abs(ground_scroll) > 30:
            ground_scroll = 0

        pipe_group.update()

    #game over
    if game_over == True:
        if button.draw() == True:
            game_over = False
            score = reset_game()
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    pygame.display.update()

pygame.quit()

