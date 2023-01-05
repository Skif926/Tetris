import pygame
from copy import deepcopy
from random import choice, randrange

Width = 10
Height = 20
Title = 45
Game_res = Width * Title, Height * Title
RES = 750, 940
FPS = 60
pause = 1
state = True
pygame.init()
sc = pygame.display.set_mode(RES)
game_sc = pygame.Surface(Game_res)
clock = pygame.time.Clock()

grid = [pygame.Rect(x * Title, y * Title, Title, Title) for x in range(Width) for y in range(Height)]

figurespos = [[(-1, -1), (-2, -1), (0, -1), (1, -1)],
              [(0, -1), (-1, -1), (-1, 0), (0, 0)],
              [(-1, 0), (-1, 1), (0, 0), (0, -1)],
              [(0, 0), (-1, 0), (0, 1), (-1, -1)],
              [(0, 0), (0, -1), (0, 1), (-1, -1)],
              [(0, 0), (0, -1), (0, 1), (1, -1)],
              [(0, 0), (0, -1), (0, 1), (-1, 0)]]
figures = [[pygame.Rect(x + Width // 2, y + 1, 1, 1) for x, y in figpos] for figpos in figurespos]
figure_rect = pygame.Rect(0, 0, Title - 2, Title - 2)
field = [[0 for i in range(Width)] for j in range(Height)]
anim_count = 0
anim_speed = 60
anim_limit = 2000
bg = pygame.image.load('img/1.jpg').convert()
game_bg = pygame.image.load('img/2.jpg').convert()
pause_bg = pygame.image.load('img/4.jpg').convert()
main_font = pygame.font.Font('font/Vasek.ttf', 100)
font = pygame.font.Font('font/Vasek.ttf', 65)
score = 0
lines = 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}
get_color = lambda: (randrange(30, 256), randrange(30, 256), randrange(30, 256))

title_tetris = main_font.render('Tetris', True, pygame.Color('Pink'))
title_score = font.render('score:', True, pygame.Color('Green'))
title_record = font.render('record:', True, pygame.Color('Yellow'))

figure = deepcopy(choice(figures))
next_figure = deepcopy(choice(figures))
color = get_color()
next_color = get_color()


def check_borders():
    if figure[i].x < 0 or figure[i].x > Width - 1:
        return False
    elif figure[i].y > Height - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True


def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')


def set_record(lrecord, lscore):
    rec = max(int(lrecord), lscore)
    with open('record', 'w') as f:
        f.write(str(rec))


while True:
    dx = 0
    record = get_record()
    rotate = False
    sc.blit(bg, (0, 0))
    sc.blit(game_sc, (20, 20))
    game_sc.blit(game_bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_RIGHT:
                dx = 1
            elif event.key == pygame.K_DOWN:
                anim_limit = 100
            elif event.key == pygame.K_UP:
                rotate = True
            elif event.key == pygame.K_SPACE:
                pause += 1
                if pause % 2 == 0:
                    state = False
                else:
                    state = True
    if state:
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].x += dx
            if not check_borders():
                figure = deepcopy(figure_old)
                break

        anim_count += anim_speed
        if anim_count > anim_limit:
            anim_count = 0
            figure_old = deepcopy(figure)
            for i in range(4):
                figure[i].y += 1
                if not check_borders():
                    for i in range(4):
                        field[figure_old[i].y][figure_old[i].x] = color
                    figure = next_figure
                    color = next_color
                    next_figure = deepcopy(choice(figures))
                    next_color = get_color()
                    anim_limit = 2000
                    break

        centr_rotate = figure[0]
        figure_old = deepcopy(figure)
        if rotate:
            for i in range(4):
                x = figure[i].y - centr_rotate.y
                y = figure[i].x - centr_rotate.x
                figure[i].x = centr_rotate.x - x
                figure[i].y = centr_rotate.y + y
                if not check_borders():
                    figure = deepcopy(figure_old)
                    break

        lastLine = Height - 1
        lines = 0
        for row in range(Height - 1, -1, -1):
            count = 0
            for i in range(Width):
                if field[row][i]:
                    count += 1
                field[lastLine][i] = field[row][i]
            if count < Width:
                lastLine -= 1
            else:
                anim_speed += 3
                lines += 1

        score += scores[lines]
        [pygame.draw.rect(game_sc, (40, 40, 40), irect, 1) for irect in grid]

        for i in range(4):
            figure_rect.x = figure[i].x * Title
            figure_rect.y = figure[i].y * Title

            pygame.draw.rect(game_sc, color, figure_rect)

        for y, raw in enumerate(field):
            for x, col in enumerate(raw):
                if col:
                    figure_rect.x = x * Title
                    figure_rect.y = y * Title
                    pygame.draw.rect(game_sc, col, figure_rect)
        for i in range(4):
            figure_rect.x = next_figure[i].x * Title + 380
            figure_rect.y = next_figure[i].y * Title + 185
            pygame.draw.rect(sc, next_color, figure_rect)
        sc.blit(title_tetris, (550, 25))
        sc.blit(title_score, (535, 780))
        sc.blit(font.render(str(score), True, pygame.Color('white')), (550, 840))
        sc.blit(title_record, (535, 680))
        sc.blit(font.render(record, True, pygame.Color('gold')), (535, 735))

        for i in range(Width):
            if field[0][i]:
                set_record(record, score)
                field = [[0 for i in range(Width)] for i in range(Height)]
                anim_count = 0
                anim_speed = 60
                anim_limit = 2000
                score = 0
                for irect in grid:
                    pygame.draw.rect(game_sc, get_color(), irect)
                    sc.blit(game_sc, (20, 20))
                    pygame.display.flip()
                    clock.tick(200)
        pygame.display.flip()
        clock.tick(FPS)
    else:
        title_pause = pygame.font.Font('font/Vasek.ttf', 230).render('Пауза', True,pygame.Color(randrange(30, 256), randrange(30, 256), randrange(30, 256), randrange(30, 256)))
        sc.blit(pause_bg, (0, 0))
        sc.blit(title_pause, (200, 400))
        pygame.display.flip()
        clock.tick(10)
