import pygame
from help import load_image, terminate
from objects import Ground


def start_screen():
    intro_text = ['Свет и Тьма',
                  'Жители Светогорода жили припеваючи',
                  "пока злостные отряды тьмы не захватили",
                  "его. Теперь в городе темно, а вам предстоит",
                  "разобраться с захватчиками!"]

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
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


# инициализация окна
pygame.init()
size = HEIGHT, WIDTH = 800, 450
screen = pygame.display.set_mode(size)
screen.fill((38, 23, 82))
FPS = 30
clock = pygame.time.Clock()

# загрузка изображений
ground_img = load_image('ground.png')

# запуск игры
if __name__ == '__main__':
    running = True
    # Создание групп спрайтов
    all_sprites = pygame.sprite.Group()
    ground_group = pygame.sprite.Group()

    # Создание спрайтов
    Ground(ground_img, ground_group, all_sprites)  # Земля

    # Запуск стартового окна
    start_screen()
    screen.fill((38, 23, 82))
    # Запуск основного игрового цикла
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        all_sprites.draw(screen)
        pygame.display.flip()
