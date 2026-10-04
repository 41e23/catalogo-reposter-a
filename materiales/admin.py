from django.contrib import admin

from .models import Material


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
	list_display = ("nombre", "categoria", "stock", "precio")
	list_filter = ("categoria",)
	search_fields = ("nombre", "categoria", "descripcion")
