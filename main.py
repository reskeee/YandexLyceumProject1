import pygame

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Движущийся круг 2')
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)
    pos = (width / 2, height / 2)

    running = True
    x_pos = 0
    v = 20  # пикселей в секунду
    fps = 75
    clock = pygame.time.Clock()
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                pos = event.pos
            pygame.draw.circle(screen, (0, 0, 255), pos, 20)
        pygame.display.flip()
        clock.tick(50)
    pygame.quit()
