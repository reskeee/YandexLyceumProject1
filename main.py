import sys
import json
import pygame
from help import load_image, terminate
from objects import Ground, Attack, Hero, Platform, Enemy, Boss


# Стартовый экран
def start_screen():
    intro_text = ['Свет и Тьма',
                  'Жители Светогорода жили припеваючи,',
                  "пока злостные отряды тьмы не захватили",
                  "их поселение. Теперь в городе темно, а вам предстоит",
                  "разобраться с захватчиками!",
                  '',
                  'Вам придется сделать 10 убийств, чтобы пройти в комнату с боссом']

    # Отображение текста
    font = pygame.font.Font(None, 30)
    text_coord = 175
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    screen.blit(icon_img_scaled, (325, 10))

    while True:
        for event_start in pygame.event.get():
            if event_start.type == pygame.QUIT:
                terminate()
            elif event_start.type == pygame.KEYDOWN or \
                    event_start.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


# Завершающий экран
def end_screen():
    intro_text = ['Это победа!',
                  '...думал Герой, пока не понял, что что-то не так.',
                  "Он победил главаря темноты, но светлее не становилось.",
                  "Оказывается стемнело из-за наступления ночи, а он убил",
                  "ни в чем неповинного босса. Вам решать, грустная ли это концовка..."]

    # Отображение текста
    font = pygame.font.Font(None, 30)
    text_coord = 175
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    screen.blit(icon_img_scaled, (325, 10))

    while True:
        for event_start in pygame.event.get():
            if event_start.type == pygame.QUIT:
                sys.exit()
        pygame.display.flip()
        clock.tick(FPS)


# Экран смерти
def death_screen():
    intro_text = ['Вы погибли!',
                  'Тяжело сказать, плохая ли это концовка.',
                  "Для этого нужно пройти игру ",
                  "Закройте окно и попробуйте заново!"]

    # Отображение текста
    font = pygame.font.Font(None, 30)
    text_coord = 175
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    screen.blit(icon_img_scaled, (325, 10))

    while True:
        for event_start in pygame.event.get():
            if event_start.type == pygame.QUIT:
                terminate()
            elif event_start.type == pygame.KEYDOWN or \
                    event_start.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def show_heath(health: int):
    font = pygame.font.Font(None, 50)
    text = font.render(str(health), True, (100, 255, 100))
    text_x = 750
    text_y = 30
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 1)


# Функция генерации уровня
def generate_level(level_number: int):
    global boss
    level = levels[level_number]
    platform_img = pygame.transform.scale(load_image('platform.png'), (50, 20))
    ground_group.empty()
    enemy_group.empty()
    Ground(ground_img, ground_group, all_sprites)  # Земля
    for sprite in level['platforms']:
        Platform(sprite[0], sprite[1], platform_img, ground_group)
    for sprite in level['enemies']:
        Enemy(enemy_img, 3, 1, sprite[0], sprite[1], enemy_group)
    if 'boss' in level.keys():
        boss = Boss(boss_img, 3, 1, attack_group, boss_group)
    else:
        boss = False


# Уровни
level0 = {
    'platforms': [],
    'enemies': [(550, 300)]
}

level1 = {
    'platforms': [(700, 250), (750, 250), (450, 200), (400, 200), (0, 100), (50, 100), (100, 100), (150, 100)],
    'enemies': [(0, 0), (400, 100)]
}

level2 = {
    'platforms': [(200, 0)],
    'enemies': []
}

bossfight = {
    'platforms': [(300, 0)],
    'enemies': [],
    'boss': [200, 200]
}

levels = [level0, level1, level2, bossfight]


# инициализация окна
pygame.init()
size = HEIGHT, WIDTH = 800, 450
screen = pygame.display.set_mode(size)
BG_COL = (85, 9, 112)
screen.fill(BG_COL)
FPS = 15
clock = pygame.time.Clock()

# загрузка изображений
ground_img = load_image('ground.png')
icon_img = load_image('icon.png')
icon_img_scaled = pygame.transform.scale(icon_img, (150, 150))
hero_img = load_image('hero.png')
hit_img = pygame.transform.scale(load_image('hit.png'), (600, 100))
platform_img = pygame.transform.scale(load_image('platform.png'),  (50, 20))
enemy_img = load_image('enemy.png')
boss_img = load_image('boss.png')
bullet_img = pygame.transform.scale(load_image('bullet.png'), (75, 50))


