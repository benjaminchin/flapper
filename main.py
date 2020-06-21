import pygame as pg
import random
from settings import *
from sprites import *
from os import path


class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

        # create images
        self.bird_high_wing = self.spritesheet.get_image(3, 491, 18, 13)
        self.bird_high_wing.set_colorkey(BLACK)
        self.bird_mid_wing = self.spritesheet.get_image(31, 491, 18, 13)
        self.bird_mid_wing.set_colorkey(BLACK)
        self.bird_low_wing = self.spritesheet.get_image(59, 491, 18, 13)
        self.bird_low_wing.set_colorkey(BLACK)

        self.top_pipe = self.spritesheet.get_image(56, 323, 27, 161)
        self.top_pipe.set_colorkey(BLACK)
        self.bottom_pipe = self.spritesheet.get_image(85, 323, 27, 161)
        self.bottom_pipe.set_colorkey(BLACK)

        floor = pg.Surface((WIDTH, 40))
        floor.fill(GREEN)
        floor.set_colorkey(BLACK)
        self.floor = Platform(FLOOR_POS[0], FLOOR_POS[1], floor)
        
        """self.all_sprites.add(self.floor)
        self.platforms.add(self.floor)"""

    def load_data(self):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        with open(path.join(self.dir, HS_FILE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

        # load spritesheet image
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))

        sfx_dir = path.join(self.dir, 'sfx')

        self.sfx_point = pg.mixer.Sound(path.join(sfx_dir, 'sfx_point.wav'))
        self.sfx_die = pg.mixer.Sound(path.join(sfx_dir, 'sfx_die.wav'))
        self.sfx_hit = pg.mixer.Sound(path.join(sfx_dir, 'sfx_hit.wav'))
        self.sfx_swooshing = pg.mixer.Sound(path.join(sfx_dir, 'sfx_swooshing.wav'))
        self.sfx_wing = pg.mixer.Sound(path.join(sfx_dir, 'sfx_wing.wav'))

        self.sfx_point.set_volume(VOLUME)
        self.sfx_die.set_volume(VOLUME)
        self.sfx_hit.set_volume(VOLUME)
        self.sfx_swooshing.set_volume(VOLUME)
        self.sfx_wing.set_volume(VOLUME)
        
    def new(self):
        # start a new game
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self, [self.bird_high_wing, self.bird_mid_wing, self.bird_low_wing, self.bird_mid_wing])
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.floor)
        self.platforms.add(self.floor)
        for plat in PLATFORM_LIST:
            top_p = Platform(plat[0], -PIPE_HEIGHT + plat[1], self.top_pipe)
            bot_p = Platform(plat[0], plat[1] + PIPE_GAP, self.bottom_pipe)
            self.all_sprites.add(top_p)
            self.platforms.add(top_p)
            self.all_sprites.add(bot_p)
            self.platforms.add(bot_p)
            
        self.sfx_swooshing.play()
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        # check if player hits a platform - only if falling
        """if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0"""

        # if player reaches top 1/4 of screen
        """if self.player.rect.top <= HEIGHT / 4:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10"""
  
        # if player reaches right 1/2 of screen
        if self.player.rect.x + 15 > WIDTH / 2:
            self.player.pos.x -= abs(self.player.vel.x)
            plat_list = self.platforms.sprites()
            floor = plat_list[0]
            floor.rect.x += self.player.vel.x
            for plat in plat_list:
                plat.rect.x -= abs(self.player.vel.x)

        plat_list = self.platforms.sprites()
        del plat_list[0]
        for plat in plat_list:

            if plat.rect.right < 0:
                plat.kill()
                # self.score += 10
            """if plat.scored is False and self.player.pos.x > plat.rect.x:
                self.score += 0.5
                plat.scored = True"""
            if plat.image == self.top_pipe:
                if plat.scored is False and self.player.pos.x > plat.rect.x:
                    self.score += 1
                    plat.scored = True
                    self.sfx_point.play()

        # Die!
        if pg.sprite.spritecollide(self.player, self.platforms, False, pg.sprite.collide_mask):
            self.draw()
            self.sfx_hit.play()
            pg.time.wait(500)
            self.sfx_die.play()
            for sprite in self.all_sprites:
                # sprite.rect.y -= max(self.player.vel.y, 10)
                # if sprite.rect.bottom < 0:
                sprite.kill()
            self.all_sprites.empty()

        if len(self.platforms) == 0:
            self.playing = False

        # spawn new platforms to keep same average number
        while len(self.platforms) < 7:
            new_pipe = random.randint(0, PIPE_HEIGHT)
            """pipe1 = Platform(WIDTH + PIPE_SPREAD, 0, PIPE_WIDTH, PIPE_BUFFER + new_pipe)
            pipe2 = Platform(WIDTH + PIPE_SPREAD, new_pipe + PIPE_GAP + PIPE_BUFFER, PIPE_WIDTH,
                             HEIGHT - (new_pipe + PIPE_BUFFER))"""
            
            pipe1 = Platform(WIDTH + PIPE_SPREAD, -PIPE_HEIGHT + new_pipe, self.top_pipe)
            pipe2 = Platform(WIDTH + PIPE_SPREAD, new_pipe + 200, self.bottom_pipe)
            self.platforms.add(pipe1)
            self.platforms.add(pipe2)
            self.all_sprites.add(pipe1)
            self.all_sprites.add(pipe2)

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    if self.player.pos.y > 25:
                        self.player.jump()
                        self.sfx_wing.play()

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(int(self.score)), 22, WHITE, WIDTH / 2, 15)
        self.screen.blit(self.floor.image, FLOOR_POS)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Spacebar to jump", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to start", 22, WHITE, WIDTH / 2, HEIGHT * 3/4)
        self.draw_text("Highscore: " + str(self.highscore), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text("Game Over!", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(int(self.score)), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)

        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("New Highscore!", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(int(self.score)))
        else:
            self.draw_text("Highscore: " + str(int(self.highscore)), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)

        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
