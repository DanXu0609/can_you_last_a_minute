
import pygame
import random
from missle_util import generateLocation, determineSpeed
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

WIDTH = 800
HEIGHT = 600
SPACESHIPWIDTH = 50
SPACESHIPHEIGHT = 30
FPS = 60
ADDENEMY = pygame.USEREVENT + 1
UPDATELOCATION = pygame.USEREVENT + 2
SCORING = pygame.USEREVENT+3




class Missle(pygame.sprite.Sprite):
    def __init__(self,tx,ty):
        super(Missle,self).__init__()
        self.choose = random.randint(0,3)
        self.locations = generateLocation(self.choose)
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((100, 68, 26))
        self.rect = self.surf.get_rect(
            center=self.locations
        )
        self.slope = (self.rect.centery - ty) / (self.rect.centerx - tx) if self.rect.centerx != tx  else 0.0

        (self.speedx , self.speedy) = determineSpeed(self.choose,self.slope)

    def update(self):
        self.rect.move_ip(self.speedx, self.speedy)
        if self.rect.right < 0 or self.rect.bottom < 0 or self.rect.left > WIDTH or self.rect.top > HEIGHT:
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.transform.rotate(pygame.
        transform.scale(pygame.image.load("spaceship.png"),(SPACESHIPWIDTH ,SPACESHIPHEIGHT)),180)

        self.rect = self.surf.get_rect()
        self.rect.width = SPACESHIPWIDTH
        self.rect.height = SPACESHIPHEIGHT
        self.rect.centerx = WIDTH/2
        self.rect.centery = HEIGHT/2

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT

        
        
def main():
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()
    SOCRE_FONT = pygame.font.SysFont('comicsans', 30)
    pygame.mixer.music.load("bgm.mp3")
    collision_sound = pygame.mixer.Sound("game_over.ogg")
    pygame.mixer.music.play(loops=-1)
    player = Player()
    score = 0
    screen = pygame.display.set_mode((WIDTH,HEIGHT))


    pygame.time.set_timer(ADDENEMY, 25)
    pygame.time.set_timer(UPDATELOCATION,25)
    pygame.time.set_timer(SCORING,1000)
    missiles = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    screen.blit(player.surf, player.rect)
    pygame.display.flip()
    targetx = player.rect.centerx
    targety = player.rect.centery

    running = True
    clock = pygame.time.Clock()


    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

            elif event.type == QUIT:
                running = False
            elif event.type == ADDENEMY:
                new_enemy = Missle(targetx,targety)
                missiles.add(new_enemy)
                all_sprites.add(new_enemy)
            elif event.type == UPDATELOCATION:
                targetx = player.rect.centerx
                targety = player.rect.centery
            elif event.type == SCORING:
                score +=  1
            
        screen.fill((255,255,255))
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        missiles.update()


        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        
        screen.blit(player.surf,player.rect)
        if pygame.sprite.spritecollideany(player, missiles):
            score_text = "You last " + str(score) + " seconds!"
            draw_text = SOCRE_FONT.render(score_text, 1, (0,0,0))
            screen.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                            2, HEIGHT/2 - draw_text.get_height()/2))
            player.kill()
            pygame.display.flip()
            collision_sound.play()
            pygame.time.delay(2000)
            running = False

        
        pygame.display.flip()

    pygame.mixer.music.stop()
    pygame.mixer.quit()



if __name__ == '__main__':
    main()
