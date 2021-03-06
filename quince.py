import pygame, sys
import pygame.freetype
import pygame.sysfont
from pygame import Rect

tilesize = 128
fontsize = 15

sprite_height = tilesize
sprite_width = tilesize
screen_width = 1024
screen_height = 1024
world_width = 100
world_height = 100

tiles_per_row = screen_width / tilesize
tiles_per_col = screen_height / tilesize

left = 0
front = 1
back = 2
right = 3

class Game:
    def __init__(self):
        self.screen = MainMenu(self)
        self.fonter = FontManager("cousine", fontsize, bold=True)
        self.soundman = SoundManager()

    def switch_screen(self, screen):
        self.screen = screen

    def key_pressed(self, key_char):
        self.screen.key_pressed(key_char)

    def update():
        pass

    def draw(self, surface):
        self.screen.draw(surface)

class WorldObject:
    def __init__(self, world):
        self.world = world

class FontManager:
    def __init__(self, name, size, **kwargs):
        self.font = self.get_font(name, size, **kwargs)

    def get_font(self, name, size, **kwargs):
        return pygame.freetype.SysFont(name, size, **kwargs)

    def draw(self, surface, pos, text, color):
        self.font.render_to(surface, pos, text, color)

class SoundManager:
    def __init__(self):
        self.sounds = []
        self.sounds.append(pygame.mixer.Sound("assets/sound/hit.wav"))
        self.sounds.append(pygame.mixer.Sound("assets/sound/select.wav"))

    def play(self, index):
        self.sounds[index].play()

    def stop(self, index):
        self.sounds[index].stop()

class MusicManager:
    def load(filename):
        pygame.mixer.music.load(filename)

    def play():
        pygame.mixer.music.play()

    def stop():
        pygame.mixer.music.fadeout(250)

    def update(self):
        pass

class Screen:
    def __init__(self, game):
        self.game = game

    def key_pressed(self, key_char):
        pass

    def draw(self, surface):
        pass

    def update(self, delta):
        pass

class Menu(Screen):
    def __init__(self, game, items):
        Screen.__init__(self, game)
        self.items = items
        self.selected = 0

    def key_pressed(self, key_char):
        i = 0
        if key_char == pygame.K_w or key_char == pygame.K_UP:
            i -= 1
            self.game.soundman.play(0)
        if key_char == pygame.K_s or key_char == pygame.K_DOWN:
            i += 1
            self.game.soundman.play(0)

        self.selected += i

        if self.selected < 0:
            self.selected = len(self.items)-1
        if self.selected >= len(self.items):
            self.selected = 0

        if key_char == pygame.K_RETURN:
            self.items[self.selected].action()
            self.game.soundman.play(0)

    def draw(self, surface):
        for (i, item) in enumerate(self.items):
            color = pygame.Color(255, 255, 255)
            if i == self.selected:
                color = pygame.Color(255, 0, 100)
            rect = self.game.fonter.font.get_rect(item.text, size = fontsize)
            self.game.fonter.draw(surface, ((screen_width/2) - ((rect.right - rect.left)/2), (screen_height/2)+(((rect.bottom - rect.top)+5)*i)), item.text, color)

class MainMenu(Menu):
    def __init__(self, game):
        items = []
        items.append(MenuItem("NEW GAME", lambda: self.game.switch_screen(World(self.game, world_height, world_width))))
        items.append(MenuItem("CREDITS", lambda: self.game.switch_screen(CreditsMenu(self.game))))
        items.append(MenuItem("EXIT", lambda: sys.exit()))
        Menu.__init__(self, game, items)

    def key_pressed(self, key_char):
        if key_char == pygame.K_q:
            sys.exit()

        Menu.key_pressed(self, key_char)

class CreditsMenu(Menu):
    def __init__(self, game):
        MusicManager.load("assets/music/tomato.ogg")
        MusicManager.play()
        items = []
        items.append(MenuItem("Crafted by Anchovieshat", lambda: None))
        Menu.__init__(self, game, items)
        self.selected = -1

    def key_pressed(self, key_char):
        if key_char == pygame.K_q:
            MusicManager.stop()
            self.game.switch_screen(MainMenu(self.game))

        Menu.key_pressed(self, key_char)
        self.selected = -1

class MenuItem():
    def __init__(self, text, action):
        self.text = text
        self.action = action

