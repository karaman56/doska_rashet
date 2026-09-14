import math



def calc_4m(length_board, width_board, claymer_price=None):
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

    ostatok = round(parameter_board - (length_board - col_board_length * parameter_board), 1)
    finish = round(parameter_board - ostatok, 1)
    square = round(length_board * width_board, 1)
    # кояймеры, стартовые кляймеры
    start_claymer = round(length_board / 0.4) + 2
    claymer = round(square * 25 - start_claymer)
    pogonyi_metr_board = total_number_board * parameter_board
    total_price_board = pogonyi_metr_board * price_bord
    total_price_claymer = round((claymer + start_claymer) * claymer_price, 1)
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
