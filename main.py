import sys
import pygame
from random import randint, randrange
from pprint import pprint as write

BACKGROUND_COLOR = (28, 28, 28)
BORDERS_COLOR = 'white'
SHIP_COLOR = 'orange'
EMPTY_CELL_COLOR = 'grey'
INACTIVE_CELL_COLOR = 'grey'
INJURED_COLOR = 'red'
TEXT_COLOR = (255, 100, 0)
BUTTON_COLOR = (160, 214, 180)
FOCUSED_BUTTON_COLOR = (113, 188, 120)
PUSHED_BUTTON_COLOR = (181, 101, 167)
SHOOTED_CELL_COLOR = BUTTON_COLOR


class BoardCell:
    def __init__(self, color):
        # the current color of the cell
        self.color = color
        # two cell color options
        self.unfocused_color = color
        self.focused_color = color
        # determines the current color option
        self.focused = False
        # update color options
        self.set_cell_color(color)
        # the ship that occupies the cell
        self.cell_ship_number = None

    def get_cell_color(self):
        return self.color

    def set_cell_color(self, color):
        self.unfocused_color = color

        hsv = pygame.Color(self.unfocused_color).hsva
        cur_color = pygame.Color(self.unfocused_color)
        if hsv[2] + 10 < 100:
            cur_color.hsva = (hsv[0], hsv[1], hsv[2] + 10, hsv[3])
        else:
            cur_color.hsva = ((hsv[0] + 10) % 360, hsv[1], hsv[2], hsv[3])
        self.focused_color = tuple(cur_color)

        self.color = color

        if self.focused:
            self.color = self.focused_color
        else:
            self.color = self.unfocused_color

    def set_focused_status(self, status):
        self.focused = status

        if self.focused:
            self.color = self.focused_color
        else:
            self.color = self.unfocused_color

    def get_cell_ship_number(self):
        return self.cell_ship_number

    def set_cell_ship_number(self, cell_ship_number):
        self.cell_ship_number = cell_ship_number

    def is_shooted(self):
        return self.color == SHOOTED_CELL_COLOR

    def set_shooted(self):
        self.set_cell_color(SHOOTED_CELL_COLOR)


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

    def set_injured(self, injured=True):
        self.injured = injured

    def set_cords(self, *cords):
        self.deck_i, self.deck_j = cords