class World(Screen):
    def __init__(self, game, width, height):
        Screen.__init__(self, game)

        music_list = []
        music_list.append("assets/music/ghosts-of-tofus.ogg")

        MusicManager.load(music_list[0])
        MusicManager.play()

        self.entity_map = load_sprite("assets/sprites/entitiesx128.png", sprite_width, sprite_height)
        self.tile_map = load_sprite("assets/sprites/tilesx128.png", sprite_width, sprite_height)

        self.game_map = []
        self.width = width
        self.height = height

        temp_surf = pygame.Surface((tilesize, tilesize))

        for x in range(0, width):
            line = []
            self.game_map.append(line)
            for y in range(0, height):
                if y % 2 == 0 and x % 2 == 0:
                    surf = temp_surf.copy()
                    surf.fill(((y*10) % 255, (x*10)%255, (x*2)%255, 255))
                    line.append(Tile(self, surf))
                else:
                    line.append(Tile(self, self.tile_map[0][0]))
        self.monsters = []
        self.monsters.append(Monster(self, self.entity_map[1], 1, 1))

        self.player = Player(self, self.entity_map[0], 0, 0)
        self.center()

    def center(self):
        x = self.player.x
        y = self.player.y

        x = x - (tiles_per_row//2)
        y = y - (tiles_per_col//2)

        if x+tiles_per_row > self.width:
            x = self.view.left
        if x < 0:
            x = 0
        if y+tiles_per_col-1 > self.height:
            y = self.view.top
        if y < 0:
            y = 0

        self.view = Rect((x,y),(x+tiles_per_row,y+tiles_per_col-1))

    def key_pressed(self, key_char):
        if key_char == pygame.K_w:
            self.player.move(0, -1)
        if key_char == pygame.K_s:
            self.player.move(0, 1)
        if key_char == pygame.K_a:
            self.player.move(-1, 0)
        if key_char == pygame.K_d:
            self.player.move(1, 0)
        if key_char == pygame.K_q:
            MusicManager.stop()
            self.game.switch_screen(MainMenu(self.game))

    def draw(self, surface):
        for x in range(self.view.left, self.view.width):
            for y in range(self.view.top, self.view.height):
                self.game_map[x][y].draw(surface, (x-self.view.left)*tilesize, (y-self.view.top+1)*tilesize)

class Tile(WorldObject):
    def __init__(self, world, sprite):
        WorldObject.__init__(self, world)
        self.sprite = sprite
        self.entities = []

    def add_entity(self, entity):
        self.entities.append(entity)

    def remove_entity(self, entity):
        self.entities.remove(entity)

    def is_collidable(self):
        for entity in self.entities:
            if entity.is_collidable():
                return True
        return False

    def collide(self, collider):
        for entity in self.entities:
            entity.collide(collider)

    def draw(self, surface, x, y):
        surface.blit(self.sprite, (x, y))

        for entity in self.entities:
            entity.draw(surface, x, y-(sprite_height/2))

class Entity(WorldObject):
    def __init__(self, world, sprites, x, y):
        WorldObject.__init__(self, world)
        world.game_map[x][y].add_entity(self)
        self.sprites = sprites
        self.x = x
        self.y = y
        self.anim_state = 0

    def move(self, x, y):
        self.move_to(self.x + x, self.y + y)

    def remove(self):
        self.world.game_map[self.x][self.y].remove_entity(self)

    def is_collidable(self):
        return True

    def collide(self, collider):
        pass

    def move_to(self, x, y):
        self.world.game_map[self.x][self.y].remove_entity(self)
        self.world.game_map[x][y].add_entity(self)

        self.x = x
        self.y = y

    def draw(self, surface, x, y):
        surface.blit(self.sprites[self.anim_state], (x, y))

    def turn(self, direction):
        if len(self.sprites) < direction:
            return
        self.anim_state = direction

class Player(Entity):
    skin_color = pygame.Color(203, 203, 203)
    bag_color = pygame.Color(152, 152, 152)
    shirt_color = pygame.Color(136, 136, 136)
    hat_rim_color = pygame.Color(123, 123, 123)
    hat_color = pygame.Color(94, 94, 94)
    boots_color = pygame.Color(84, 84, 84)

    def __init__(self, world, sprites, x, y):
        Entity.__init__(self, world, [], x, y)
        self.original = sprites
        for sprite in sprites:
            sprite = sprite.copy()
            px = pygame.PixelArray(sprite)
            px.replace(self.skin_color, pygame.Color(255, 200, 190)) #Skin
            px.replace(self.bag_color, pygame.Color(114, 49, 17)) #Bag
            px.replace(self.shirt_color, pygame.Color(19, 67, 155)) #Body
            px.replace(self.hat_rim_color, pygame.Color(27, 72, 155)) #Hat Rim
            px.replace(self.hat_color, pygame.Color(32, 85, 181)) #Hat
            px.replace(self.boots_color, pygame.Color(103, 61, 42)) #Boots
            self.sprites.append(sprite)

    def move_to(self, x, y):
        if self.x > x:
            self.turn(left)
        elif self.x < x:
            self.turn(right)
        if self.y > y:
            self.turn(back)
        elif self.y < y:
            self.turn(front)

        if x >= self.world.width:
            return
        if x < 0:
            return
        if y >= self.world.height:
            return
        if y < 0:
            return

        if not self.world.game_map[x][y].is_collidable():
            Entity.move_to(self, x, y)
            self.world.center()

        else:
            self.world.game_map[x][y].collide(self)
            self.world.game.soundman.play(0)

class Monster(Entity):
    body_color = pygame.Color(136, 136, 136)

    def __init__(self, game, sprites, x, y):
        Entity.__init__(self, game, [], x, y)
        self.original = sprites
        for sprite in sprites:
            sprite = sprite.copy()
            px = pygame.PixelArray(sprite)
            px.replace(self.body_color, pygame.Color(19, 67, 155)) #Body
            self.sprites.append(sprite)

    def collide(self, collider):
        self.remove()

    def move_to(self, x, y):
        if self.x > x:
            self.turn(left)
        elif self.x < x:
            self.turn(right)
        if self.y > y:
            self.turn(back)
        elif self.y < y:
            self.turn(front)

        if x >= self.game.world.width:
            return
        if x < 0:
            return
        if y >= self.game.world.height:
            return
        if y < 0:
            return
        Entity.move_to(self, x, y)

def load_sprite(filename, width, height):
    image = pygame.image.load(filename).convert_alpha()
    image_width, image_height = image.get_size()
    sprite_table = []
    for sprite_y in range(0, int(image_height/height)):
        line = []
        sprite_table.append(line)
        for sprite_x in range(0, int(image_width/width)):
            rect = (sprite_x*width, sprite_y*height, width, height)
            line.append(image.subsurface(rect))
    return sprite_table

if __name__=='__main__':
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.DOUBLEBUF, 32)
    clock = pygame.time.Clock()

    game = Game()
    pygame.key.set_repeat(500, 30)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                game.key_pressed(event.key)

        screen.fill((0,0,0,0))

        game.draw(screen)

        pygame.display.flip()
        clock.tick(60)

