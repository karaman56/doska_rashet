from django.shortcuts import redirect

class PasswordCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Страницы, которые должны быть доступны без пароля
        exempt_urls = ['/login/', '/logout/']

        # Если запрашиваемая страница НЕ в списке exempt_urls
        if request.path not in exempt_urls:
            # и пользователь не авторизован (нет метки в сессии)
            if not request.session.get('is_authorized'):
                return redirect('calculator:login')

        # Если всё хорошо – пропускаем запрос дальше к обычному view
        response = self.get_response(request)
        return response