class Ship:
    def __init__(self, decks_number=1, head_pos=(0, 0), horizontal=True, ship_number=0):
        # число палуб
        self.decks_number = decks_number
        # is bot board
        self.is_bot = False
        # горизонтальный / вертикальный
        # maybe head
        self.head_pos = head_pos
        self.horizontal = horizontal
        # статус корабля
        self.alive = True
        # номер корабля в списке board
        self.ship_number = ship_number
        # для заполнения информации о палубах корабля
        self.new_ship = True
        # палубы со значением их целостности
        self.decks = list()
        self.decks_list_filling()
        # placed
        self.placed = False
        # позиция головы
        self.set_head_pos(head_pos)

    def is_horizontal(self):
        return self.horizontal

    def decks_list_filling(self):
        # new ship or not
        if self.decks:
            self.new_ship = False
        # filling
        cur_i, cur_j = self.head_pos
        for x in range(self.decks_number):
            if self.new_ship:
                self.decks.append(Deck(cur_i, cur_j))
            else:
                self.decks[x].set_cords(cur_i, cur_j)
            if self.horizontal:
                cur_j += 1
            else:
                cur_i += 1

    def change_horizontal(self, cur_board):
        if not self.horizontal:
            if self.head_pos[1] + self.decks_number - 1 < cur_board.width:
                self.horizontal = not self.horizontal
                self.decks_list_filling()
        else:
            if self.head_pos[0] + self.decks_number - 1 < cur_board.height:
                self.horizontal = not self.horizontal
                self.decks_list_filling()

    def get_size(self):
        return len(self.decks)

    def set_number(self, numb):
        self.ship_number = numb

    def set_head_pos(self, new_pos):
        new_head_i, new_head_j = new_pos
        cur_height, cur_width = 10, 10
        if self.is_horizontal():
            new_head_j = min(cur_width - self.get_size(), new_head_j)
        else:
            new_head_i = min(cur_height - self.get_size(), new_head_i)
        self.head_pos = new_head_i, new_head_j
        self.decks_list_filling()

    def place_is_ok(self, cur_board):
        board_list = cur_board.board
        cur_i, cur_j = self.head_pos
        cur_height, cur_width = cur_board.get_size()
        for x in range(self.decks_number):
            # current cell
            if board_list[cur_i][cur_j].get_cell_ship_number() is not None:
                return False
            # corners
            if cur_i != 0 and cur_j != 0:
                if board_list[cur_i - 1][cur_j - 1].get_cell_ship_number() is not None:
                    return False
            if cur_i != 0 and cur_j != cur_width - 1:
                if board_list[cur_i - 1][cur_j + 1].get_cell_ship_number() is not None:
                    return False
            if cur_i != cur_height - 1 and cur_j != 0:
                if board_list[cur_i + 1][cur_j - 1].get_cell_ship_number() is not None:
                    return False
            if cur_i != cur_height - 1 and cur_j != cur_width - 1:
                if board_list[cur_i + 1][cur_j + 1].get_cell_ship_number() is not None:
                    return False
            # other cells
            if self.horizontal:
                # tail or nose
                if x == 0:
                    if cur_j != 0:
                        if board_list[cur_i][cur_j - 1].get_cell_ship_number() is not None:
                            return False
                if x == self.decks_number - 1:
                    if cur_j != cur_width - 1:
                        if board_list[cur_i][cur_j + 1].get_cell_ship_number() is not None:
                            return False
                # all decks
                if cur_i < cur_height - 1:
                    if board_list[cur_i + 1][cur_j].get_cell_ship_number() is not None:
                        return False
                if cur_i > 0:
                    if board_list[cur_i - 1][cur_j].get_cell_ship_number() is not None:
                        return False
                # index growing
                cur_j += 1
            else:
                # tail or nose
                if x == 0:
                    if cur_i != 0:
                        if board_list[cur_i - 1][cur_j].get_cell_ship_number() is not None:
                            return False
                if x == self.decks_number - 1:
                    if cur_i != cur_height - 1:
                        if board_list[cur_i + 1][cur_j].get_cell_ship_number() is not None:
                            return False
                # all decks
                if cur_j < cur_width - 1:
                    if board_list[cur_i][cur_j + 1].get_cell_ship_number() is not None:
                        return False
                if cur_j > 0:
                    if board_list[cur_i][cur_j - 1].get_cell_ship_number() is not None:
                        return False
                # index growing
                cur_i += 1
        self.placed = True
        return True

    def is_deck_injured(self, cur_cell):
        if self.horizontal:
            deck_numb = cur_cell[1] - self.head_pos[1]
        else:
            deck_numb = cur_cell[0] - self.head_pos[0]

        return self.decks[deck_numb].is_injured()

    def set_deck_injured(self, cur_cell):
        if self.horizontal:
            deck_numb = cur_cell[1] - self.head_pos[1]
        else:
            deck_numb = cur_cell[0] - self.head_pos[0]

        self.decks[deck_numb].set_injured()

        self.alive = False
        for deck in self.decks:
            if not deck.is_injured():
                self.alive = True

    def set_bot_status(self, is_bot=True):
        self.is_bot = is_bot

    def ship_render(self, board_list):
        for deck in self.decks:
            if not deck.is_injured():
                board_list[deck.get_i()][deck.get_j()].set_cell_color(SHIP_COLOR)
                if self.is_bot:
                    board_list[deck.get_i()][deck.get_j()].set_cell_color(EMPTY_CELL_COLOR)
            else:
                board_list[deck.get_i()][deck.get_j()].set_cell_color(INJURED_COLOR)
            if self.placed:
                board_list[deck.get_i()][deck.get_j()].set_cell_ship_number(self.ship_number)

        if not self.alive:
            cur_i, cur_j = self.head_pos
            cur_height, cur_width = (10, 10)
            for x in range(self.decks_number):
                # corners
                if cur_i != 0 and cur_j != 0:
                    board_list[cur_i - 1][cur_j - 1].set_shooted()
                if cur_i != 0 and cur_j != cur_width - 1:
                    board_list[cur_i - 1][cur_j + 1].set_shooted()

                if cur_i != cur_height - 1 and cur_j != 0:
                    board_list[cur_i + 1][cur_j - 1].set_shooted()
                if cur_i != cur_height - 1 and cur_j != cur_width - 1:
                    board_list[cur_i + 1][cur_j + 1].set_shooted()
                # other cells
                if self.horizontal:
                    # tail or nose
                    if x == 0:
                        if cur_j != 0:
                            board_list[cur_i][cur_j - 1].set_shooted()
                    if x == self.decks_number - 1:
                        if cur_j != cur_width - 1:
                            board_list[cur_i][cur_j + 1].set_shooted()
                    # all decks
                    if cur_i < cur_height - 1:
                        board_list[cur_i + 1][cur_j].set_shooted()
                    if cur_i > 0:
                        board_list[cur_i - 1][cur_j].set_shooted()
                    # index growing
                    cur_j += 1
                else:
                    # tail or nose
                    if x == 0:
                        if cur_i != 0:
                            board_list[cur_i - 1][cur_j].set_shooted()
                    if x == self.decks_number - 1:
                        if cur_i != cur_height - 1:
                            board_list[cur_i + 1][cur_j].set_shooted()
                    # all decks
                    if cur_j < cur_width - 1:
                        board_list[cur_i][cur_j + 1].set_shooted()
                    if cur_j > 0:
                        board_list[cur_i][cur_j - 1].set_shooted()
                    # index growing
                    cur_i += 1


