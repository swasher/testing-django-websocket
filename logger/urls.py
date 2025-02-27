from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('log/', views.log_view, name='log'),  # Добавили новый путь для log.html
    path('add_name/', views.add_name, name='add_name'),
]