# запуск игры
if __name__ == '__main__':
    # Объявление переменных
    running = True  # Игровой цикл
    motion = False  # Двигается ли персонаж
    velocity = 10  # Скорость персонажа
    rotate = 'RIGHT'  # Поворот персонажа
    jump = False  # Прыгает ли персонаж
    jumpcount = 0  # Счетчик прыжка
    jumpmax = 18  # Максимальная высота прыжка
    health_points = 3  # Здоровье персонажа
    level = 0  # Номер уровня
    win = False  # Проверка победы
    g = 1  # Ускорение падения
    is_new_level = True  # Переходит ли персонаж на новый уровень
    kills = 0  # Счетчик убийств
    boss = False
    hero_x = 100
    hero_y = 100

    # Открытие файла сохранения
    with open('save.json') as save:
        data = json.load(save)
        if save:
            hero_x = data['hero_cords'][0]
            hero_y = data['hero_cords'][1]
            health_points = data['health']
            level = data['level']
            kills = data['kills']

    # Создание групп спрайтов
    all_sprites = pygame.sprite.Group()
    ground_group = pygame.sprite.Group()
    attack_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    boss_group = pygame.sprite.Group()

    # Создание персонажа
    hero = Hero(hero_img, 9, 1, hero_x, hero_y, all_sprites)

    # Запуск стартового окна
    start_screen()
    screen.fill(BG_COL)

    # Запуск основного игрового цикла
    while running:
        screen.fill(BG_COL)
        for event in pygame.event.get():
            # Проверка выхода и сохранение при выходе
            if event.type == pygame.QUIT:
                save_dict = {
                    'hero_cords': (hero.rect.x, hero.rect.y),
                    'health': health_points,
                    'level': level,
                    'kills': kills
                }
                with open('save.json', mode='wt', encoding='utf-8') as save:
                    json.dump(save_dict, save)
                running = False

            # Проверка нажатия кнопок движения
            if event.type == pygame.KEYDOWN:
                print(event.key)
                # Поворот персонажа вправо
                if event.key == 97:
                    if rotate != 'LEFT':
                        hero.flip()
                        rotate = 'LEFT'
                    motion = 'LEFT'

                # Поворот персонажа вправо
                if event.key == 100:
                    if rotate != 'RIGHT':
                        hero.flip()
                        rotate = 'RIGHT'
                    motion = 'RIGHT'

                # Прыжок если персонаж на земле
                if not jump and event.key == 119 and pygame.sprite.spritecollideany(hero, ground_group):
                    jump = True
                    jumpcount = jumpmax

                # Создание атаки
                if event.key == 32:
                    if rotate == 'RIGHT':
                        attack = Attack(hit_img, 4, 1, hero.rect.x + 100, hero.rect.y, all_sprites, attack_group)
                    else:
                        attack = Attack(hit_img, 4, 1, hero.rect.x - 150, hero.rect.y, all_sprites, attack_group)
                        attack.flip()

            # Проверка отпускания кнопок движения
            if event.type == pygame.KEYUP:
                if event.key in [97, 100]:
                    motion = False

        # Проверка перехода уровня
        if hero.rect.x + 100 >= 800:  # Правая стека
            if level == 3:
                hero.rect.x = 650
            elif level == 2 and kills >= 10:
                level = 3
                hero.rect.x = 20
                hero.rect.y -= 5
                is_new_level = True
            elif level == 2 and kills < 10:
                hero.rect.x = 650
            elif level == 1:
                level = 2
                hero.rect.x = 20
                hero.rect.y -= 5
                is_new_level = True
            elif level == 0:
                level = 1
                hero.rect.x = 20
                hero.rect.y -= 5
                is_new_level = True

        if hero.rect.x <= 0:  # Левая стенка
            if level == 0:
                hero.rect.x = 5
                is_new_level = True
            elif level == 1:
                level = 0
                hero.rect.x = 675
                hero.rect.y -= 5
                is_new_level = True
            elif level == 2:
                level = 1
                hero.rect.x = 675
                hero.rect.y -= 5
                is_new_level = True
            elif level == 3:
                hero.rect.x = 5

        # Нанесение урона
        for enemy in enemy_group:
            if pygame.sprite.spritecollideany(enemy, attack_group):
                enemy.heath_points -= 1
                enemy_group.update()
                if enemy.heath_points <= 0:
                    kills += 1
                print(enemy.heath_points)

        # Получение персонажем урона
        if pygame.sprite.spritecollideany(hero, enemy_group):
            health_points -= 1
            hero.rect.y -= 50
            if rotate == 'LEFT':
                hero.rect.x += 80
            elif rotate == 'RIGHT':
                hero.rect.x -= 80

        # Движение
        if motion == 'LEFT':
            hero.rect.x -= velocity
        elif motion == 'RIGHT':
            hero.rect.x += velocity

        # Прыжок и падение
        if jump:
            hero.rect.y -= jumpcount
            if not jumpcount > 0:
                jump = False
                hero.is_on_ground = True
                g = 1
            jumpcount -= 1
        elif not pygame.sprite.spritecollideany(hero, ground_group):
            hero.rect.y += 5 + g
            g += 1

        if is_new_level:
            is_new_level = False
            generate_level(level)

        if health_points == 0:
            death_screen()
            sys.exit()

        # Обновление экрана
        all_sprites.update()
        enemy_group.update()
        if boss:
            boss_group.update(bullet_img, (boss.rect.x, 100), enemy_group)
            boss_group.draw(screen)
            if boss.heath_points == 0:
                end_screen()
                save_dict = {
                    'hero_cords': (100, 100),
                    'health': 5,
                    'level': 0,
                    'kills': 0
                }
                with open('save.json', mode='wt', encoding='utf-8') as save:
                    json.dump(save_dict, save)
                sys.exit()
        ground_group.draw(screen)
        enemy_group.draw(screen)
        all_sprites.draw(screen)
        show_heath(health_points)
        pygame.display.flip()
        # print(is_new_level if is_new_level is True else 0)
        clock.tick(FPS)
