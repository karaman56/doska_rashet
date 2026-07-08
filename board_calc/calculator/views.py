import logging
from django.shortcuts import render, redirect
from django.conf import settings
from django.db.models import Q
from calculator.models import Client, Calculation, PriceSettings
from . import calculations_3
from . import calculations_4


logger = logging.getLogger(__name__)


def save_calculation(
    first_name, last_name, phone, address,
    length, width, board_width_cm, board_type,
    price_board, price_claymer,
    total_boards, total_claymers, total_price,
    ostatok=None, finish_board=None, square_area=None, pogonyi_metr=None,
    comment=''
):
    """
    Сохраняет расчёт в базу ТОЛЬКО если заполнены Имя, Фамилия и Телефон.
    Возвращает True, если сохранение выполнено, иначе False.
    """
    # Проверяем, что все три поля не пустые (даже после удаления пробелов)
    if not (first_name and first_name.strip() and
            last_name and last_name.strip() and
            phone and phone.strip()):
        return False

    # Убираем лишние пробелы
    first_name = first_name.strip().lower()
    last_name = last_name.strip().lower()
    phone = phone.strip()
    address = address.strip() if address else ''

    # Создаём нового клиента (пока без проверки на дубликаты – просто новый)
    client = Client.objects.create(
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        address=address
    )

    # Создаём запись расчёта (дата и время проставятся автоматически)
    Calculation.objects.create(
        client=client,
        length=length,
        width=width,
        board_width_cm=board_width_cm,
        board_type=board_type,
        price_board=price_board,
        price_claymer=price_claymer,
        total_boards=int(total_boards),
        total_claymers=int(total_claymers),
        total_price=total_price,
        ostatok=ostatok,
        finish_board=finish_board,
        square_area=square_area,
        pogonyi_metr=pogonyi_metr,
        comment=comment,
    )

    logger.info(
        f"Расчёт сохранён: клиент={last_name} {first_name}, "
        f"доска={board_type}, длина={length}, ширина={width}, "
        f"ширина_доски={board_width_cm}см, "
        f"кол-во_досок={total_boards}, кляймеров={total_claymers}, "
        f"сумма={total_price}, комментарий='{comment}'"
    )
    return True