class ChooseShipButton:
    def __init__(self, head, btn_size, text):
        self.head = self.head_x, self.head_y = head
        self.size = self.width, self.height = btn_size
        self.text = text
        self.btn_color = BUTTON_COLOR
        self.border_color = BORDERS_COLOR

        # allowed ship number
        self.allowed_ship_number = 5 - int(self.text[1:])

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
        if self.allowed_ship_number:
            if self.is_focused(cur_pos):
                self.btn_color = FOCUSED_BUTTON_COLOR
            else:
                self.btn_color = BUTTON_COLOR

    # add ship to board
    def button_pushed(self, cur_pos, cur_board):
        if self.is_focused(cur_pos):
            if not cur_board.placing_ship and self.allowed_ship_number:
                # update color
                self.btn_color = PUSHED_BUTTON_COLOR
                # create new ship
                h_pos = cur_board.get_size()
                new_decks_number = int(self.text[1:])
                cur_board.add_ship(Ship(decks_number=new_decks_number,
                                        head_pos=(h_pos[0] - 1, 0)))
                # allowed ship number updating
                self.allowed_ship_number = max(0, self.allowed_ship_number - 1)
                if not self.allowed_ship_number:
                    self.btn_color = INACTIVE_CELL_COLOR

    def button_unpushed(self, cur_pos):
        if self.is_focused(cur_pos) and self.allowed_ship_number:
            self.btn_color = FOCUSED_BUTTON_COLOR


class Board:
    # создание поля
    def __init__(self, board_width, board_height):
        # size
        self.width = board_width
        self.height = board_height
        # list of boards cells values
        self.board = list()
        # board filling
        self.board_filling()
        # shooted cells
        self.shooted = list()
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

        # the last highlighted cell info
        self.last_highlighted_cell_cords = None

        # new ship placing flag
        self.placing_ship = False

        # required number of ships
        self.need_to_place_ships = 10

    # add ship function
    def add_ship(self, new_ship):
        self.ships.append(new_ship)
        self.ships[-1].set_number(len(self.ships) - 1)
        self.placing_ship = True

    # board filling
    def board_filling(self):
        for _ in range(self.height):
            self.board.append([BoardCell(EMPTY_CELL_COLOR)
                               for nn in range(self.width)])

    def reduce_required_number_of_ships(self):
        self.need_to_place_ships -= 1
        if not self.need_to_place_ships:
            # game status
            global ship_placement_stage, battle_begins_table_need
            ship_placement_stage = False
            battle_begins_table_need = True
            # btn delete
            global choose_ship_btns
            choose_ship_btns.clear()

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_size(self):
        return self.height, self.width

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
            if self.placing_ship:
                self.board = list()
                self.board_filling()
            for btn in choose_ship_btns:
                btn.btn_render()

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
        for ship in self.ships:
            ship.ship_render(self.board)

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
                # cur color
                cur_color = self.board[i][j].get_cell_color()
                pygame.draw.rect(screen, pygame.Color(cur_color),
                                 (cur_cell_x + 3, cur_cell_y + 3,
                                  self.cell_size - 6, self.cell_size - 6), 0,
                                 border_radius=5)
                cur_cell_x += self.cell_size

    def get_cell(self, mouse_pos):
        if 0 < mouse_pos[0] - self.left < self.cell_size * self.width and \
                0 < mouse_pos[1] - self.top < self.cell_size * self.height:
            clicked_cell_i = (mouse_pos[1] - self.top) // self.cell_size
            clicked_cell_j = (mouse_pos[0] - self.left) // self.cell_size

            return clicked_cell_i, clicked_cell_j

    def on_click(self, cell_coords):
        if cell_coords:
            if self.board[cell_coords[0]][cell_coords[1]].get_cell_color() == EMPTY_CELL_COLOR:
                self.board[cell_coords[0]][cell_coords[1]].set_cell_color(SHIP_COLOR)
            else:
                self.board[cell_coords[0]][cell_coords[1]].set_cell_color(EMPTY_CELL_COLOR)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def cell_highlighting(self, mouse_pos):
        # необходимость player_fired ????????
        global player_fired
        cell = self.get_cell(mouse_pos)

        # the last focused cell update
        if self.last_highlighted_cell_cords:
            reset_i, reset_j = self.last_highlighted_cell_cords
            self.board[reset_i][reset_j].set_focused_status(False)
        self.last_highlighted_cell_cords = cell

        # the currently focused cell update
        if cell is not None:
            self.board[cell[0]][cell[1]].set_focused_status(True)

    def get_move(self, cur_pos):
        if self.placing_ship:
            if self.get_cell(cur_pos):
                new_head_i, new_head_j = self.get_cell(cur_pos)
                if self.ships[-1].is_horizontal():
                    new_head_j = min(self.width - self.ships[-1].get_size(), new_head_j)
                else:
                    new_head_i = min(self.height - self.ships[-1].get_size(), new_head_i)
                # set new head position
                self.ships[-1].set_head_pos((new_head_i, new_head_j))

    def is_attacked(self, cell):
        damaged_ship_number = self.board[cell[0]][cell[1]].get_cell_ship_number()
        if damaged_ship_number is not None:
            # shoot to injured cell
            if self.ships[damaged_ship_number].is_deck_injured(cell):
                return True
        return False

    def get_attack(self, curs_pos, cell_attacked=None):
        cell = cell_attacked
        if not cell_attacked:
            cell = self.get_cell(curs_pos)
        global player_fired, player_order
        if cell and not self.is_attacked(cell):
            damaged_ship_number = self.board[cell[0]][cell[1]].get_cell_ship_number()
            if damaged_ship_number is not None:
                # shoot to injured cell
                if self.ships[damaged_ship_number].is_deck_injured(cell):
                    pass
                else:
                    self.ships[damaged_ship_number].set_deck_injured(cell)
                    player_fired = True
            # shoot to empty cell
            else:
                self.board[cell[0]][cell[1]].set_shooted()
                self.shooted.append(cell)
                player_order = not player_order
                player_fired = True


