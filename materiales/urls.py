from django.urls import path

from . import views

app_name = "materiales"

urlpatterns = [
    path("", views.listar_materiales, name="lista"),
    path("crear/", views.crear_material, name="crear"),
    path("editar/<int:pk>/", views.editar_material, name="editar"),
    path("eliminar/<int:pk>/", views.eliminar_material, name="eliminar"),
]
