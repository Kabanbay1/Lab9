import pygame, sys
from pygame.locals import *
import random, time
 
pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
COINS=random.randint(2,10)
SPEED = 5
SCORE = 0
SCORE1 = 0
coin=pygame.image.load("Coin.png")
 
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)
 
background = pygame.image.load("AnimatedStreet.png")
 
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")
 
class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)  
 
      def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if (self.rect.top > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Coin(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.transform.scale(coin,(20,20))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)  
 
      def move(self):
        self.rect.move_ip(0,COINS)
        if (self.rect.top > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,5)
         
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)

P1 = Player()
E1 = Enemy()
C1= Coin() #coins
 
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)
 
INC_SPEED = pygame.USEREVENT + 0
pygame.time.set_timer(INC_SPEED, 1000)

while True:
       
    for event in pygame.event.get():
        if event.type == INC_SPEED:
              SPEED += 0.5     
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
 
    DISPLAYSURF.blit(background, (0,0))
    scores = font_small.render(str(SCORE), True, BLACK)
    scores1 = font_small.render(str(SCORE1), True, "YELLOW")
    DISPLAYSURF.blit(scores1, (360 ,10))    
    DISPLAYSURF.blit(scores, (10,10))
 
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

   #To be run if collision occurs between Player and Coin
    if pygame.sprite.spritecollideany(P1, coins):
        #if a player collects N number of bonus score or more, the speed becomes proportional to the score
        if SCORE1 >= 500:
            SPEED = SCORE1/100 
        pygame.mixer.Sound('catch.mp3').play()
        coin = pygame.sprite.spritecollideany(P1, coins)  # Get the collided coin
        if coin:
            if isinstance(coin, Coin):
                SCORE1 += 10
            coin.kill()  # Remove the collided coin
            # Generate new coin that hasn't been collected yet and doesn't spawn inside the player
            available_coins = [C1]
            collected_coins = [sprite for sprite in coins if sprite.rect == coin.rect]
            available_coins = [coin for coin in available_coins if coin not in collected_coins]
            if available_coins:
                new_coin = random.choice(available_coins)
                new_coin.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)
                # Check if new coin collides with the player
                while pygame.sprite.spritecollideany(new_coin, all_sprites):
                    new_coin.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)
                coins.add(new_coin)
                all_sprites.add(new_coin)


    if pygame.sprite.spritecollideany(P1, enemies):
          pygame.mixer.Sound('crash.wav').play()
          time.sleep(0.5)
                    
          DISPLAYSURF.fill(RED)
          DISPLAYSURF.blit(game_over, (30,250))
           
          pygame.display.update()
          for entity in all_sprites:
                entity.kill() 
          time.sleep(2)
          pygame.quit()
          sys.exit()        
         
    pygame.display.update()
    FramePerSec.tick(FPS)