class Bot:
    def __init__(self):
        self.already_shoot = list()

    def get_already_shoot(self):
        return self.already_shoot

    def bot_attack(self, cur_board):
        attacked = (randrange(0, 10), randrange(0, 10))
        while attacked in self.already_shoot:
            attacked = (randrange(0, 10), randrange(0, 10))
        cur_board.get_attack(None, cell_attacked=attacked)
        self.already_shoot.append(attacked)
        if not cur_board.is_attacked(attacked):
            global player_order
            player_order = True

        pygame.time.wait(1500)


def battle_begins_table_render():
    # render table
    table_text = 'The battle begins'
    font = pygame.font.Font(None, 50)
    text = font.render(table_text, True, (100, 255, 100))
    text_x = player_board.left + 115
    text_y = player_board.top + player_board.cell_size * player_board.height + 20
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, PUSHED_BUTTON_COLOR, (text_x - 10, text_y - 10,
                                                   text_w + 20, text_h + 20), 1)


def bot_board_filling(cur_board):
    tec_number = 0
    for new_ship_deck_number in range(1, 5):
        for new_ship_deck_kol in range(5 - new_ship_deck_number):
            # new ship info
            new_head = (randrange(0, 10), randrange(0, 10))
            horiz = bool(randrange(0, 2))
            # ship adding
            cur_board.add_ship(Ship(new_ship_deck_number,
                                    new_head, horiz, tec_number))
            while not cur_board.ships[-1].place_is_ok(cur_board):
                # new ship info
                new_head = (randrange(0, 10), randrange(0, 10))
                horiz = bool(randrange(0, 2))
                cur_board.ships[-1].set_head_pos(new_head)
                if cur_board.ships[-1].is_horizontal() != horiz:
                    cur_board.ships[-1].change_horizontal(cur_board)

            cur_board.ships[-1].ship_render(cur_board.board)
            cur_board.ships[-1].set_bot_status()
            tec_number += 1


def order_table_render(is_player_order):
    # render table
    table_text = 'Bot order'
    if is_player_order:
        table_text = 'Your order'
    font = pygame.font.Font(None, 50)
    text = font.render(table_text, True, (100, 255, 100))
    text_x = screen.get_size()[1] // 2 + 30
    text_y = player_board.top + player_board.cell_size * player_board.height + 20
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, PUSHED_BUTTON_COLOR, (text_x - 10, text_y - 10,
                                                   text_w + 20, text_h + 20), 1)


