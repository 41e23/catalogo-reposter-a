from decimal import Decimal

from django import forms

from .models import Material

PRECIO_MINIMO = Decimal("100")


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ["nombre", "categoria", "precio", "disponible", "descripcion"]
        widgets = {
            "nombre": forms.TextInput(attrs={"placeholder": "Ej: Harina sin polvos de hornear"}),
            "precio": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "descripcion": forms.Textarea(attrs={"rows": 3}),
        }
        labels = {
            "nombre": "Nombre del material",
            "categoria": "Categoría",
            "precio": "Precio (CLP)",
            "disponible": "¿Disponible?",
            "descripcion": "Descripción",
        }
        error_messages = {
            "nombre": {"required": "El nombre es obligatorio."},
            "precio": {
                "required": "El precio es obligatorio.",
                "invalid": "Ingresa un precio numérico válido.",
            },
        }

    def clean_precio(self):
        precio = self.cleaned_data["precio"]
        if precio < PRECIO_MINIMO:
            raise forms.ValidationError(
                f"El precio debe ser al menos ${PRECIO_MINIMO} CLP."
            )
        return precio

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"].strip()
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")
        if nombre.isdigit():
            raise forms.ValidationError("El nombre no puede contener solo números.")
        return nombre
