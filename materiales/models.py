from django.db import models


class Material(models.Model):
    """Material o insumo de repostería (harina, chocolate, moldes, etc.)."""

    CATEGORIAS = [
        ("harinas", "Harinas y secos"),
        ("azucares", "Azúcares y endulzantes"),
        ("lacteos", "Lácteos y huevos"),
        ("chocolates", "Chocolates y coberturas"),
        ("decoracion", "Decoración"),
        ("utensilios", "Utensilios y moldes"),
        ("otros", "Otros"),
    ]

    nombre = models.CharField(max_length=100)
    categoria = models.CharField("Categoría", max_length=20, choices=CATEGORIAS, default="otros")
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)
    descripcion = models.TextField("Descripción", blank=True)
    fecha_registro = models.DateTimeField("Fecha de registro", auto_now_add=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Material"
        verbose_name_plural = "Materiales"

    def __str__(self):
        return f"{self.nombre} ({self.get_categoria_display()})"
