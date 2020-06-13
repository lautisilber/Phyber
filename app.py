import pygame

def main():
    pygame.init()

    screen = pygame.display.set_mode([600, 400])
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))

        pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

        pygame.display.flip()

    pygame.quit

if __name__ == '__main__':
    main()
