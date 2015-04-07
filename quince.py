import pygame, sys
from pygame import Rect

tilesize = 128
sprite_height = tilesize
sprite_width = tilesize
screen_width = 1024
screen_height = 1024
tiles_per_row = screen_width / tilesize
tiles_per_col = screen_height / tilesize
left = 0
front = 1
back = 2
right = 3

class Game:
    def __init__(self, world_width, world_height):
        self.world = World(self, world_width, world_height)
        self.entity_map = load_sprite("assets/entitiesx128.png", sprite_width, sprite_height)
        self.player = Player(self, self.entity_map[0], 0, 0)
        self.monsters = []
        self.monsters.append(Monster(self, self.entity_map[1], 1, 1))
        self.center_world()

    def center_world(self):
        x = self.player.x
        y = self.player.y

        x = x - (tiles_per_row//2)
        y = y - (tiles_per_col//2)

        if x+tiles_per_row > self.world.width:
            x = self.view.left
        if x < 0:
            x = 0
        if y+tiles_per_col-1 > self.world.height:
            y = self.view.top
        if y < 0:
            y = 0

        self.view = Rect((x,y),(x+tiles_per_row,y+tiles_per_col-1))

    def draw(self, surface):
        self.world.draw(self.view, surface)

class GameObject:
    def __init__(self, game):
        self.game = game

class World(GameObject):
    def __init__(self, game, width, height):
        GameObject.__init__(self, game)
        self.tile_map = load_sprite("assets/tilesx128.png", sprite_width, sprite_height)
        self.width = width
        self.height = height
        self.game_map = []
        temp_surf = pygame.Surface((tilesize, tilesize))
        for x in range(0, width):
            line = []
            self.game_map.append(line)
            for y in range(0, height):
                if y % 2 == 0 and x % 2 == 0:
                    surf = temp_surf.copy()
                    surf.fill(((y*10) % 255, (x*10)%255, (x*2)%255, 255))
                    line.append(Tile(game, surf))
                else:
                    line.append(Tile(game, self.tile_map[0][0]))
        self.monsters = []

    def draw(self, rect, surface):
        for x in range(rect.left, rect.width):
            for y in range(rect.top, rect.height):
                self.game_map[x][y].draw(surface, (x-rect.left)*tilesize, (y-rect.top+1)*tilesize)

class Tile(GameObject):
    def __init__(self, game, sprite):
        GameObject.__init__(self, game)
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

    def draw(self, surface, x, y):
        surface.blit(self.sprite, (x, y))

        for entity in self.entities:
            entity.draw(surface, x, y-(sprite_height/2))

class Entity(GameObject):
    def __init__(self, game, sprites, x, y):
        GameObject.__init__(self, game)
        self.game.world.game_map[x][y].add_entity(self)
        self.sprites = sprites
        self.x = x
        self.y = y
        self.anim_state = 0

    def move(self, x, y):
        self.move_to(self.x + x, self.y + y)

    def is_collidable(self):
        return True

    def move_to(self, x, y):
        game.world.game_map[self.x][self.y].remove_entity(self)
        game.world.game_map[x][y].add_entity(self)

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

    def __init__(self, game, sprites, x, y):
        Entity.__init__(self, game, [], x, y)
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

        if x >= self.game.world.width:
            return
        if x < 0:
            return
        if y >= self.game.world.height:
            return
        if y < 0:
            return

        if not self.game.world.game_map[x][y].is_collidable():
            Entity.move_to(self, x, y)
            self.game.center_world()

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

    game = Game(100, 100)
    pygame.key.set_repeat(500, 30)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    game.player.move(0, 1)
                if event.key == pygame.K_UP:
                    game.player.move(0, -1)
                if event.key == pygame.K_LEFT:
                    game.player.move(-1, 0)
                if event.key == pygame.K_RIGHT:
                    game.player.move(1, 0)
                if event.key == pygame.K_w:
                    game.player.turn(back)
                if event.key == pygame.K_s:
                    game.player.turn(front)
                if event.key == pygame.K_a:
                    game.player.turn(left)
                if event.key == pygame.K_d:
                    game.player.turn(right)
                if event.key == pygame.K_q:
                    sys.exit()

        screen.fill((0,0,0,0))

        game.draw(screen)

        pygame.display.flip()
        clock.tick(60)

