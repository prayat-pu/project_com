#sprite class for plat from
from settings import *
import pygame as pg 
from os import path
vec = pg.math.Vector2
from random import choice,randrange
# from random import*

class player(pg.sprite.Sprite):
    def __init__(self,game):
        self._layer = player_layer
        self.group = game.all_sprites
        pg.sprite.Sprite.__init__(self,self.group)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.radius = 30
        self.rect = self.image.get_rect()
        self.rect.center = (40,height - 100)
        self.pos = vec(width/2,height/4 -100)
        self.vel = vec(0,0)
        self.acc = vec(0,0)

        # self.dir = path.dirname(__file__)
        # self.snd_dir = path.join(self.dir,'sound')
        # self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir,'jump19.wav'))

    def mp(self,picture,x,y):

        pic = pg.image.load(path.join('img',picture)).convert_alpha()
        pic = pg.transform.scale(pic,(x,y))
        return pic


    def load_images(self):
        stand = self.mp('m_stand.png',62,100)
        ready = self.mp('m_ready.png',62,100)
        self.standing_frames = [stand,ready]

        for i in self.standing_frames:
            i.set_colorkey(black)
            
        move_r1 = self.mp('m_r_1.png',60,100)
        move_r2 = self.mp('m_r_2.png',60,100)

        self.walking_frames_r = [move_r1,move_r2]

        for i in self.walking_frames_r:
            i.set_colorkey(black)

        self.walking_frames_l = []
        for frame in self.walking_frames_r:
            frame.set_colorkey(black)
            self.walking_frames_l.append(pg.transform.flip(frame,True,False))
            
        self.jump_frame = self.mp('m_j.png',75,87)
        self.jump_frame.set_colorkey(black)
        
    def jump(self):
        #jump only player stand block
        # self.rect.x += 1 
        hits = pg.sprite.spritecollide(self,self.game.platform,False)
        hit_slidr = pg.sprite.spritecollide(self,self.game.slideptr,False)
        hit_slidl = pg.sprite.spritecollide(self,self.game.slideptl,False)
        # if self.pos.y < hits[0].rect.centery:
        #     self.player.pos.y = lowest.rect.top + 1
        # # self.rect.x -=1

        if hits and not self.jumping:
            self.game.jump_sound.play()
            self.jumping = True
            self.vel.y = -player_jump
        elif hit_slidr or hit_slidl:
            self.game.jump_sound.play()
            self.jumping = True
            self.vel.y = -player_jump

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    
    def update(self):
        self.animation()
        self.acc = vec(0,0.5)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -player_acc
        if keys[pg.K_RIGHT]:
            self.acc.x = player_acc

        self.acc.x += (self.vel.x
         *player_friction)


        self.vel += self.acc
        self.pos += self.vel + 0.5*self.acc

        if self.pos.x > width + self.rect.width/2:
            self.pos.x = 0 - self.rect.width/2
        if self.pos.x < 0 - self.rect.width/2 :
            self.pos.x = width + self.rect.width /2

        self.rect.midbottom = self.pos

    def animation(self):
        now = pg.time.get_ticks()

        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        #show work
        if self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1)%len(self.walking_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walking_frames_r[self.current_frame]
                    self.vel.x = 0
                else:
                    self.image = self.walking_frames_l[self.current_frame]
                    self.vel.x = 0


        #show idle animation
        if not self.jumping and not self.walking:
            #time to swtih img
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1)%len(self.standing_frames)
                
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        self.mask = pg.mask.from_surface(self.image)


class platform(pg.sprite.Sprite):
    def __init__(self,game,x,y,first_plat):
        self._layer = platform_layer
        self.group = game.all_sprites,game.platform
        pg.sprite.Sprite.__init__(self,self.group)
        self.game = game
        ground1 = self.mp('g1.png',150,35)
        ground2 = self.mp('g2.png',100,35)
        image =[ground1,ground2]
        self.image = choice(image)
        if self.image == image[1] and first_plat == False:
            x = choice([0,100,200,300,400])
        # self.image = pg.Surface((w,h))
        self.image.set_colorkey(white)
        # self.image.fill(green)
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y

        if self.game.score > 1300:
            if randrange(80) < pow_spaw:
                pow(self.game,self) 
        if self.game.score > 2000:
            if randrange(100) < bur_spaw:
                bur(self.game,self)
        if randrange(100) < coin_spaw:
            coin(self.game,self)
        # self.rect.y += 1
        # self.rect.x +=5
    def mp(self,picture,x,y):

        pic = pg.image.load(path.join('img',picture)).convert_alpha()
        pic = pg.transform.scale(pic,(x,y))
        return pic
        # self.rect.x +=5

    def update(self) :
        self.rect.y += 1

class slideptr(pg.sprite.Sprite):
    def __init__(self,game):
        self._layer = platform_layer
        self.group = game.all_sprites,game.slideptr
        pg.sprite.Sprite.__init__(self,self.group)

        self.game = game
        image =self.mp('KY.png',100,35)
        self.image = image
        # self.image = pg.Surface((w,h))
        self.image.set_colorkey(black)
        # self.image.fill(green)
        self.rect = self.image.get_rect()
        self.rect.centerx = -100
        self.vx = randrange(1,2)
        self.rect.y = -500
        self.dy = 0.5
        # print(self.slide_speed)

    def update(self):

        self.rect.x += self.vx
        self.speed = self.vx
        # print(self.speed)
        # print(self.rect.x)
        # self.player.rect.x += self.vx
        # print(self.vx)
        center = self.rect.center
        self.rect = self.image.get_rect()
        # self.mask = pg.mask.from_surface(self.image)
        self.rect.center = center
        # self.rect.y += self.vy

        if self.rect.left > width + 100 or self.rect.right < -100:
            self.kill()
        if self.rect.top + 10 >= height :
            self.kill()
    def mp(self,picture,x,y):

        pic = pg.image.load(path.join('img',picture)).convert_alpha()
        pic = pg.transform.scale(pic,(x,y))
        return pic

