from pprint import pprint

import pygame
import sys
import os

FPS = 50

pygame.init()
pygame.display.set_caption('Game')
WIDTH = 500
HEIGHT = 500
size = 500, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    return list(level_map)


test = load_level('level.txt')
field = [[None] * len(test[0]) for _ in range(len(test))]
FIELD = [[None] * len(test[0]) for _ in range(len(test))]


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ПЕРЕМЕЩЕНИЕ ГЕРОЯ", "",
                  "Правила игры",
                  "Перемещение происходит клавишами стрелок,",
                  "Также камера двигается за персонажем"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mario.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Wall(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(block_group, all_sprites)
        self.mode = tile_type
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.x = 0
        self.y = 0

    def move(self, side):
        global field
        if side == 'L':
            if not isinstance(FIELD[self.pos_x - 1][self.pos_y], Wall):
                self.x -= 1
                all_sprites.empty()
                block_group.empty()
                tiles_group.empty()
                for y in range(level_y + 1):
                    for x in range(level_x + 1):
                        if level[(y + self.y) % (level_y + 1)][(x + self.x) % (level_x + 1)] == '#':
                            FIELD[x][y] = Wall('wall', x, y)
                        else:
                            FIELD[x][y] = Tile('empty', x, y)
                    print()
        if side == 'R':
            if not isinstance(FIELD[self.pos_x + 1][self.pos_y], Wall):
                self.x += 1
                all_sprites.empty()
                block_group.empty()
                tiles_group.empty()
                for y in range(level_y + 1):
                    for x in range(level_x + 1):
                        if level[(y + self.y) % (level_y + 1)][(x + self.x) % (level_x + 1)] == '#':
                            FIELD[x][y] = Wall('wall', x, y)
                        else:
                            FIELD[x][y] = Tile('empty', x, y)
                    print()
        if side == 'U':
            print(FIELD[self.pos_x][self.pos_y - 1])
            if not isinstance(FIELD[self.pos_x][self.pos_y - 1], Wall):
                self.y -= 1
                all_sprites.empty()
                block_group.empty()
                tiles_group.empty()
                for y in range(level_y + 1):
                    for x in range(level_x + 1):
                        if level[(y + self.y) % (level_y + 1)][(x + self.x) % (level_x + 1)] == '#':
                            FIELD[x][y] = Wall('wall', x, y)
                        else:
                            FIELD[x][y] = Tile('empty', x, y)
                    print()
        if side == 'D':
            if not isinstance(FIELD[self.pos_x][self.pos_y + 1], Wall):
                self.y += 1
                all_sprites.empty()
                block_group.empty()
                tiles_group.empty()
                for y in range(level_y + 1):
                    for x in range(level_x + 1):
                        if level[(y + self.y) % (level_y + 1)][(x + self.x) % (level_x + 1)] == '#':
                            FIELD[x][y] = Wall('wall', x, y)
                        else:
                            FIELD[x][y] = Tile('empty', x, y)


player = None

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
block_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level):
    global field
    new_player, x, y = None, None, None
    print(field)
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                t = Tile('empty', x, y)
                FIELD[x][y] = t
            elif level[y][x] == '#':
                w = Wall('wall', x, y)
                FIELD[x][y] = w
            elif level[y][x] == '@':
                t = Tile('empty', x, y)
                FIELD[x][y] = t
                new_player = Player(x, y)
    return new_player, x, y, level


start_screen()
running = True
player, level_x, level_y, level = generate_level(load_level('level.txt'))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.move('L')
            if event.key == pygame.K_RIGHT:
                player.move('R')
            if event.key == pygame.K_UP:
                player.move('U')
            if event.key == pygame.K_DOWN:
                player.move('D')
    screen.fill('black')
    all_sprites.draw(screen)
    block_group.draw(screen)
    tiles_group.draw(screen)
    player.update()
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
