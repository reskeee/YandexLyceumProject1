import pygame
from help import load_image, terminate
from objects import Ground


class Character(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.is_on_ground = False

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.is_on_ground = pygame.sprite.spritecollideany(self, ground_group)

    def flip(self):
        for frame in range(len(self.frames)):
            self.frames[frame] = pygame.transform.flip(self.frames[frame], True, False)


def start_screen():
    intro_text = ['Свет и Тьма',
                  'Жители Светогорода жили припеваючи,',
                  "пока злостные отряды тьмы не захватили",
                  "их поселение. Теперь в городе темно, а вам предстоит",
                  "разобраться с захватчиками!"]

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

# запуск игры
if __name__ == '__main__':
    running = True
    motion = False
    rotate = 'RIGHT'
    jump = False
    jumpcount = 0
    jumpmax = 12

    # Создание групп спрайтов
    all_sprites = pygame.sprite.Group()
    ground_group = pygame.sprite.Group()

    # Создание спрайтов
    Ground(ground_img, ground_group, all_sprites)  # Земля
    hero = Character(hero_img, 9, 1, 100, 100)  # Персонаж

    # Запуск стартового окна
    start_screen()
    screen.fill((38, 23, 82))

    # Запуск основного игрового цикла
    while running:
        screen.fill((38, 23, 82))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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
                if not jump and event.key == 32:
                    jump = True
                    jumpcount = jumpmax

            if event.type == pygame.KEYUP:
                if event.key in [97, 100]:
                    motion = False

        if motion == 'LEFT':
            hero.rect.x -= 10
        elif motion == 'RIGHT':
            hero.rect.x += 10
        if jump:
            hero.rect.y -= jumpcount
            if not jumpcount > -jumpmax:
                jump = False
                hero.is_on_ground = True
            jumpcount -= 1.5
        elif not hero.is_on_ground:
            hero.rect.y += 5

        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
