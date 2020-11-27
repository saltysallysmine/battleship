import pygame


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    # board render
    def render(self):
        for i in range(self.height):
            cur_cell_x = self.left
            cur_cell_y = self.top + i * self.cell_size
            for j in range(self.width):
                cur_color = 'white'
                pygame.draw.rect(screen, pygame.Color(cur_color),
                                 (cur_cell_x, cur_cell_y,
                                  self.cell_size, self.cell_size), 3,
                                 border_radius=8)
                if self.board[i][j] == 1:
                    cur_color = 'orange'
                else:
                    cur_color = 'grey'

                pygame.draw.rect(screen, pygame.Color(cur_color),
                                 (cur_cell_x + 3, cur_cell_y + 3,
                                  self.cell_size - 6, self.cell_size - 6), 0,
                                 border_radius=5)
                cur_cell_x += self.cell_size

    def get_cell(self, mouse_pos):
        if 0 < mouse_pos[0] - self.left < self.cell_size * self.width and \
                0 < mouse_pos[1] - self.top < self.cell_size * self.height:
            clicked_cell_i = (mouse_pos[1] - self.left) // self.cell_size
            clicked_cell_j = (mouse_pos[0] - self.left) // self.cell_size
            return clicked_cell_i, clicked_cell_j

    def on_click(self, cell_coords):
        if cell_coords:
            if self.board[cell_coords[0]][cell_coords[1]] == 0:
                self.board[cell_coords[0]][cell_coords[1]] = 1
            else:
                self.board[cell_coords[0]][cell_coords[1]] = 0

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption('Клетчатое поле')
    size = width, height = 800, 500
    screen = pygame.display.set_mode(size)
    board = Board(6, 6)
    board.set_view(30, 30, 70)

    running = True
    while running:
        # checking events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)

        # screen updating
        screen.fill((0, 0, 0))
        board.render()
        pygame.display.flip()

    # game ending
    pygame.quit()
