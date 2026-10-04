from django.urls import include, path

urlpatterns = [
    path("", include("catalogo.urls")),
    path("materiales/", include("materiales.urls")),
]
