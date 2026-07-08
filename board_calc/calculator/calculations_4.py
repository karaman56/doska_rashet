# calculator/calculations_3.py
import math

def calc_3m(length_board, width_board, price_bord, claymer_price):
    """
    Расчёт количества досок длиной 3 метра.
    Возвращает словарь с результатами: total, ostatok, finish, square.
    """
    parameter_board = 3
    col_board_length = length_board // parameter_board
    ostatok_length = length_board % parameter_board
    col_board_width = math.ceil(width_board / 0.14)

    total_number_board = col_board_width * col_board_length

    if ostatok_length > 0:
        # Добавочные доски в зависимости от остатка
        if ostatok_length <= 0.5:
            dop_board = 0.5
        elif ostatok_length <= 1:
            dop_board = 1
        elif ostatok_length <= 1.5:
            dop_board = 1.5
        else:
            dop_board = 3

        total_number_board += math.ceil(dop_board * col_board_width / parameter_board)

    # Обрезок и крайняя доска
    ostatok = round(parameter_board - (length_board - col_board_length * parameter_board), 1)
    finish = round(parameter_board - ostatok, 1)
    square = round(length_board * width_board, 1)
    # кояймеры, стартовые кляймеры
    start_claymer = round(length_board / 0.4) + 2
    claymer = square * 21 - start_claymer - 2
    pogonyi_metr_board = total_number_board * parameter_board
    total_price_board = pogonyi_metr_board * price_bord
    total_price_claymer = round((claymer + start_claymer) * claymer_price, 1)
    return {
        'total': total_number_board,
        'ostatok': ostatok,
        'finish': finish,
        'square': square,
        'start_claymer': start_claymer,
        'claymer': claymer,
        'pogonyi_metr_board': pogonyi_metr_board,
        'total_price_board': total_price_board,
        'total_price_claymer': total_price_claymer,

    }


def calc_4m(length_board, width_board):
    """
    Расчёт количества досок длиной 4 метра.
    Пока возвращает только total.
    """
    parameter_board = 4
    col_board_length = length_board // parameter_board
    ostatok_length = length_board % parameter_board
    col_board_width = math.ceil(width_board / 0.14)

    total = col_board_width * col_board_length

    if ostatok_length > 0:
        dop_board = math.ceil(ostatok_length)
        total += math.ceil(dop_board * col_board_width / parameter_board)

    # Здесь позже добавишь остальные поля (ostatok, finish, square)
    return {
        'total': total_number_board,
        'ostatok': ostatok,
        'finish': finish,
        'square': square,
        'start_claymer': start_claymer,
        'claymer': claymer,
        'pogonyi_metr_board': pogonyi_metr_board,
        'total_price_board': total_price_board,
        'total_price_claymer': total_price_claymer,

    }
