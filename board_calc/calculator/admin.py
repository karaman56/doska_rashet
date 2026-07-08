from django.contrib import admin
from .models import Client, Calculation, PriceSettings


# Клиентов показываем как обычно
admin.site.register(Client)


@admin.register(PriceSettings)
class PriceSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        """Запрещаем создавать новую запись, если уже есть хотя бы одна."""
        if PriceSettings.objects.exists():
            return False
        return True


@admin.register(Calculation)
class CalculationAdmin(admin.ModelAdmin):
    list_display = (
        'client_name',
        'client_phone',          # <- теперь этот метод есть внутри класса
        'board_type',
        'length',
        'width',
        'board_width_cm',
        'price_board',
        'price_claymer',
        'total_boards',
        'total_claymers',
        'total_price',
        'ostatok',
        'finish_board',
        'square_area',
        'pogonyi_metr',
        'created_at_formatted',
    )

    ordering = ('client__last_name', '-created_at')

    search_fields = (
        'client__last_name',
        'client__first_name',
        'client__phone',
    )

    # Методы для отображения данных клиента
    @admin.display(description='Клиент', ordering='client__last_name')
    def client_name(self, obj):
        if obj.client:
            return f"{obj.client.last_name} {obj.client.first_name}"
        return "—"

    @admin.display(description='Телефон клиента', ordering='client__phone')
    def client_phone(self, obj):
        return obj.client.phone if obj.client else "—"

    @admin.display(description='Дата и время', ordering='created_at')
    def created_at_formatted(self, obj):
        return obj.created_at.strftime('%d.%m.%Y %H:%M')