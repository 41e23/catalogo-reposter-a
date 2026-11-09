"""Serialización de materiales usando las reglas comerciales del CRUD HTML."""
from decimal import Decimal

from rest_framework import serializers

from .models import Material


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ('id', 'nombre', 'categoria', 'precio', 'disponible', 'descripcion', 'fecha_registro')
        read_only_fields = ('id', 'fecha_registro')
        extra_kwargs = {
            'nombre': {'required': True, 'allow_blank': False, 'trim_whitespace': True},
            'precio': {'required': True},
        }

    def validate_nombre(self, value):
        nombre = value.strip()
        if len(nombre) < 3:
            raise serializers.ValidationError('El nombre debe tener al menos 3 caracteres.')
        if nombre.isdigit():
            raise serializers.ValidationError('El nombre no puede contener solo números.')
        return nombre

    def validate_precio(self, value):
        if value < Decimal('100.00'):
            raise serializers.ValidationError('El precio debe ser al menos $100 CLP.')
        return value
