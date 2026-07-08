from django.urls import path
from . import views

app_name = 'calculator'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('history/', views.history, name='history'),
    path('client/', views.client_calculations, name='client_calculations'),  # поиск расчётов клиента
    path('clients/', views.client_list, name='client_list'),                 # база клиентов
]