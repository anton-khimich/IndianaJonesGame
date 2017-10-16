import pygame
import random
from pygame.locals import *
pygame.init()

class Player(pygame.sprite.Sprite):
    """A class that models the character that the player controls. The character
    can jump, and roll. The player also has a number of lives.
    """
    def __init__(self):
        """Construct the Player object. In addition to having properties that 
        allow the Player's jump and roll methods to work, the Player also tracks
        the score and amount of lives.
        """
        pygame.sprite.Sprite.__init__(self)
        self.score = 0
        self.lives = 0
        self.invcount = 0
        self.running = True
        self.jumping = False
        self.rolling = False
        self.runanim = []
        self.jumpanim = []
        self.rollanim = []
        self.damaged = pygame.image.load("indy_damaged.png").convert_alpha()
        self.animnum = 0
        self.jump_begin = False
        self.roll_begin = False
        self.jump_count = 0
        self.jump_height = 0
        
        #Animations
        for i in range(0, 16):
            temp = pygame.image.load("indy{}.png".format(i)).convert_alpha()
            self.runanim.append(temp)
        for i in range(0, 24):
            temp = pygame.image.load("indyroll{}.png".format(i)).convert_alpha()
            self.rollanim.append(temp)
        self.image = self.runanim[self.animnum]
        self.rect = self.image.get_rect()
        self.rect.topleft = (200, 290)
                           
    def update(self):
        """P.update() --> Non
        A method that checks if the Player collides with a trap, and if the Player
        is meant to jump, run or roll.
	"""
        if len(pygame.sprite.spritecollide(self, traps, False)) > 0:
                #Trap hit but the Player has extra lives
            if self.lives > 0 and self.invcount == 0:
                self.invincible()
                #Game Over
            if self.lives == 0 and self.invcount == 0:
                sound2.play()
                blackground = pygame.Surface(screen.get_size())
                blackground = blackground.convert()
                blackground.fill((0, 0, 0))
                end = myfont.render("You Died.", 1, (255, 255, 255))
                end1 = myfont.render("Your score was: {}.".format(self.player_score()), 1, (255, 255, 255))                
                screen.blit(blackground, (0, 0))
                screen.blit(end, (420, 180))
                screen.blit(end1, (330, 260))
                pygame.display.flip()
                global keep_going #So that this affects the main game loop as well.
                
                #A loop that quits the game when any key is pressed.
                while keep_going:
                    for ev in pygame.event.get(): 
                        if ev.type == pygame.QUIT:
                            keep_going = False
                        elif ev.type == KEYDOWN:
                            keep_going = False
                            
        if self.invcount > 0:
            self.invcount -=1
        if self.running:
            self.run()
        if self.jumping:
            self.jump()
        if self.rolling:
            self.roll()
    
    def run(self):
        """P.run() --> None
        A method that modifies the rect of the Player to ensure it is on the ground,
        and cycles through a list of animations.
        """
        self.rect = self.image.get_rect()
        self.rect.topleft = (200, 290)
        if self.animnum > 15:
            self.animnum = 0
        self.image = self.runanim[self.animnum]
        self.animnum += 1
        #Flickering of the Player while invulnerable
        if self.invcount > 0 and self.invcount % 2 == 0:
            self.image = self.damaged          
                   
    def jump(self):
        """P.jump() --> None
        A method that models the Player jumping.
        """
        if self.jump_begin:
            self.jump_count = 32
            self.jump_begin = False
            self.jump_height = 0
        if self.jump_count > 18:
            self.jump_height += 5
        if self.jump_count < 14 and self.jump_count != 0:
            self.jump_height -= 5
        if self.jump_count == 0:
            self.jumping = False
            self.running = True
        self.jump_count -=1
        if self.animnum > 15:
            self.animnum = 0
        self.image = self.runanim[self.animnum]         
        self.rect = self.image.get_rect()
        self.rect.topleft = (200, 290 - self.jump_height)
        #Flickering of the Player while invulnerable
        if self.invcount > 0 and self.invcount % 2 == 0:
            self.image = self.damaged         
        
    def roll(self):
        """P.roll() --> None
        A method that models the Player rolling.
        """
        if self.roll_begin:
            self.animnum = 0
            self.roll_begin = False
        self.image = self.rollanim[self.animnum]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (200, 342)
        self.animnum += 1
        if self.animnum >= 23:
            self.rolling = False
            self.running = True
        #Flickering of the Player while invulnerable
        if self.invcount > 0 and self.invcount % 2 == 0:
            self.image = self.damaged        
            
    def invincible(self):
        """P.invincible() --> None
        A method that makes the Player invincible to Traps after being hit by one.
        """
        self.lives -= 1
        self.score -= 1
        self.image = self.damaged
        if self.invcount == 0:
            self.invcount = 25
        sound1.play()
        
    
    def player_score(self):
        """P.score() --> str
        A method that returns the Player's score.
        """
        return str(self.score)

