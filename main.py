import pygame


def draw():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render("Hello, Pygame!", True, (100, 255, 100))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 1)
    # screen flip
    pygame.display.flip()


if __name__ == "__main__":
    # pygame initialization
    pygame.init()
    # set size
    size = width, height = 800, 600
    # screen initialization
    screen = pygame.display.set_mode(size)
    # screen flip
    pygame.display.flip()

    # game loop
    while pygame.event.wait().type != pygame.QUIT:
        draw()

    # game ending
    pygame.quit()
