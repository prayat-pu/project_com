# -*- coding: utf-8 -*-
# @Author: boss
# @Date:   2017-04-20 02:08:21
# @Last Modified by:   Pongsit
# @Last Modified time: 2017-04-25 06:23:44
import pygame as pg
import random
from os import path
from settings import *
from sprites import *
# from datetime import *


class game:
    def __init__(self):
        #initialize game window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((width, height))
        pg.display.set_caption(title)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(font_name)
        self.load_data()
        # bglist = ['b111.jpg','b2.jpg','b1111.jpg','gggg1.jpg']
        # self.background2 = pg.image.load(bglist[random.randrange(0,4)]).convert()
        self.dir = path.dirname(__file__)
        self.bg_dir = path.join(self.dir,'img')
        self.keep = 0
        self.background2 = pg.image.load(path.join(self.bg_dir,'b00.jpg')).convert_alpha()
        self.cross_y = 0
        self.background3 = pg.image.load(path.join(self.bg_dir,'b0.jpg')).convert_alpha()
        self.startbutton1 = pg.image.load(path.join(self.bg_dir,'start2.png')).convert_alpha()
        self.startbutton2 = pg.image.load(path.join(self.bg_dir,'start.png')).convert_alpha()
        self.cartoon = pg.image.load(path.join(self.bg_dir,'bunny2_hurt1.png')).convert_alpha()
        self.cartoon.set_colorkey(black)
        self.cartoon = pg.transform.scale(self.cartoon,(150,250))
        self.creditp = pg.image.load(path.join(self.bg_dir,'credit.png')).convert_alpha()


    def load_data(self):
        #hign score
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir,'img')
        with open(path.join(self.dir,hs_file),'r') as f:
            # self.highscore = int(f.read())
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

        #load spritesheet image
        self.spritesheet = Spritesheet(path.join(img_dir,spritesheet))
        #load sound 
        self.snd_dir = path.join(self.dir,'sound')
        self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir,'jump19.wav'))
        self.boost = pg.mixer.Sound(path.join(self.snd_dir,'powerup17.wav'))
        self.sndcoin = pg.mixer.Sound(path.join(self.snd_dir,'coin.wav'))


    def new(self):
        #reset the game
        self.score = 0
        self.lencoin = 0
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platform = pg.sprite.Group()
        self.powerup = pg.sprite.Group()
        self.ai = pg.sprite.Group()
        self.cloud = pg.sprite.Group()
        self.bur = pg.sprite.Group()
        self.slideptr = pg.sprite.Group()
        self.slideptl = pg.sprite.Group()
        self.coin = pg.sprite.Group()
        self.player = player(self)
       

      
        for plat in platform_list:
            first_plat = True
            p = platform(self,*plat,first_plat)
        self.ai_time = 0 
        pg.mixer.music.load(path.join(self.snd_dir,'bgsound.wav'))
        self.run()
        

    def run(self):
        #game loop
        pg.mixer.music.play(-1)
        self.clock.tick(fps)
        self.playing = True
        bglist = [path.join(self.bg_dir,'b1.jpg'),path.join(self.bg_dir,'b2.jpg'),path.join(self.bg_dir,'b3.jpg'),path.join(self.bg_dir,'b4.jpg'),path.join(self.bg_dir,'b5.jpg'),path.join(self.bg_dir,'b6.jpg'),path.join(self.bg_dir,'b7.jpg')]
        self.background2 = pg.image.load(bglist[random.randrange(0,7)]).convert_alpha()
        while self.playing:
            self.clock.tick(fps)
            self.event()
            self.update()
            self.draw()

        pg.mixer.music.fadeout(500)


    def update(self):
        #game loop - update
        self.all_sprites.update()


        now = pg.time.get_ticks()
        # if now - self.ai_time > 1:
        # # if now - self.ai_time > 20:
        #     self.ai_time = now
        #     ai(self)


        #spawn a ai 
        # print(self.player.vel.y)
        if self.score < 5000:
            if now - self.ai_time > ai_freq + random.choice([-1000,-500,0,500,1000]):
                self.ai_time = now
                ai(self)
        # elif self.score > 7000:
        #     # if now - self.ai_time > ai_freq + random.choice([-1000,-500,0,500,1000]):
        #     if now - self.ai_time > ai_freq + random.choice([-1000,-500,0,500,1000]) - 1000 :
        #         self.ai_time = now
        #         ai(self)
        else:
            # if now - self.ai_time > ai_freq + random.choice([-1000,-500,0,500,1000]):
            if now - self.ai_time > ai_freq + random.choice([-1000,-500,0,500,1000]) - 1000 :
                self.ai_time = now
                ai(self)

        ai_hit = pg.sprite.spritecollide(self.player,self.ai,False,pg.sprite.collide_circle)

        if ai_hit:
            ai_low = ai_hit[0]    
            for i in ai_hit:
                if i.rect.bottom > ai_low.rect.bottom:
                    ai_low = i
            if self.player.pos.y > ai_low.rect.top and self.player.vel.y > 0:
                self.boost.play()
                self.player.vel.y = -20
                self.player.jumping = True 
                ai_low.rect.y += 100
            elif self.player.vel.y > -15.5:
                self.player.vel.y = -10 
                self.die = True
                self.playing = False




        #check if player hit a platform
        hits = pg.sprite.spritecollide(self.player,self.platform,False)
        hit_slider = pg.sprite.spritecollide(self.player,self.slideptr,False)
        hit_slidel = pg.sprite.spritecollide(self.player,self.slideptl,False)

        if self.player.vel.y > 0:
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.x < lowest.rect.right+15  and self.player.pos.x > lowest.rect.left-15: 
                    if self.player.pos.y < lowest.rect.centery:
                        self.player.pos.y = lowest.rect.top + 3
                        self.player.vel.y = 0
                        self.player.jumping = False

            if hit_slider:
                low = hit_slider[0]
                for hit in hit_slider:
                    if hit.rect.bottom > low.rect.bottom:
                        low = hit
                if self.player.pos.x < low.rect.right +15 and self.player.pos.x > low.rect.left -15 : 
                    if self.player.pos.y < low.rect.centery:
                        self.player.pos.y = low.rect.top + 5
                        self.player.pos.x += 1
                        self.player.vel.y = 0
                        self.player.jumping = False
            if hit_slidel:
                lo = hit_slidel[0]
                for hi_l in hit_slidel:
                    lo = hi_l
                if self.player.pos.x < lo.rect.right +15 and self.player.pos.x > lo.rect.left -15 : 
                    if self.player.pos.y < lo.rect.centery:
                        self.player.pos.y = lo.rect.top + 5
                        self.player.pos.x -= 1
                        self.player.vel.y = 0
                        self.player.jumping = False


        if randrange(10000) < 5 :
            # slide[random.randint(0,1)]
            slideptr(self)
        elif  10 <randrange(10000) < 15:
            slideptl(self)
            # time.sleep(10)



        if len(self.platform) == 7:
        # if player go to top of screen
            if self.player.rect.top <= height/3:
                self.player.pos.y += abs(self.player.vel.y)
                for slide in self.slideptr:
                    slide.rect.y += max(abs(self.player.vel.y),2)
                for slide in self.slideptl:
                    slide.rect.y += max(abs(self.player.vel.y),2)
                for mob in self.ai:
                    mob.rect.y += max(abs(self.player.vel.y),2)
                for plat in self.platform:
                    plat.rect.y += abs(self.player.vel.y)
                    if plat.rect.top >= height or self.player.vel.y > 20:
                        plat.kill()
                        self.score += random.randrange(20,50)
            self.player.pos.y += 1
            for slide in self.slideptr:
                slide.rect.y += 2
            for slide in self.slideptl:
                slide.rect.y += 2
            for mob in self.ai:
                mob.rect.y += 1
            for plat in self.platform:
                plat.rect.y += 1
                if plat.rect.top >= height or self.player.vel.y > 20:
                    plat.kill()
                    self.score += random.randrange(20,50)

        pow_hit= pg.sprite.spritecollide(self.player,self.powerup,True)

        for pow_ in pow_hit:
            if pow_.type == 'boost':
                self.boost.play()
                self.player.vel.y = -boost_power
                self.player.jumping = True

        bur_hit= pg.sprite.spritecollide(self.player,self.bur,False,pg.sprite.collide_circle)
        for bur in bur_hit:
            if bur.rect.bottom < 0:
                bur.kill()
        if bur_hit and self.player.vel.y > -0.5 and self.player.pos.y < bur.rect.bottom:
            self.player.vel.y = -10
            self.die = True 
            self.playing = False

        coin_hit = pg.sprite.spritecollide(self.player,self.coin,True)

        if coin_hit:
            self.sndcoin.play()
            self.lencoin += 1

        for coin in coin_hit:
            if coin.type == 'coin':
                if coin.rect.bottom < 0:
                    coin.kill()



        

        #die
        if self.player.rect.bottom > height:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y,5)
                if sprite.rect.bottom < 0 :
                    sprite.kill()

        # if self.player.rect.center == height:
        #     self.playing = False

        if len(self.platform) == 0:
            falling_sound = pg.mixer.Sound('falling.WAV')
            pg.mixer.Sound.play(falling_sound)
            self.playing = False


        # new platform to keep some average 
        while len(self.platform) < 7 and self.player.vel.y < 16:
            # p = platform
            wid = random.randrange(50,100)
            first_plat = False
            platform(self,random.choice([0,150,300]),-30,first_plat)

   
            
 
    def event(self):
        # game loop - event
        # self.player.jump()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE or event.key == pg.K_UP:
                    self.player.jump()


    def draw(self):
        #game loop - draw
        #self.screen.fill(blue)
        self.screen.blit(self.background2, (0,0))
        self.all_sprites.draw(self.screen)
        # self.screen.blit(self.player.image,self.player.rect)

        len_score= len(str(self.score))
        self.draw_text("score : " + str(self.score),26,green,width*3/20+(len_score*3),15)
        self.draw_text('coin : ' +str(self.lencoin),26,yellow,width -100,15)
        # after drawing anything,flip the display
        pg.display.flip()


    def show_start_screen(self):

        pg.mixer.music.load(path.join(self.snd_dir,'Yippee.wav'))
        pg.mixer.music.play(-1)
        background = pg.image.load(path.join(self.bg_dir,'b1.jpg')).convert()
        self.screen.blit(background, (0,0))
        #first screen

        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)
    def text_start(self):
        logo = pg.image.load(path.join(self.bg_dir,'logo.png')).convert_alpha()
        logo.set_colorkey(black)
        self.screen.blit(logo,(width/10,height/5))
        # self.draw_text(title,48,purple,width/2,height/4)
        self.draw_text('Arrow to move space to jump',22,yellow,width/2,height/2)
        # self.draw_text('press a key to play',22,white,width/2,height*3/4)
        self.draw_text('high score : '+str(self.highscore),22,white,width/2,15)



    def show_over_screen(self):
        #game over screen
        if not self.running:
            return
        pg.mixer.music.load(path.join(self.snd_dir,'Yippee.wav'))
        pg.mixer.music.play(-1)
        self.screen.blit(self.background3, (0,0))
        pg.display.flip()
        self.wait_for_key2()
        self.cross_y = 0
        pg.mixer.music.fadeout(500)

    def gg(self):
        self.draw_text('Game over',50,red,width/2,25)
        self.draw_text('X coin : ' +str(self.lencoin),27,yellow,width/2,70)
        #self.draw_text('yourscore : ' +str(self.score+self.lencoin),26,white,width/2,15)

        if self.lencoin != 0:
            lastscore = self.score*self.lencoin
            self.draw_text('your score: ' + str(lastscore),28,white,width/2,100)
        else:
            lastscore = self.score
            self.draw_text('your score: ' + str(lastscore),28,white,width/2,100)
            
        if lastscore > self.highscore:
            self.highscore = lastscore
            self.draw_text('New high score!!!',32,yellow,width/2,height/2+48)
            with open(path.join(self.dir,hs_file),'w') as f:
                f.write(str(self.highscore))
                
        else:
            self.draw_text('High score: ' + str(self.highscore),30,white,width/2,height - 100)

    def credit(self):
        background = pg.image.load(path.join(self.bg_dir,'b1.jpg')).convert()
        self.screen.blit(background, (0,0))
        self.screen.blit(self.creditp, (40,10))

    def click(self,message,x,y,w,h,c1,c2,show):
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        c1 = pg.transform.scale(c1,(w,h))
        c2 = pg.transform.scale(c2,(w,h))

        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            if show == 1:
                self.screen.blit(c1, (x,y))
            if click[0] == 1:
                if message == 'Start' or message == 'Play Again':
                    return False
                if message == 'Credit':
                    self.credit()
                    return 3
                elif message == 'Quit':
                    quit()
        else:
            if show == 1:
                self.screen.blit(c2, (x,y))

        if show == 1:
            self.draw_text(message,22,white,x+(w/2),y)


    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(fps)
            background = pg.image.load(path.join(self.bg_dir,'b1.jpg')).convert()
            self.screen.blit(background, (0,0))
            if self.click('Credit',8,600,110,35,self.startbutton1,self.startbutton2,1) == 3:
                self.credit()
                
            else:
                self.click('Start',170,380,150,35,self.startbutton1,self.startbutton2,1)
                self.click('Quit',170,420,150,35,self.startbutton1,self.startbutton2,1)
                self.text_start()

            if self.click('Start',170,380,150,35,self.startbutton1,self.startbutton2,0) is False:
                waiting = False
            pg.display.flip()
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False

    def wait_for_key2(self):
        waiting = True
        while waiting:

            
            self.screen.blit(self.cartoon,(160,self.cross_y))
            self.clock.tick(fps)
            if self.cross_y < 150:     
                self.cross_y += 3
                pg.display.flip()
                self.screen.blit(self.background3, (0,0))
            else:
                self.click('Play Again',80,450,150,35,self.startbutton1,self.startbutton2,1)
                self.click('Quit',250,450,150,35,self.startbutton1,self.startbutton2,1)
                self.gg()
                pg.display.flip()
        
            if self.click('Play Again',80,450,150,35,self.startbutton1,self.startbutton2,0) is False:
                waiting = False
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False

    def draw_text(self,text,size,color,x,y):

        font = pg.font.Font(self.font_name,size)
        text_surface = font.render(text,True,color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface,text_rect)

g = game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_over_screen()

quit()





