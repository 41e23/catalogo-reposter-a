from django.test import TestCase
from django.urls import reverse

from materiales.models import Material


class PortadaTests(TestCase):
    def test_muestra_hasta_tres_materiales_disponibles(self):
        for nombre in ['Chocolate', 'Harina', 'Moldes', 'Vainilla']:
            Material.objects.create(
                nombre=nombre,
                categoria='otros',
                precio=100,
                disponible=True,
            )
        Material.objects.create(
            nombre='Agotado',
            categoria='otros',
            precio=100,
            disponible=False,
        )

        response = self.client.get(reverse('inicio:inicio'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [material.nombre for material in response.context['destacados']],
            ['Chocolate', 'Harina', 'Moldes'],
        )
        self.assertNotContains(response, 'Agotado')

    def test_muestra_mensaje_si_no_hay_materiales_disponibles(self):
        response = self.client.get(reverse('inicio:inicio'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Por el momento no hay productos destacados.')
