# shoot them up
import pygame
import random
import os


class Player(pygame.sprite.Sprite):
    # sprite for player

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        img_path = os.path.join(Game.image_folder, "playerShip1_orange.png")
        self.image = pygame.image.load(img_path)
        self.image = pygame.transform.scale(self.image, (50,38))
        self.mini_image = pygame.transform.scale(self.image, (21, 19))
        self.life = 3
        self.rect = self.image.get_rect()

        self.radius = 10
        #pygame.draw.circle(self.image, Game.RED, self.rect.center, self.radius)

        self.rect.centerx = Game.WIDTH/2
        self.rect.bottom = Game.HEIGHT - 10


        self.speed_x = 0

        self.shoot_sound = pygame.mixer.Sound(os.path.join(Game.sound_folder, "laser.ogg"))

        self.shield = 100

        self.last_shoot = pygame.time.get_ticks()
        #毫秒
        self.shoot_delay = 200
        self.last_death = pygame.time.get_ticks()
        self.death_delay = 1500
        self.hidden = False
        #powerups
        self.power = 1
        self.powerup_timer = pygame.time.get_ticks()

    def powerup(self):
        self.power+=1
        self.powerup_timer = pygame.time.get_ticks()




    def health_bar(self):
        bar_length = self.image.get_rect().width
        bar_height = 3

        fill_length = (self.shield/100)* bar_length
        #red
        outline_rect = pygame.Rect(0, self.rect.height-bar_height ,bar_length,bar_height)
        #green
        fill_rect = pygame.Rect(0, self.rect.height-bar_height ,fill_length ,bar_height)

        self.image.fill(Game.RED, outline_rect)
        self.image.fill(Game.GREEN, fill_rect)



# find out which key is pressed, and action after the key pressed
    def update(self):
        now = pygame.time.get_ticks()
        if self.power >= 2 and now - self.powerup_timer > Game.POWERUP_TIME:
            self.power -= 1
            self.powerup_timer = now

        if self.hidden and pygame.time.get_ticks() - self.last_death > self.death_delay:
            print("unhidden")
            self.hidden = False
            self.rect.centerx = Game.WIDTH/2
            self.rect.bottom = Game.HEIGHT - 10

        self.speed_x = 0

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_LEFT]:
            self.speed_x = -5

        elif key_pressed[pygame.K_RIGHT]:
            self.speed_x = 5

        self.rect.x += self.speed_x

        if self.rect.right > Game.WIDTH:
            self.rect.right = Game.WIDTH

        elif self.rect.left < 0:
            self.rect.left = 0

        self.rect.x += self.speed_x

        self.health_bar()


    def hide(self):
        self.hidden = True
        self.last_death = pygame.time.get_ticks()
        self.rect.centerx = Game.WIDTH/2
        self.rect.top = Game.HEIGHT


    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shoot > self.shoot_delay:
            self.last_shoot = now

        if self.power == 1:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            Game.all_sprites.add(bullet)
            Game.bullets.add(bullet)

        elif self.power >= 2:
            bullet1 = Bullet(self.rect.left, self.rect.top)
            bullet2 = Bullet(self.rect.right, self.rect.top)
            Game.all_sprites.add(bullet1)
            Game.bullets.add(bullet1)
            Game.all_sprites.add(bullet2)
            Game.bullets.add(bullet2)
        self.shoot_sound.play()


class Bullet(pygame.sprite.Sprite):
    #direction = "up this will be defult if i don't give value"
    #add color
    def __init__(self, x, y, direction = "up"):
        pygame.sprite.Sprite.__init__(self)
        img_path = os.path.join(Game.image_folder, "laserRed16.png")
        self.image = pygame.image.load(img_path)
        self.rect = self.image.get_rect()

        self.direction = direction
        if self.direction == "up":
            self.speed_y = -10
        else:
            self.speed_y = 10
            self.image = pygame.transform.rotate(self.image, 180)

        self.rect.centerx = x
        self.rect.top = y

    def update(self):
        self.rect.y += self.speed_y

        if self.rect.bottom < 0 or self.rect.top> Game.HEIGHT:
            self.kill()

class Explosion(pygame.sprite.Sprite):

    explosion_animation = {}
    explosion_animation["large"] = []
    explosion_animation["small"] = []
    explosion_animation["player"] = []
    explosion_folder = os.path.join(os.getcwd(), "image/explosion")

    @staticmethod
    def init():
        for i in range(9):
            filename = "regularExplosion0{}.png".format(i)
            image = pygame.image.load(os.path.join(Explosion.explosion_folder,filename))
            image_large = pygame.transform.scale(image, (75, 75))
            image_small = pygame.transform.scale(image, (42, 42))
            Explosion.explosion_animation["large"].append(image_large)
            Explosion.explosion_animation["small"].append(image_small)
        for a in range(9):
            filename01 = "sonicExplosion0{}.png".format(a)
            image = pygame.image.load(os.path.join(Explosion.explosion_folder, filename01))
            image_player = pygame.transform.scale(image, (65, 65))
            Explosion.explosion_animation["player"].append(image_player)

    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = Explosion.explosion_animation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now

            self.frame += 1
            if self.frame == len(Explosion.explosion_animation[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = Explosion.explosion_animation[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Enemy(pygame.sprite.Sprite):
    move_type = ["to_left", "to_right", "bounce", "default"]

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        enemy_files = ["enemyBlack1.png", "enemyBlue2.png", "enemyGreen4.png", "enemyRed5.png"]

        filename = random.choice(enemy_files)

        enemy_image_folder = os.path.join(Game.image_folder, "enemies")

        image = pygame.image.load(os.path.join(enemy_image_folder, filename))

        self.image = pygame.transform.scale(image, (50,38))
        self.rect = self.image.get_rect()

        self.speed_x = random.randrange(1,3)
        self.speed_y = random.randrange(1,3)

        self.type = random.choice(Enemy.move_type)

        self.rect_y = -40
        print(self.type)
        if self.type == "to_left":
            self.rect.x = Game.WIDTH - self.rect.width
        elif self.type == "to_right":
            self.rect.x = self.rect.width
        elif self.type == "bounce":
            self.rect.x = random.randrange(self.rect.width, Game.WIDTH- self.rect.width)
            self.speed_x = random.randrange(3, 6)
        else:
            self.rect.x = random.randrange(self.rect.width, Game.WIDTH - self.rect.width)

        self.damage = 95
        self.score = 5

        self.ebullet_timer = pygame.time.get_ticks()
        self.e_fre = 1000
    def update(self):
        self.rect.y += self.speed_y

        if self.type == "to_left":
            self.rect.x -= self.speed_x
        elif self.type == "to right":
            self.rect.x += self.speed_x
        elif self.type == "bounce":
            if self.rect.left <= 0 or self.rect.right >= Game.WIDTH:
                self.speed_x = self.speed_x * -1

            if self.rect.left < 0:
                self.rect.left = 0
            elif self.rect.right>Game.WIDTH:
                self.rect.right = Game.WIDTH

            self.rect.x += self.speed_x
        else: #defult
            pass

        if self.rect.height > Game.HEIGHT or self.rect.right< 0 or self.rect.left > Game.WIDTH:
            self.kill()
        now = pygame.time.get_ticks()
        if now - self.ebullet_timer > self.e_fre:
            self.ebullet_timer = now

            self.shoot()

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.bottom, "down")
        Game.all_sprites.add(bullet)
        Game.enemy_bullets.add(bullet)


class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.rock_files = ["meteorGrey_med2.png", "meteorGrey_tiny1.png", "meteorGrey_big4.png", "meteorGrey_big1.png"]

        filename = random.choice(self.rock_files)

        self.rock_image_folder = os.path.join(Game.image_folder, "rock")

        self.org_image = pygame.image.load(os.path.join(self.rock_image_folder, filename))
        self.image = self.org_image
        self.rect = self.image.get_rect()

        self.speed_x = random.randrange(-3, 3)
        self.speed_y = random.randrange(1, 8)

        self.rect.x = random.randrange(Game.WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        Rock = pygame.sprite.Group()

        self.rotation = 0
        self.rotation_speed = random.randrange(-10, 10)
        self.last_tick = pygame.time.get_ticks()

        self.damage = 1
        self.score = 1

        if self.rect.width < 20:
            self.score = 10
            self.damage = 10
        elif self.rect.width <30:
            self.score = 8
            self.damage = 30
        elif self.rect.width < 50:
            self.score = 4
            self.damage = 50
        else:
            self.score = 1
            self.damage = 70

#Hw random size rock, add another folder in image(put different sizes of rock inside, random rock sizes)

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_tick > 50:
            self.last_tick = now
            new_image = pygame.transform.rotate(self.org_image, self.rotation)
            self.rotation = (self.rotation + self.rotation_speed) % 360

            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()


        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.right < 0 or self.rect.left > Game.WIDTH or self.rect.top > Game.HEIGHT:
            self.speed_x = random.randrange(-3, 3)
            self.speed_y = random.randrange(1, 8)

            self.rect.x = random.randrange(Game.WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)

class Powerups(pygame.sprite.Sprite):
    powerup_files = {}
    powerup_files["shield"]="shield_gold.png"
    powerup_files["bolt"]= "bolt_gold.png"
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        Powerups.powerup_image_folder = os.path.join(Game.image_folder, "powerups")
        self.type = random.choice(list(Powerups.powerup_files.keys()))
        self.image = pygame.image.load(os.path.join(Powerups.powerup_image_folder, Powerups.powerup_files[self.type]))
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speed_y = random.randrange(3, 6)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > Game.HEIGHT:
            self.kill()


class Game():
    WIDTH = 480
    HEIGHT = 600
    FPS = 30

    POWERUP_TIME= 5000

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    enemy = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()


    image_folder = os.path.join(os.getcwd(), "image")

    sound_folder = os.path.join(os.getcwd(), "sound")

    def __init__(self):
        # initialize pygame and create a window
        pygame.init()

        #for sound(必须有，不然声音是无法出现的）
        pygame.mixer.init()

        #load background music
        pygame.mixer.music.load(os.path.join(Game.sound_folder, "background.mp3"))
        #pygame.mixer.music.set_volume(0.4)    控制音量

        self.screen = pygame.display.set_mode((Game.WIDTH, Game.HEIGHT))
        pygame.display.set_caption("Shmup")
        self.clock = pygame.time.Clock()

        self.player = Player()
        Game.all_sprites.add(self.player)

        self.enemies = pygame.sprite.Group()


        for i in range(8):
            self.new_rock()

        self.background = pygame.image.load(os.path.join(Game.image_folder, "background.jpg"))
        self.background_rect = self.background.get_rect()



        self.score = 0
        self.font_name = pygame.font.match_font("arial")

        self.enemy_timer = pygame.time.get_ticks()
        self.enemy_frequency = 5000
        Explosion.init()
    def new_rock(self):
        r = Rock()
        self.enemies.add(r)
        Game.all_sprites.add(r)

#True 抗锯齿
    def draw_text(self, surface, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, Game.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)
        #blit 是把一个surface贴到另一个surface上面

    def draw_player_lives(self, surface, x, y):
        for i in range(self.player.life):
            img_rect = self.player.mini_image.get_rect()
            img_rect.x = x + 35*i
            img_rect.y = y
            #paste image
            surface.blit(self.player.mini_image, img_rect)

    def show_start_screen(self):
        self.screen.blit(self.background, self.background_rect)

        self.draw_text(self.screen, "SPACE WAR", 64, Game.WIDTH/2,Game.HEIGHT/4)
        self.draw_text(self.screen, "Press space key to shoot & Use arrow key to move left or right", 22, Game.WIDTH/2, Game.HEIGHT/2)
        self.draw_text(self.screen, "Press ANYKEY to start", 58, Game.WIDTH/2, (Game.HEIGHT/4)*3)
        pygame.display.flip()

        waiting = True

        while waiting:
            self.clock.tick(Game.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYUP:
                    waiting = False


    def reset(self):
        Game.bullets.empty()
        self.enemies.empty()
        Game.all_sprites.empty()
        Game.powerups.empty()

        for i in range(8):
            self.new_rock()
        self.player = Player()
        Game.all_sprites.add(self.player)

        self.score = 0
    def add_an_enemy(self):
        now = pygame.time.get_ticks()
        if now - self.enemy_timer > self.enemy_frequency:
            self.enemy_timer = now
            self.enemy_frequency = random.randint(2000, 5000)
            e = Enemy()
            Game.all_sprites.add(e)
            self.enemies.add(e)


    def gameloop(self):

        self.good_to_go = True


        #gameloop
        self.running = True
        self.hit_sound = pygame.mixer.Sound(os.path.join(Game.sound_folder, "explosion.wav"))
        #start to play background music
        pygame.mixer.music.play(loops = -1)
        while self.running:
            if self.good_to_go:
                self.show_start_screen()
                self.good_to_go = False

                self.reset()

            #keep loop running at a right speed
            self.clock.tick(Game.FPS)

            #process input (events)
            for event in pygame.event.get():
                #check for close the window
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.shoot()

#HW, player hits the rock, player die. game,quit.
#02. bullets hits the rock, rock dissappear, bullet dissappear
            #update
            Game.all_sprites.update()
            self.add_an_enemy()

            hits = pygame.sprite.spritecollide(self.player, self.enemies, True, pygame.sprite.collide_circle)

            for hit in hits:
                self.player.shield -= hit.damage
                self.new_rock()
                if self.player.shield<=0:
                    death_explosion = Explosion(self.player.rect.center, "player")
                    Game.all_sprites.add(death_explosion)
                    self.player.life -= 1
                    self.player.hide()
                    self.player.shield = 100
                    print(self.player.life)
                if self.player.life == 0:
                    print("good to go: False")
                    self.good_to_go = True

                explosion = Explosion(hit.rect.center, "small")
                Game.all_sprites.add(explosion)

            hits1 = pygame.sprite.groupcollide(self.enemies, Game.bullets, True, True)


            for hit in hits1:
                self.score += hit.score
                print(self.score)
                self.hit_sound.play()

                explosion = Explosion(hit.rect.center, "large")
                Game.all_sprites.add(explosion)
                # random.random() give 小数点 here, you can use random, range() or random.randint()
                if random.random()> 0.5:
                    powerups = Powerups(hit.rect.center)
                    Game.all_sprites.add(powerups)
                    Game.powerups.add(powerups)
                self.new_rock()

            hits2 = pygame.sprite.spritecollide(self.player, self.powerups, True)

            for hit in hits2:
                if hit.type == "shield":
                    self.player.shield += 30
                    if self.player.shield > 100:
                        self.player.shield = 100

                if hit.type == "bolt":
                    self.player.powerup()
            #hits4 = pygame.groupcollide(Game.enemy_bullets, Game.bullets, True, True)
            #for hit in hits4:
                #self.kill()
            hits3 = pygame.sprite.spritecollide(self.player, Game.enemy_bullets, True)
            for hit in hits3:
                self.player.shield -= 45
                if self.player.shield<=0:
                    death_explosion = Explosion(self.player.rect.center, "player")
                    Game.all_sprites.add(death_explosion)
                    self.player.life -= 1
                    self.player.hide()
                    self.player.shield = 100
                    print(self.player.life)
                if self.player.life == 0:
                    print("good to go: False")
                    self.good_to_go = True

               # explosion = Explosion(hit.rect.center, "small")
               # Game.all_sprites.add(explosion)

           #render / draw
            self.screen.blit(self.background, self.background_rect)
            Game.all_sprites.draw(self.screen)

            self.draw_text(self.screen, str(self.score), 36, Game.WIDTH/2, 20)
            self.draw_player_lives(self.screen, Game.WIDTH- 100,20)

            #after drawing everything. flip the display
            pygame.display.flip()

            #pygame.display.update()

        pygame.quit()

game = Game()
game.gameloop()