class Traps(pygame.sprite.Sprite):
    """A class that models a variety of traps that will harm the Player.
    """
    def __init__(self, trap):
        """Creates a Traps object, which is a Sprite, and selects from 3 different trap templates when
        placed in the game, as per the parameter given(trap).
        """
        pygame.sprite.Sprite.__init__(self)
        self.trap = trap
        self.traps = []
        self.trapnum = 0
        if self.trap == "spike":
            temp = pygame.image.load("trap0.png").convert_alpha()
            self.traps.append(temp)
            self.image = self.traps[self.trapnum]
            self.rect = self.image.get_rect()
            self.rect.bottomleft = (1000, 352)            
        elif self.trap == "bat":
            for i in range(0, 11):
                temp = pygame.image.load("bat{}.png".format(i)).convert_alpha()
                self.traps.append(temp)
            self.image = self.traps[self.trapnum]
            self.rect = self.image.get_rect()
            self.rect.topright = (1000, 265)
        elif self.trap == "snake":
            sound3.play()
            temp = pygame.image.load("snake.png").convert_alpha()
            self.traps.append(temp)
            self.image = self.traps[self.trapnum]
            self.rect = self.image.get_rect()
            self.rect.bottomleft = (1000, 342)

    def spawn(self):
        """T.spawn() --> None
        Creates a Trap object and adds it to the group of Traps.
        """
        #Has a random chance of making either of the 3 Traps.
        randnum = random.random()
        if randnum >= 2/3:
            t1 = Traps("spike")
        elif randnum <= 1/3:
            sound0.play()
            t1 = Traps("bat")
        else:
            t1 = Traps("snake")
        traps.add(t1)

    def update(self):
        """T.update() --> None
        A method that updates the Traps positions, as well as spawns Coins, Lives
        and other Traps.
        """
        if self.trap == "spike" or self.trap == "snake":
            self.rect.bottomleft = (self.rect.bottomleft[0] - 8, self.rect.bottomleft[1])
        if self.trap == "bat":
            temp = self.rect.bottomleft 
            if self.trapnum > 10:
                self.trapnum = 0            
            self.image = self.traps[self.trapnum]
            self.rect = self.image.get_rect()
            self.rect.bottomleft = (temp[0] - 16, temp[1])
            self.trapnum += 1       
        if self.rect.bottomright[0] < 0:
            self.kill()
            if len(traps) == 0:
                self.spawn()              
            if p.score % 5 == 0:
                c.spawn()
            if p.score % 10 == 0:
                l.spawn()
            p.score += 1     
        elif self.rect.bottomleft[0] == 280:
            randnum = random.random()
            if randnum >= self.chance():
                self.spawn()
        elif self.rect.bottomleft[0] == 744:
            randnum = random.random()
            if randnum >= self.chance():
                self.spawn()
                
    def chance(self):
        """T.chance() --> float
        Returns a float that changes the chance for a Trap to spawn.
        """
        if p.score < 8:
            chance = 0.65
        elif p.score >= 8 and p.score < 20:
            chance = 0.6
        elif p.score >= 20 and p.score < 40:
            chance = 0.55
        else:
            chance = 0.5
        return chance
            
