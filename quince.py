import pygame, sys

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.game_map = []
        for x in range(0, width):
            line = []
            game_map.append(line)
            for y in range(0, height):
                line.append(0)
        self.monsters = []

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
    screen_width = 1024
    screen_height = 1024
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.DOUBLEBUF, 32)
    clock = pygame.time.Clock()

    screen.fill((0,0,0))
    sprite_height = 128
    sprite_width = 128
    sprite_table = load_sprite("player4x.png", sprite_width, sprite_height)
    tile_table = load_sprite("dirt.png", sprite_width, sprite_height)

    player_sprite = sprite_table[0][0]
    sprite_x = (screen_width/2)
    sprite_y = (screen_height/2) + (sprite_height/2)

    player_x = 0
    player_y = 0

    step = 128
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    player_sprite = sprite_table[1][0]
                    sprite_y += step
                if event.key == pygame.K_UP:
                    player_sprite = sprite_table[2][0]
                    sprite_y -= step
                if event.key == pygame.K_LEFT:
                    player_sprite = sprite_table[0][0]
                    sprite_x -= step
                if event.key == pygame.K_RIGHT:
                    player_sprite = sprite_table[3][0]
                    sprite_x += step
                if event.key == pygame.K_q:
                    sys.exit()

        screen.fill((0,0,0,0))

        x = 0
        y = 128

        while x < screen_width:
            while y < screen_height:
                screen.blit(tile_table[0][0], (x, y))
                y += 128
            y = 128
            x += 128

        screen.blit(player_sprite, (sprite_x, sprite_y))
        pygame.display.flip()
        clock.tick(60)

