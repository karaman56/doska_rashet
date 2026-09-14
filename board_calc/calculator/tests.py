import math

from django.contrib.admin.templatetags.admin_list import result_list
from django.db.models.expressions import result


def calc_4m(length_board, width_board):
    """
    Расчёт количества досок длиной 4 метра.
    Пока возвращает только total.
    """


    parameter_board = 4
    col_board_length = length_board // parameter_board
    print(col_board_length, 'Кол досок по 4 м')
    ostatok_length = length_board % parameter_board
    print(ostatok_length, 'остаток метров')
    col_board_width = math.ceil(width_board / 0.14)
    print(col_board_width, "Количество по ширине ")

    total = col_board_width * col_board_length
    print(total, "Общая без доп")

    if ostatok_length > 0:
        dop_board = math.ceil(ostatok_length)
        total = total + math.ceil(dop_board * col_board_width / parameter_board)
    return(total)

result =  calc_4m(10,2)
print (result)


    # Здесь позже добавишь остальные поля (ostatok, finish, square)
    #return {
        #'total': total_number_board,
        #'ostatok': ostatok,
        #'finish': finish,
        #'square': square,
        #'start_claymer': start_claymer,
        #'claymer': claymer,
        #'pogonyi_metr_board': pogonyi_metr_board,
        #'total_price_board': total_price_board,
        #'total_price_claymer': total_price_claymer,

    #}
