import pygame
from help import load_image


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, *group):
        super().__init__(*group)
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

    def flip(self):
        for frame in range(len(self.frames)):
            self.frames[frame] = pygame.transform.flip(self.frames[frame], True, False)


class Ground(pygame.sprite.Sprite):
    def __init__(self, image, *group):
        super().__init__(*group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 385


class Attack(pygame.sprite.Sprite):
    def __init__(self, sheet: pygame.Surface, columns: int, rows: int, x: int, y: int, *group):
        super().__init__(*group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.framecount = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.framecount += 1
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        if self.framecount == 4:
            self.kill()

    def flip(self):
        for frame in range(len(self.frames)):
            self.frames[frame] = pygame.transform.flip(self.frames[frame], True, False)


class Hero(AnimatedSprite):
    def __init__(self, sheet, columns, rows, x, y, *group):
        super().__init__(sheet, columns, rows, x, y, *group)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, sheet: pygame.Surface, columns: int, rows: int, x: int, y: int, *group):
        super().__init__(*group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.framecount = 0
        self.heath_points = 12

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
        if self.heath_points <= 12:
            self.image = self.frames[0]
        if self.heath_points <= 8:
            self.image = self.frames[1]
        if self.heath_points <= 4:
            self.image = self.frames[2]
        if self.heath_points == 0:
            self.kill()


class Platform(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, image, *group):
        super().__init__(*group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
