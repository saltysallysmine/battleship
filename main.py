import pygame
from pprint import pprint as write

BACKGROUND_COLOR = (28, 28, 28)
BORDERS_COLOR = 'white'
SHIP_COLOR = 'orange'
EMPTY_CELL_COLOR = 'grey'
INJURED_COLOR = 'red'


class Ship:
    def __init__(self, decks_number=1, head_pos=(0, 0), horizontal=True, ship_number=0):
        # число палуб
        self.decks_number = decks_number
        # позиция головы
        self.head_pos = self.head_i, self.head_j = head_pos
        # горизонтальный / вертикальный
        self.horizontal = horizontal
        # статус корабля
        self.alive = True
        # номер корабля в списке board
        self.ship_number = ship_number
        # палубы со значением их целостности
        self.decks = list()
        self.decks_list_filling()

    def decks_list_filling(self):
        cur_i, cur_j = self.head_pos
        for _ in range(self.decks_number):
            self.decks.append({'deck_i': cur_i,
                               'deck_j': cur_j,
                               'deck_injured': False})
            if self.horizontal:
                cur_j += 1
            else:
                cur_i += 1

    def ship_render(self, board_list):
        for el in self.decks:
            if not el['deck_injured']:
                board_list[el['deck_i']][
                    el['deck_j']]['cell_color'] = SHIP_COLOR
            else:
                board_list[el['deck_i']][
                    el['deck_j']]['cell_color'] = INJURED_COLOR

            board_list[el['deck_i']][el['deck_j']][
                'cell_ship_number'] = self.ship_number


class Board:
    # создание поля
    def __init__(self, board_width, board_height):
        # size
        self.width = board_width
        self.height = board_height
        # list of boards cells values
        self.board = list()
        for _ in range(board_height):
            self.board.append([{'cell_color': EMPTY_CELL_COLOR,
                                'cell_ship_number': None}
                               for nn in range(board_width)])

        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

        # rows and lines names
        self.lines_names = {}
        for i in range(1, 11):
            self.lines_names[i - 1] = str(i)
        self.rows_names = {}
        for i in range(65, 75):
            self.rows_names[i - 65] = chr(i)

        # list of ships placed on the board
        self.ships = list()

    # add ship function
    def add_ship(self, decks_number):
        self.ships.append(Ship(decks_number=decks_number))

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def rendering_symbol(self, symbol_number, symbol_x, symbol_y, rows=True):
        if rows:
            symbol = self.rows_names[symbol_number]
        else:
            symbol = self.lines_names[symbol_number]

        font = pygame.font.Font(None, self.cell_size)
        text = font.render(symbol, True, pygame.Color(SHIP_COLOR))
        text_rect = text.get_rect(center=(symbol_x + self.cell_size // 2,
                                          symbol_y + self.cell_size // 2))
        screen.blit(text, text_rect)

    # board render
    def render(self):

        # rendering rows names
        cur_x = self.left
        cur_y = self.top - self.cell_size
        for i in range(10):
            self.rendering_symbol(i, cur_x, cur_y)
            cur_x += self.cell_size

        # rendering lines names
        cur_x = self.left - self.cell_size
        cur_y = self.top
        for i in range(10):
            self.rendering_symbol(i, cur_x, cur_y, rows=False)
            cur_y += self.cell_size

        # ships rendering
        for el in self.ships:
            el.ship_render(self.board)

        # board cells filling
        for i in range(self.height):
            cur_cell_x = self.left
            cur_cell_y = self.top + i * self.cell_size
            for j in range(self.width):
                cur_color = BORDERS_COLOR
                pygame.draw.rect(screen, pygame.Color(cur_color),
                                 (cur_cell_x, cur_cell_y,
                                  self.cell_size, self.cell_size), 3,
                                 border_radius=8)

                cur_color = self.board[i][j]['cell_color']
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
            if self.board[cell_coords[0]][cell_coords[1]]['cell_color'] == EMPTY_CELL_COLOR:
                self.board[cell_coords[0]][cell_coords[1]]['cell_color'] = SHIP_COLOR
            else:
                self.board[cell_coords[0]][cell_coords[1]]['cell_color'] = EMPTY_CELL_COLOR

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption('Battleship')
    size = width, height = 700, 700
    screen = pygame.display.set_mode(size)
    player_board = Board(10, 10)
    player_board.set_view(80, 80, 50)

    # test ship
    player_board.add_ship(5)

    running = True
    while running:
        # checking events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                player_board.get_click(event.pos)

        # screen updating
        screen.fill(BACKGROUND_COLOR)
        player_board.render()
        # screen flip
        pygame.display.flip()

    # game ending
    pygame.quit()
