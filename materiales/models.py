from django.db import models


class Material(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50)
    stock = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre
