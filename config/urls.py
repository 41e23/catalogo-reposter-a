from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("catalogo.urls")),
    path("inicio/", include("inicio.urls")),
    path("materiales/", include("materiales.urls")),
    path("proveedores/", include("proveedores.urls")),
]
