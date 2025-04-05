#Создай собственный Шутер!

from pygame import *
from random import *

win__width = 700 #ширина окна
win_heigt = 500 #высота
lose = 0
score = 0
img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
img_enemy = 'ufo.png'
img_bullet = 'bullet.png'
score = 0
lost = 0
max_lost = 3 #счётчик выхода
goal = 10 #Победа 
#классы объектов
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x< win__width-80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        #исчезновение в конце экрана
        if self.rect.y > win_heigt:
            self.rect.x = randint(80, win__width-80)
            self.rect.y = 0
            lost+=1
class Bullet(GameSprite):
    def update(self):
        self.rect.y+= self.speed

        if self.rect.y<0:
            self.kill()

#созание окна
window = display.set_mode((win__width, win_heigt))
display.set_caption('SpaceShooter')

background = transform.scale(image.load(img_back), (win__width, win_heigt))

#музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
#игрок
ship = Player(img_hero, 5, win_heigt-100, 80, 100, 10)
finish = False
run = True
#группа врагов
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win__width-80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
bullets = sprite.Group()
    #текст
font.init()
font2 = font.SysFont('Verdana', 36)

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()
    if not finish:
        window.blit(background, (0, 0))
        #текст
        text = font2.render('Счёт: '+ str(score), 1, (255, 255, 255))
        window.blit(text,(10, 20))

        text_lose = font2.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        ship.update()
        ship.reset()
        bullets.update()
        bullets.draw(window)
        monsters.update()
        monsters.draw(window)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score+=1
            monster = Enemy(img_enemy, randint(80, win__width-80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        if sprite.spritecollide(ship  , monsters, False) or lost>=max_lost:
            finish = True
            window.blit(text_lose, (200, 200))
        if score>= goal:
            finish = True
            window.blit(text, (200, 200))
        display.update()

    time.delay(50)