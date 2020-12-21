import pygame
from pprint import pprint as write

BACKGROUND_COLOR = (28, 28, 28)
BORDERS_COLOR = 'white'
SHIP_COLOR = 'orange'
EMPTY_CELL_COLOR = 'grey'
INJURED_COLOR = 'red'
TEXT_COLOR = (255, 100, 0)
BUTTON_COLOR = (160, 214, 180)
FOCUSED_BUTTON_COLOR = (113, 188, 120)
PUSHED_BUTTON_COLOR = (181, 101, 167)


class Deck:
    def __init__(self, cur_i, cur_j, injured=False):
        self.deck_i = cur_i
        self.deck_j = cur_j
        self.injured = injured

    def get_cords(self):
        return self.deck_i, self.deck_j

    def get_i(self):
        return self.deck_i

    def get_j(self):
        return self.deck_j

    def is_injured(self):
        return self.injured

    def set_injured(self, injured):
        self.injured = injured

    def set_cords(self, cords):
        self.deck_i, self.deck_j = cords


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
            self.decks.append(Deck(cur_i, cur_j))
            if self.horizontal:
                cur_j += 1
            else:
                cur_i += 1

    def ship_render(self, board_list):
        for deck in self.decks:
            if not deck.is_injured():
                board_list[deck.get_i()][deck.get_j()][
                    'cell_color'] = SHIP_COLOR
            else:
                board_list[deck.get_j()][deck.get_j()][
                    'cell_color'] = INJURED_COLOR

            board_list[deck.get_i()][deck.get_j()][
                'cell_ship_number'] = self.ship_number


class ChooseShipButton:
    def __init__(self, head, btn_size, text):
        self.head = self.head_x, self.head_y = head
        self.size = self.width, self.height = btn_size
        self.text = text
        self.btn_color = BUTTON_COLOR
        self.border_color = BORDERS_COLOR

    # rendering button
    def btn_render(self):
        # button
        pygame.draw.rect(screen, pygame.Color(self.border_color),
                         (self.head, self.size), 3, border_radius=10)

        pygame.draw.rect(screen, pygame.Color(self.btn_color),
                         (self.head_x + 3, self.head_y + 3,
                          self.width - 6, self.height - 6), 0,
                         border_radius=5)

        # text
        font = pygame.font.Font(None, 50)
        text = font.render(self.text, True, pygame.Color(TEXT_COLOR))
        text_rect = text.get_rect(center=(self.head_x + self.width // 2,
                                          self.head_y + self.height // 2))
        screen.blit(text, text_rect)

    def is_focused(self, cur_pos):
        return 0 < cur_pos[0] - self.head_x < self.width \
               and 0 < cur_pos[1] - self.head_y < self.height

    def get_motion(self, cur_pos):
        if self.is_focused(cur_pos):
            self.btn_color = FOCUSED_BUTTON_COLOR
        else:
            self.btn_color = BUTTON_COLOR

    # add ship to board
    def button_pushed(self, cur_pos):
        if self.is_focused(cur_pos):
            self.btn_color = PUSHED_BUTTON_COLOR

    def button_unpushed(self, cur_pos):
        if self.is_focused(cur_pos):
            self.btn_color = FOCUSED_BUTTON_COLOR


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
        # rendering choose ship buttons
        if ship_placement_stage:
            for el in choose_ship_btns:
                el.btn_render()

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

    # ship placement stage
    ship_placement_stage = True

    # test items
    # test ship
    player_board.add_ship(5)

    # choose ship buttons rendering
    choose_ship_btns = list()
    for i in range(1, 5):
        choose_ship_btns.append(
            ChooseShipButton((player_board.left + (i - 1) * 125,
                              player_board.top +
                              player_board.cell_size * 10 + 15),
                             (125, 80), f'x{i}'))

    running = True
    while running:
        # checking events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEMOTION:
                # choose btns
                if ship_placement_stage:
                    for el in choose_ship_btns:
                        el.get_motion(event.pos)

            if event.type == pygame.MOUSEBUTTONDOWN:
                # choose btns
                if ship_placement_stage:
                    for el in choose_ship_btns:
                        el.button_pushed(event.pos)
                # player_board.get_click(event.pos)

            if event.type == pygame.MOUSEBUTTONUP:
                # choose btns
                if ship_placement_stage:
                    for el in choose_ship_btns:
                        el.button_unpushed(event.pos)

        # screen updating
        screen.fill(BACKGROUND_COLOR)
        player_board.render()
        # screen flip
        pygame.display.flip()

    # game ending
    pygame.quit()