class slideptl(pg.sprite.Sprite):
    def __init__(self,game):
        self._layer = platform_layer
        self.group = game.all_sprites,game.slideptl
        pg.sprite.Sprite.__init__(self,self.group)

        self.game = game
        image =self.mp('KY.png',100,35)
        self.image = image
        # self.image = pg.Surface((w,h))
        self.image.set_colorkey(black)
        # self.image.fill(green)
        self.rect = self.image.get_rect()
        self.rect.centerx = width+100
        self.vx = randrange(1,2)
        self.rect.y = -500
        self.dy = 0.5
        # print(self.slide_speed)

    def update(self):

        self.rect.x -= self.vx
        center = self.rect.center
        self.rect = self.image.get_rect()
        # self.mask = pg.mask.from_surface(self.image)
        self.rect.center = center
        # self.rect.y += self.vy

        if self.rect.left > width + 100 or self.rect.right < -100:
            self.kill()
        if self.rect.top + 10 >= height :
            self.kill()
    def mp(self,picture,x,y):

        pic = pg.image.load(path.join('img',picture)).convert_alpha()
        pic = pg.transform.scale(pic,(x,y))
        return pic





class pow(pg.sprite.Sprite):
    def __init__(self,game,plat):
        self._layer = pow_layer
        self.group = game.all_sprites, game.powerup
        pg.sprite.Sprite.__init__(self,self.group)
        self.game = game
        self.plat = plat
        self.type = choice(['boost']) #70" width="71" y="1292" x="826

        self.image =self.mp('carrot.png')
        # self.image = pg.Surface((w,h))
        self.image.set_colorkey(black)
        # self.image.fill(green)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx 
        self.rect.bottom = self.plat.rect.top -5
    def mp(self,picture):

        pic = pg.image.load(path.join('img',picture)).convert_alpha()
        # pic = pg.transform.scale(pic,(x,y))
        return pic

    def update(self):
        self.rect.bottom = self.plat.rect.top -5
        if not self.game.platform.has(self.plat):
            self.kill()

class bur(pg.sprite.Sprite):
    def __init__(self,game,plat):
        self._layer = pow_layer
        self.group = game.all_sprites, game.bur
        pg.sprite.Sprite.__init__(self,self.group)
        self.game = game
        self.plat = plat
        self.type = choice(['bur']) #70" width="71" y="1292" x="826
        self.image =pg.image.load(path.join('img','bur.png')).convert_alpha()
        # self.image = pg.Surface((w,h))
        self.image.set_colorkey(black)
        # self.image.fill(green)
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.radius = 40
        self.rect.centerx = choice([self.plat.rect.right-20,self.plat.rect.left+20])
        self.rect.bottom = self.plat.rect.top + 15

    def update(self):
        self.rect.bottom = self.plat.rect.top + 15 
        self.rect.y += 1
        self.mask = pg.mask.from_surface(self.image)
        if not self.game.platform.has(self.plat):
            self.kill()

class coin(pg.sprite.Sprite):
    def __init__(self,game,plat):
        self.layer = coin_layer
        self.group = game.all_sprites,game.coin
        pg.sprite.Sprite.__init__(self,self.group)
        self.game = game
        self.plat = plat
        self.type = choice(['coin']) #70" width="71" y="1292" x="826
        self.image =pg.image.load(path.join('img','gold_1.png')).convert_alpha()
        # self.image = pg.Surface((w,h))
        self.image.set_colorkey(black)
        # self.image.fill(green)
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.radius = 40
        self.rect.centerx = choice([self.plat.rect.right-20,self.plat.rect.left+20,self.plat.rect.centerx])
        self.rect.bottom = self.plat.rect.top -10

    def update(self):
        self.rect.bottom = self.plat.rect.top -10
        self.rect.y += 1
        self.mask = pg.mask.from_surface(self.image)
        if not self.game.platform.has(self.plat):
            self.kill()




class ai(pg.sprite.Sprite):
    def __init__(self,game):
        self._layer = mob_layer
        self.group = game.all_sprites, game.ai
        pg.sprite.Sprite.__init__(self,self.group)
        self.game = game
        self.image_up = self.mp('monster.png')
        self.image_up.set_colorkey(black)
        self.image_down = self.mp('monster1.png')
        self.image_down.set_colorkey(black)
        self.image = self.image_up
        self.radius = 35
        self.rect = self.image.get_rect()
        # self.mask = pg.mask.from_surface(self.image)
        self.rect.centerx = choice([-100,width+100])
        self.vx = randrange(1,4)
        if self.rect.centerx > width:
            self.vx *= -1
        self.rect.y = -200
        self.vy = 0
        self.dy = 0.5
    def mp(self,picture):

        pic = pg.image.load(path.join('img',picture)).convert_alpha()
##        pic = pg.transform.scale(pic,(x,y))
        return pic


    def update(self):
        self.rect.x += self.vx
        self.vy += self.dy

        if self.vy > 3 or self.vy < -3:
            self.dy *= -1 

        center = self.rect.center
        if self.dy < 0:
            self.image = self.image_up
        else:
            self.image = self.image_down
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.center = center
        self.rect.y += self.vy

        if self.rect.left > width + 100 or self.rect.right < -100:
            self.kill()




class Spritesheet:
    def __init__(self,filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self,x,y,width,height):
        image = pg.Surface((width,height))
        image.blit(self.spritesheet,(0,0),(x,y,width,height))
        image = pg.transform.scale(image,((width*3)//8,(height*3)//8))
        return image


