
import pygame
import pygame_menu

from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, WHITE, BLACK, ABOUT, FPS, DIFFICULTY, GAME_NAME
from checkers.game import Game
from negamax.negamax import negamax
from negamax.transposition_table import TranspositionTable
from enum import Enum
import secrets


class Difficulty(Enum):
    EASY = 'easy'
    MEDIUM = 'medium'
    HARD = 'hard'


clock, main_menu, surface = None, None, None

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(GAME_NAME)


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def random_move(game):
    piece, move = secrets.choice(game.board.get_all_valid_moves(WHITE))
    if len(move[1]) > 0:
        game.board.remove(move[1])
    pygame.time.delay(1000)
    game.board.move(piece, move[0][0], move[0][1])


def has_move(game, run, color):
    have_move = False
    for piece in game.board.get_pieces(color):
        for _ in game.board.get_valid_moves(piece).items():
            have_move = True
            break
    winner = game.get_winner
    if not have_move:
        color = WHITE if color == BLACK else BLACK
        game.winner = color
        winner = game.winner
        run = False
    return winner, run


def run_game(difficulty):
    assert isinstance(difficulty, list)
    difficulty = difficulty[0]
    assert isinstance(difficulty, str)

    global main_menu
    global clock
    global surface

    main_menu.disable()
    main_menu.full_reset()

    run = True
    game = Game(WIN)
    transposition_table = TranspositionTable()
    transposition_table.from_file()

    while run:
        clock.tick(FPS)
        alpha = float("-inf")
        beta = float("inf")
        if game.turn == WHITE:
            winner, run = has_move(game, run, WHITE)
            if difficulty == Difficulty.EASY.name:
                if secrets.SystemRandom().random() < 0.3:
                    value, next_board = negamax(game.board, 5, WHITE, 1, game, alpha, beta, transposition_table)
                    game.board = next_board
                else:
                    random_move(game)
            elif difficulty == Difficulty.MEDIUM.name:
                if secrets.SystemRandom().random() < 0.7:
                    value, next_board = negamax(game.board, 5, WHITE, 1, game, alpha, beta, transposition_table)
                    game.board = next_board
                else:
                    random_move(game)
            else:
                value, next_board = negamax(game.board, 5, WHITE, 1, game, alpha, beta, transposition_table)
                game.board = next_board
            game.change_turn()

        if game.get_winner is not None:
            winner = game.get_winner
            run = False

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu.enable()

                    # Quit this function, then skip to loop of main-menu on line 224
                    return

        if main_menu.is_enabled():
            main_menu.update(events)

        if game.turn == BLACK:
            winner, run = has_move(game, run, BLACK)

        game.update()

    transposition_table.to_file()

    game_over_theme = pygame_menu.themes.THEME_DEFAULT.copy()
    game_over_theme.widget_margin = (0, 0)

    game_over_menu = pygame_menu.Menu(
            height=HEIGHT * 0.6,
            theme=game_over_theme,
            title='GAME OVER',
            width=WIDTH * 0.6
        )
    game_over_menu.add.label('GAME OVER', align=pygame_menu.locals.ALIGN_CENTER, font_size=40)

    if winner == WHITE:
        winner_statement = 'AI wins!'
    else:
        winner_statement = 'Human wins!'

    game_over_menu.add.label(winner_statement, align=pygame_menu.locals.ALIGN_CENTER, font_size=30)
    game_over_menu.add.vertical_margin(30)
    game_over_menu.add.button('Return to menu', main_menu)

    game_over_menu.enable()
    game_over_menu.mainloop(surface, main_background, fps_limit=FPS)

    return


def main_background() -> None:
    """
    Function used by menus, draw on background while menu is active.
    """
    global surface
    surface.fill((128, 0, 128))


def set_difficulty(value, difficulty):
    DIFFICULTY[0] = difficulty


def main():

    global clock
    global main_menu
    global surface

    clock = pygame.time.Clock()
    surface = WIN

    play_menu = pygame_menu.Menu(
        height=HEIGHT * 0.7,
        title='Play Menu',
        width=WIDTH * 0.75
    )

    play_menu.add.button('Start',  # When pressing return -> play(DIFFICULTY[0], font)
                         run_game,
                         DIFFICULTY)
    play_menu.add.selector('Select difficulty ',
                           [('1 - Easy', Difficulty.EASY.name),
                            ('2 - Medium', Difficulty.MEDIUM.name),
                            ('3 - Hard', Difficulty.HARD.name)],
                           onchange=set_difficulty,
                           selector_id='select_difficulty')
    play_menu.add.button('Return to main menu', pygame_menu.events.BACK)

    about_theme = pygame_menu.themes.THEME_DEFAULT.copy()
    about_theme.widget_margin = (0, 0)

    about_menu = pygame_menu.Menu(
        height=HEIGHT * 0.6,
        theme=about_theme,
        title='About',
        width=WIDTH * 0.6
    )

    for m in ABOUT:
        about_menu.add.label(m, align=pygame_menu.locals.ALIGN_LEFT, font_size=20)
    about_menu.add.vertical_margin(30)
    about_menu.add.button('Return to menu', pygame_menu.events.BACK)

    main_theme = pygame_menu.themes.THEME_DEFAULT.copy()

    main_menu = pygame_menu.Menu(
        height=HEIGHT * 0.6,
        theme=main_theme,
        title='Main Menu',
        width=WIDTH * 0.6
    )

    main_menu.add.button('Play', play_menu)
    main_menu.add.button('About', about_menu)
    main_menu.add.button('Quit', pygame_menu.events.EXIT)

    while True:

        # Tick
        clock.tick(FPS)

        # Paint background
        main_background()

        # Application events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        # Main menu
        if main_menu.is_enabled():
            main_menu.mainloop(surface, main_background, fps_limit=FPS)

        # Flip surface
        pygame.display.flip()


if __name__ == '__main__':
    main()
