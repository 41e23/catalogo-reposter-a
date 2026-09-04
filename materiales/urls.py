from django.urls import path
from . import views

app_name = 'materiales'

urlpatterns = [
    path('', views.lista, name='lista'),
]
