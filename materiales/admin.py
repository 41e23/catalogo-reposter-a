from django.contrib import admin

from .forms import MaterialForm
from .models import Material


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    form = MaterialForm
    list_display = ("nombre", "categoria", "precio", "disponible")
    list_filter = ("categoria", "disponible")
    search_fields = ("nombre", "descripcion")
    list_editable = ("disponible",)
    ordering = ("nombre",)
    readonly_fields = ("fecha_registro",)