def index(request):
    # Контекст с начальными значениями
    context = {
        'result_3m': None, 'result_4m': None,
        'ostatok_3m': None, 'finish_board_3m': None,
        'square_board': None, 'start_claymer': None,
        'claymer': None, 'pogonyi_metr_board': None,
        'total_price_board': None, 'total_price_claymer': None,
        'length_board': None,
        'width_board': None,
        'price_bord_str': None,
        'claymer_price_str': None,
        'board_width_cm': None,
    }

    # Получаем заводские цены из базы
    try:
        price_settings = PriceSettings.objects.get()
        price_board_14 = price_settings.price_board_14cm
        price_board_15 = price_settings.price_board_15cm
        premium_price_14 = price_settings.premium_price_14cm
        premium_price_15 = price_settings.premium_price_15cm
        default_price_claymer = price_settings.price_claymer
        brosh_price = price_settings.brosh_price  # новое
        tesn_price = price_settings.tesn_price  # новое
        brosh_after_tesn_price = price_settings.brosh_after_tesn_price
    except PriceSettings.DoesNotExist:
        price_board_14 = 0.0
        price_board_15 = 0.0
        default_price_claymer = 0.0
        brosh_price = 0.0
        tesn_price = 0.0
        premium_price_14 = 0.0
        premium_price_15 = 0.0

    # Цена доски по умолчанию (для 14 см) – для GET-запроса
    default_price_board = price_board_14

    if request.method == 'POST':
        length_board = float(request.POST.get('length'))
        width_board = float(request.POST.get('width'))
        calc_type = request.POST.get('calc_type')

        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')
        comment = request.POST.get('comment', '')

        # Ширина доски
        board_width_cm_str = request.POST.get('board_width_cm')
        if board_width_cm_str and board_width_cm_str.strip():
            board_width_cm = int(board_width_cm_str)
            board_width_m = board_width_cm / 100.0
        else:
            board_width_cm = 14
            board_width_m = 0.14

        # Переопределяем цену доски в зависимости от выбранной ширины
        if board_width_cm == 15:
            default_price_board = price_board_15
        else:
            default_price_board = price_board_14

        # Цены
        price_bord_str = request.POST.get('price_bord')
        claymer_price_str = request.POST.get('claymer_price')
        price_bord = float(price_bord_str) if price_bord_str and price_bord_str.strip() else 0.0
        claymer_price = float(claymer_price_str) if claymer_price_str and claymer_price_str.strip() else 0.0

        if calc_type == '3m':
            res = calculations_3.calc_3m(length_board, width_board, board_width_m, price_bord, claymer_price)

            context.update({
                'length_board': length_board,
                'width_board': width_board,
                'price_bord': price_bord,
                'claymer_price_str': claymer_price_str,
                'board_width_cm': board_width_cm,
                'result_3m': res['total'],
                'ostatok_3m': res['ostatok'],
                'finish_board_3m': res['finish'],
                'square_board': res['square'],
                'start_claymer': res['start_claymer'],
                'claymer': res['claymer'],
                'pogonyi_metr_board': res['pogonyi_metr_board'],
                'total_price_board': res['total_price_board'],
                'total_price_claymer': res['total_price_claymer'],
            })

            save_calculation(
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                address=address,
                length=length_board,
                width=width_board,
                board_width_cm=board_width_cm,
                board_type='3m',
                price_board=price_bord,
                price_claymer=claymer_price,
                total_boards=res['total'],
                total_claymers=res['claymer'] + res['start_claymer'],
                total_price=res['total_price_board'] + res['total_price_claymer'],
                ostatok=res['ostatok'],
                finish_board=res['finish'],
                square_area=res['square'],
                pogonyi_metr=res['pogonyi_metr_board'],
                comment=comment,
            )

        elif calc_type == '4m':
            res = calculations_4.calc_4m(length_board, width_board)
            context['result_4m'] = res['total']

    # Кладём заводские цены в контекст (теперь default_price_board определена всегда)
    context['price_board_14'] = price_board_14
    context['price_board_15'] = price_board_15
    context['default_price_board'] = default_price_board
    context['default_price_claymer'] = default_price_claymer
    context['brosh_price'] = brosh_price
    context['tesn_price'] = tesn_price
    context['brosh_after_tesn_price'] = brosh_after_tesn_price
    context['premium_price_14'] = premium_price_14
    context['premium_price_15'] = premium_price_15

    return render(request, 'calculator/index.html', context)


def history(request):
    # Достаём все расчёты из базы, сортируем: сначала фамилия клиента (А-Я), потом дата (новые сверху)
    # Если клиента нет (null), такие записи уйдут в конец списка
    calculations = Calculation.objects.select_related('client').order_by('client__last_name', '-created_at')

    # Передаём в шаблон
    return render(request, 'calculator/history.html', {'calculations': calculations})


def client_calculations(request):
    query = request.GET.get('q', '')  # что ввёл пользователь в поисковую строку
    calculations = []
    if query:
        # Ищем расчёты, где фамилия ИЛИ имя клиента содержит запрос (без учёта регистра)
        calculations = Calculation.objects.select_related('client').filter(
            Q(client__last_name__icontains=query) | Q(client__first_name__icontains=query)
        ).order_by('client__last_name', '-created_at')

    return render(request, 'calculator/client_calculations.html', {
        'query': query,
        'calculations': calculations,
    })

def client_list(request):
    clients = Client.objects.order_by('last_name', 'first_name')
    return render(request, 'calculator/client_list.html', {'clients': clients})


def login_view(request):
    """Страница входа: проверяет пароль и пускает на сайт."""
    error = None
    if request.method == 'POST':
        entered_password = request.POST.get('password', '')
        if entered_password == settings.SITE_PASSWORD:
            # Пароль верный – запоминаем в сессии, что пользователь авторизован
            request.session['is_authorized'] = True
            return redirect('calculator:index')   # переходим на главную
        else:
            error = 'Неверный пароль. Попробуйте ещё раз.'

    return render(request, 'calculator/login.html', {'error': error})

def logout_view(request):
    """Выход: удаляем метку из сессии и возвращаем на вход."""
    request.session.pop('is_authorized', None)
    logger.info("Пользователь вышел из системы")
    return redirect('calculator:login')