def game_over_table_render(pl_lose, bt_lose):
    table_text = ''
    if pl_lose:
        table_text = 'You lose!'
    if bt_lose:
        table_text = 'You win!'
    font = pygame.font.Font(None, 50)
    text = font.render(table_text, True, (100, 255, 100))
    text_x = screen.get_size()[1] // 2 + 30
    text_y = player_board.top + player_board.cell_size * player_board.height + 20
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, PUSHED_BUTTON_COLOR, (text_x - 10, text_y - 10,
                                                   text_w + 20, text_h + 20), 1)
    # screen flip
    pygame.display.flip()
    # wait
    pygame.time.wait(2000)


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption('Battleship')
    size = width, height = 700, 700
    screen = pygame.display.set_mode(size)
    player_board = Board(10, 10)
    player_board.set_view(80, 80, 50)

    # ship placement stage
    ship_placement_stage = True
    # game over
    game_over = False
    # start game flag
    battle_begins_table_need = False

    # test items
    # test ship
    # player_board.add_ship(Ship(decks_number=3))

    # choose ship buttons rendering
    choose_ship_btns = list()
    for i in range(1, 5):
        choose_ship_btns.append(
            ChooseShipButton((player_board.left + (i - 1) * 125,
                              player_board.top +
                              player_board.cell_size * 10 + 15),
                             (125, 80), f'x{i}'))

    # fps
    fps = 60
    clock = pygame.time.Clock()

    # placing ships stage
    while ship_placement_stage:
        # checking events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ship_placement_stage = False
                game_over = True
                terminate()

            if event.type == pygame.MOUSEMOTION:
                # choose btns
                if ship_placement_stage:
                    for btns in choose_ship_btns:
                        btns.get_motion(event.pos)
                    player_board.get_move(event.pos)
                # board cells highlighting
                player_board.cell_highlighting(event.pos)

            if event.type == pygame.MOUSEBUTTONDOWN:
                # choose btns
                if ship_placement_stage:
                    for el in choose_ship_btns:
                        el.button_pushed(event.pos, player_board)
                # player_board.get_click(event.pos)

            if event.type == pygame.MOUSEBUTTONUP:
                # choose btns
                if ship_placement_stage:
                    for el in choose_ship_btns:
                        el.button_unpushed(event.pos)

            if event.type == pygame.KEYDOWN:
                if player_board.placing_ship:
                    # space pressing
                    if event.key == pygame.K_SPACE:
                        player_board.ships[-1].change_horizontal(player_board)
                    # enter pressing
                    if event.key == 13:
                        if player_board.ships[-1].place_is_ok(player_board):
                            player_board.placing_ship = False
                            player_board.reduce_required_number_of_ships()

        # screen updating
        screen.fill(BACKGROUND_COLOR)
        # boards ands btns
        player_board.render()
        # battle begins table
        if battle_begins_table_need:
            battle_begins_table_render()

        # screen flip
        pygame.display.flip()

        # battle begins table delete
        if battle_begins_table_need:
            battle_begins_table_need = False
            pygame.time.wait(3000)

        # delay for constant fps
        clock.tick(fps)

    # preparing for game
    bot = Bot()
    player_lose = False
    bot_lose = False
    # player board
    size = width, height = 1000, 700
    screen = pygame.display.set_mode(size)
    player_board.set_view(40, 150, 40)
    # bot board
    bot_board = Board(player_board.width, player_board.height)
    bot_board.set_view(500, 150, 40)
    bot_board_filling(bot_board)
    # order
    player_order = True
    player_fired = False

    # game loop
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                terminate()

            if event.type == pygame.MOUSEMOTION:
                # board cells highlighting
                player_board.cell_highlighting(event.pos)
                bot_board.cell_highlighting(event.pos)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_order:
                    player_fired = False
                    bot_board.get_attack(event.pos)

        # bot order
        if not player_order and not player_fired:
            # bot attack
            player_fired = True
            bot.bot_attack(player_board)

        # screen updating
        screen.fill(BACKGROUND_COLOR)
        # boards
        player_board.render()
        bot_board.render()
        # player fired
        player_fired = False

        # game over finding
        player_lose = True
        bot_lose = True
        for ship in player_board.ships:
            if ship.alive:
                player_lose = False
        for ship in bot_board.ships:
            if ship.alive:
                bot_lose = False

        if player_lose or bot_lose:
            game_over = True

        # render order table
        order_table_render(player_order)

        # screen flip
        pygame.display.flip()
        # delay for constant fps
        clock.tick(fps)

    # boards
    # screen updating
    screen.fill(BACKGROUND_COLOR)
    player_board.render()
    bot_board.render()
    game_over_table_render(player_lose, bot_lose)

    # game ending
    pygame.quit()
