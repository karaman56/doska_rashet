from django.db import models


class Client(models.Model):
    first_name = models.CharField(max_length=100)   # имя
    last_name = models.CharField(max_length=100)    # фамилия
    phone = models.CharField(max_length=20)         # номер телефона
    address = models.TextField(blank=True)          # адрес (необязательный)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Calculation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время')

    # Исходные данные
    length = models.FloatField(verbose_name='Длина (м)')
    width = models.FloatField(verbose_name='Ширина (м)')
    board_width_cm = models.IntegerField(verbose_name='Ширина доски (см)')
    board_type = models.CharField(max_length=2, verbose_name='Тип доски')
    price_board = models.FloatField(default=0.0, verbose_name='Цена доски за 1 м²')
    price_claymer = models.FloatField(default=0.0, verbose_name='Цена кляймера')


    # Результаты расчёта
    total_boards = models.IntegerField(verbose_name='Количество досок')
    total_claymers = models.IntegerField(verbose_name='Количество кляймеров')
    total_price = models.FloatField(verbose_name='Общая стоимость')

    # Дополнительные результаты (чтобы всё было как в расчёте)
    ostatok = models.FloatField(null=True, blank=True, verbose_name='Обрезок (м)')
    finish_board = models.FloatField(null=True, blank=True, verbose_name='Крайняя доска (м)')
    square_area = models.FloatField(null=True, blank=True, verbose_name='Площадь (м²)')
    pogonyi_metr = models.FloatField(null=True, blank=True, verbose_name='Погонные метры')
    comment = models.TextField(blank=True, verbose_name='Комментарий')

    def __str__(self):
        return f"Расчёт от {self.created_at:%d.%m.%Y %H:%M}"

    class Meta:
        ordering = ['-created_at']  # новые записи сверху

class PriceSettings(models.Model):
    """Одиночная запись с заводскими ценами (будет всегда одна строка)."""
    price_board_14cm = models.FloatField(default=0.0, verbose_name='Цена доски 14 см за 1 пог. м (руб)')
    price_board_15cm = models.FloatField(default=0.0, verbose_name='Цена доски 15 см за 1 пог. м (руб)')
    premium_price_14cm = models.FloatField(default=749.0, verbose_name='Цена премиум доски 14 см (руб/п.м)')
    premium_price_15cm = models.FloatField(default=557.0, verbose_name='Цена премиум доски 15 см (руб/п.м)')
    price_claymer = models.FloatField(default=0.0, verbose_name='Цена одного кляймера (руб)')
    brosh_price = models.FloatField(default=0.0, verbose_name='Надбавка за брошюрование (руб/п.м)')
    tesn_price = models.FloatField(default=0.0, verbose_name='Надбавка за теснение (руб/п.м)')
    brosh_after_tesn_price = models.FloatField(default=0.0, verbose_name='Надбавка за брошюрование после теснения (руб/п.м)')

    def save(self, *args, **kwargs):
        # Запрещаем создавать больше одной записи
        if not self.pk and PriceSettings.objects.exists():
            raise Exception('Можно создать только один набор настроек. Редактируйте существующий.')
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Розничная цены'

    class Meta:
        verbose_name = 'Настройки цен'
        verbose_name_plural = 'Настройки цен'