import pygame
from help import load_image, terminate
from objects import Ground, AnimatedSprite, Attack, Hero


# Стартовый экран
def start_screen():
    intro_text = ['Свет и Тьма',
                  'Жители Светогорода жили припеваючи,',
                  "пока злостные отряды тьмы не захватили",
                  "их поселение. Теперь в городе темно, а вам предстоит",
                  "разобраться с захватчиками!"]

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


# инициализация окна
pygame.init()
size = HEIGHT, WIDTH = 800, 450
screen = pygame.display.set_mode(size)
screen.fill((38, 23, 82))
FPS = 15
clock = pygame.time.Clock()

# загрузка изображений
ground_img = load_image('ground.png')
icon_img = load_image('icon.png')
icon_img_scaled = pygame.transform.scale(icon_img, (150, 150))
hero_img = load_image('hero.png')
hit_img = pygame.transform.scale(load_image('hit.png'), (600, 100))

# запуск игры
if __name__ == '__main__':
    running = True
    motion = False
    rotate = 'RIGHT'
    jump = False
    jumpcount = 0
    jumpmax = 12
    game_screen = 0
    health_points = 3

    # Создание групп спрайтов
    all_sprites = pygame.sprite.Group()
    ground_group = pygame.sprite.Group()
    attack_group = pygame.sprite.Group()

    # Создание спрайтов
    Ground(ground_img, ground_group, all_sprites)  # Земля
    hero = Hero(hero_img, 9, 1, 100, 100, all_sprites)  # Персонаж

    # Запуск стартового окна
    start_screen()
    screen.fill((38, 23, 82))

    # Запуск основного игрового цикла
    while running:
        screen.fill((38, 23, 82))
        for event in pygame.event.get():
            # Проверка выхода
            if event.type == pygame.QUIT:
                running = False

            # Проверка нажатия кнопок движения
            if event.type == pygame.KEYDOWN:
                print(event.key)
                if event.key == 97:
                    if rotate != 'LEFT':
                        hero.flip()
                        rotate = 'LEFT'
                    motion = 'LEFT'

                if event.key == 100:
                    if rotate != 'RIGHT':
                        hero.flip()
                        rotate = 'RIGHT'
                    motion = 'RIGHT'

                if not jump and event.key == 119:
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

        if hero.rect.x + 100 >= 800:
            hero.rect.x = 15
            hero.rect.y -= 5
        if hero.rect.x <= 0:
            hero.rect.x = 675
            hero.rect.y -= 5

        # Движение
        if motion == 'LEFT':
            hero.rect.x -= 10
        elif motion == 'RIGHT':
            hero.rect.x += 10

        # Прыжок и падение
        if jump:
            hero.rect.y -= jumpcount
            if not jumpcount > -jumpmax:
                jump = False
                hero.is_on_ground = True
            jumpcount -= 1
        elif not pygame.sprite.spritecollideany(hero, ground_group):
            hero.rect.y += 5

        # Обновление экрана
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
