import pygame, sys
from pygame import Rect

tilesize = 32
sprite_height = 32
sprite_width = 32
screen_width = 1024
screen_height = 1024
tiles_per_row = screen_width / tilesize
tiles_per_col = screen_height / tilesize

class Game:
    def __init__(self, world_width, world_height):
        self.world = World(self, world_width, world_height)
        self.entity_map = load_sprite("player.png", sprite_width, sprite_height)
        self.player = Player(self, self.entity_map[1][0], 0, 0)
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
        self.tile_map = load_sprite("dirt32.png", sprite_width, sprite_height)
        self.width = width
        self.height = height
        self.game_map = []
        derpsurface = pygame.Surface((tilesize, tilesize))
        for x in range(0, width):
            line = []
            self.game_map.append(line)
            for y in range(0, height):
                if y % 2 == 0 and x % 2 == 0:
                    surf = derpsurface.copy()
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

    def draw(self, surface, x, y):
        surface.blit(self.sprite, (x, y))

        for entity in self.entities:
            entity.draw(surface, x, y-(sprite_height/2))

class Entity(GameObject):
    def __init__(self, game, sprite, x, y):
        GameObject.__init__(self, game)
        self.game.world.game_map[x][y].add_entity(self)
        self.sprite = sprite
        self.x = x
        self.y = y

    def move(self, x, y):
        self.move_to(self.x + x, self.y + y)

    def move_to(self, x, y):
        game.world.game_map[self.x][self.y].remove_entity(self)
        game.world.game_map[x][y].add_entity(self)

        self.x = x
        self.y = y

    def draw(self, surface, x, y):
        surface.blit(self.sprite, (x, y))

class Player(Entity):
    def move_to(self, x, y):
        if x >= self.game.world.width:
            return
        if x < 0:
            return
        if y >= self.game.world.height:
            return
        if y < 0:
            return
        Entity.move_to(self, x, y)
        self.game.center_world()

def load_sprite(filename, width, height):
    image = pygame.image.load(filename).convert_alpha()
    image_width, image_height = image.get_size()
    sprite_table = []
    for sprite_x in range(0, int(image_width/width)):
        line = []
        sprite_table.append(line)
        for sprite_y in range(0, int(image_height/height)):
            rect = (sprite_x*width, sprite_y*height, width, height)
            line.append(image.subsurface(rect))
    return sprite_table

if __name__=='__main__':
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.DOUBLEBUF, 32)
    clock = pygame.time.Clock()

    game = Game(100, 100)

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
                if event.key == pygame.K_q:
                    sys.exit()

        screen.fill((0,0,0,0))

        game.draw(screen)

        pygame.display.flip()
        clock.tick(60)