class Rock(object):
    """A class that models a rotating rock surface.
    """
    def __init__(self):
        """Construct a Rock which has a list of animations.
        """
        self.anim = []
        self.animnum = 0
        for i in range(0, 12):
            temp = pygame.image.load("rock{}.png".format(i)).convert_alpha()
            self.anim.append(temp)
        
    def update(self):
        """R.update() --> None
        Cycles through the animations of the Rock.
        """
        if self.animnum > 11:
            self.animnum = 0
        screen.blit(self.anim[self.animnum], (-50, 230))
        self.animnum += 1
        
class Life(pygame.sprite.Sprite):
    """A class that models a Life object. The object will increase the amount of 
    lives the player has when they collide.
    """
    def __init__(self):
        """Construct a Life object, that is randomly placed off the screen on
        the right side.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("heart0.png").convert_alpha()
        self.rect = self.image.get_rect()
        rand_y = random.randint(235, 340)
        self.rect.bottomleft = (1500, rand_y)        
        
    def spawn(self):
        """L.spawn() --> None
        A method that places a Life object in the game.
        """
        l1 = Life()
        lives.add(l1)
    
    def update(self):
        """L.update() --> None
        A method that moves the Life object, as well as checking if it collides
        with the Player.
        """
        if pygame.sprite.collide_rect(self, p) == True:
            sound5.play()
            p.lives += 1
            self.kill()
        self.rect.bottomleft = (self.rect.bottomleft[0] - 8, self.rect.bottomleft[1])
        if self.rect.bottomright[0] < 0:
            self.kill()
        
class Coin(pygame.sprite.Sprite):
    """A class that models a Coin object. When it collides with the Player,
    it disappears, and 1 is added to the Player's score.
    """
    def __init__(self):
        """Construct a Coin object, that has a list of animations, and is placed
        randomly off the right edge of the screen.
        """
        pygame.sprite.Sprite.__init__(self)
        self.anim = []
        self.animnum = 0
    
        for i in range(0, 12):
            temp = pygame.image.load("coin{}.png".format(i)).convert_alpha()
            self.anim.append(temp)    
        self.image = self.anim[self.animnum]
        self.rect = self.image.get_rect()
        rand_y = random.randint(235, 340)
        self.rect.bottomleft = (1100, rand_y)
    
    def spawn(self):
        """C.spawn() --> None
        A method that places a Coin object within the game.
        """
        c1 = Coin()
        coins.add(c1)
    
    def update(self):
        """C.update() --> None
        A method that moves the Coin object, as well as adding to the score of 
        the Player if they collide.
        """
        if pygame.sprite.collide_rect(self, p) == True:
            sound4.play()
            p.score += 1
            self.kill()    
        if self.rect.bottomright[0] < 0:
            self.kill()   
        temp = self.rect.bottomleft 
        if self.animnum > 11:
            self.animnum = 0    
        self.image = self.anim[self.animnum]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (temp[0] - 8, temp[1])
        self.animnum += 1        

#Setting up for the Background and Foreground functions                            
background = pygame.image.load("background.png")
background_size = background.get_size()
screen = pygame.display.set_mode(background_size)
background = background.convert()

w = background.get_width()
x = 0
x1 = w

foreground = pygame.image.load("foreground.png").convert_alpha()
foreground1 = pygame.image.load("base.png").convert_alpha()
w1 = foreground.get_width()
h = background.get_height() - foreground.get_height()
a = 0
a1 = w1

#Font
myfont = pygame.font.Font("8bitOperatorPlus-Bold.ttf", 30)

#Image to that is shown beside number of lives
heart = pygame.image.load("heart1.png").convert_alpha()

#Music and Sounds
pygame.mixer.music.load("bgMusic.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)
sound0 = pygame.mixer.Sound("bat0.ogg")
sound1 = pygame.mixer.Sound("pain.ogg")
sound2 = pygame.mixer.Sound("museum.ogg")
sound3 = pygame.mixer.Sound("snakes.ogg")
sound4 = pygame.mixer.Sound("coin.ogg")
sound5 = pygame.mixer.Sound("life.ogg")

def Background():
    """Background() --> None
    A function that moves the two backgrounds in order to create an infinite 
    background. This is achieved by having one background begin where the other ends,
    and when one is completely off the screen, it is moved to the right of the
    visible background.
    """
    global x, x1
    x -= 2
    x1 -= 2
    screen.blit(background, (x,0))
    screen.blit(background, (x1, 0))
    if x <= -w:
        x = w
    if x1 <= -w:
        x1 = w  
        
def Foreground():
    """Foreground() --> None
    A function that moves the four foregrounds(top and bottom) in order to create an infinite 
    foreground. This is done the same way as in Background().
    """
    global a, a1
    a -= 8
    a1 -= 8
    screen.blit(foreground, (a,h))
    screen.blit(foreground, (a1, h))
    screen.blit(foreground1, (a, 0))
    screen.blit(foreground1, (a1, 0))
    if a <= -w1:
        a = w1
    if a1 <= -w1:
        a1 = w1  
        
def Score():
    """Score() --> None
    A function that displays the Player's score at the top left of the screen as
    a Font object.
    """
    label = myfont.render("Score: {}".format(p.player_score()), 1, (255, 255, 255))
    screen.blit(label, (50, 20))  
    
def Lives():
    """Lives() --> None
    A function that displays the Player's number of lives at the top left of the
    screen.
    """
    label = myfont.render("x {}".format(p.lives), 1, (255, 255, 255))
    screen.blit(label, (100, 70))
    screen.blit(heart, (50, 73))

#Labels and variables for the Instructions() function.
x3 = 300
x4 = 1300
label0 = myfont.render("Press Up or Space to jump.", 1, (255, 255, 255))
label1 = myfont.render("Press Down to roll.", 1, (255, 255, 255))
    
def Instructions():
    """Instructions() --> None
    A function that places some basic instructions on the screen, and then moves
    them off the screen.
    """
    global x3, x4
    if x3 > -500:
        screen.blit(label0, (x3, 160))
        x3 -= 4
    if x4 > -500:
        screen.blit(label1, (x4, 160))
        x4 -= 4

#Clock for the game loop.
clock = pygame.time.Clock() 
#This counter makes it so no input can be detected for some time after a key is pressed.
clock_count = 0
keep_going = True
paused = False

#Objects that are in the beginning of the game.
p = Player()
t = Traps("spike")
r = Rock()
c = Coin()
l = Life()

#Groups for the objects in order to update them all at once.
player = pygame.sprite.Group()
traps = pygame.sprite.Group()
coins = pygame.sprite.Group()
lives = pygame.sprite.Group()
player.add(p)
traps.add(t)
coins.add(c)
lives.add(l)

while keep_going:
    clock.tick(30)
    
    for ev in pygame.event.get():        
        if ev.type == pygame.QUIT:
            keep_going = False
        elif ev.type == pygame.KEYDOWN:
            #If the user wants to jump
            if ev.key == pygame.K_UP and clock_count == 0 or ev.key == pygame.K_SPACE and clock_count == 0:
                clock_count = 32
                p.running = False
                p.jump_begin = True
                p.jumping = True  
            #If the user wants to roll
            elif ev.key == pygame.K_DOWN and clock_count == 0:
                clock_count = 24
                p.running = False
                p.roll_begin = True
                p.rolling = True
            #If the user wants to pause
            elif ev.key == pygame.K_p:
                paused = True
    
    #A loop that keeps the game paused unless unpaused by the user.            
    while paused:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                keep_going = False
                paused = False
            if ev.type == KEYDOWN:
                if ev.key == pygame.K_p:
                    paused = False
                    
    #The updation of all Groups as well as the blitting of all Surfaces.                
    Background()
    Foreground()    
    player.draw(screen)
    player.update()
    traps.draw(screen)
    traps.update()
    coins.draw(screen)
    coins.update()
    lives.draw(screen)
    lives.update()
    r.update()
    Score()
    Lives()
    Instructions()
    pygame.display.flip()
    
    if clock_count > 0:
        clock_count -= 1