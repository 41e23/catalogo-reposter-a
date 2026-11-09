"""Pruebas de la Evaluación 3: autenticación, CRUD, validación y permisos."""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Material


class MaterialApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='evaluador', password='Clave-Ficticia-123!')
        self.client = APIClient()
        self.material = Material.objects.create(nombre='Harina integral', categoria='harinas', precio='150.00')
        self.url = reverse('api-materiales-list')
        self.detail_url = reverse('api-materiales-detail', args=(self.material.pk,))
        self.payload = {
            'nombre': 'Chocolate amargo', 'categoria': 'chocolates',
            'precio': '250.00', 'disponible': True, 'descripcion': '70% cacao',
        }

    def authenticate(self):
        response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'evaluador', 'password': 'Clave-Ficticia-123!',
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        return response.data

    def test_tokens_y_renovacion(self):
        pair = self.authenticate()
        response = self.client.post(reverse('token_refresh'), {'refresh': pair['refresh']}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)

    def test_get_sin_token_permitido(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_detalle_autorizado(self):
        self.authenticate()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['nombre'], 'Harina integral')

    def test_post_autorizado(self):
        self.authenticate()
        response = self.client.post(self.url, self.payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Material.objects.filter(nombre='Chocolate amargo').exists())

    def test_patch_autorizado(self):
        self.authenticate()
        response = self.client.patch(self.detail_url, {'nombre': 'Harina especial'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.material.refresh_from_db()
        self.assertEqual(self.material.nombre, 'Harina especial')

    def test_put_autorizado(self):
        self.authenticate()
        response = self.client.put(self.detail_url, self.payload, format='json')
        self.assertEqual(response.status_code, 200)
        self.material.refresh_from_db()
        self.assertEqual(self.material.nombre, 'Chocolate amargo')

    def test_delete_autorizado(self):
        self.authenticate()
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Material.objects.filter(pk=self.material.pk).exists())

    def test_post_invalido(self):
        self.authenticate()
        for changes, field in [({'precio': '99.99'}, 'precio'), ({'nombre': '12'}, 'nombre'), ({'categoria': 'no_valida'}, 'categoria'), ({'nombre': ''}, 'nombre')]:
            with self.subTest(changes=changes):
                response = self.client.post(self.url, {**self.payload, **changes}, format='json')
                self.assertEqual(response.status_code, 400)
                self.assertIn(field, response.data)

    def test_post_sin_token_rechazado(self):
        response = self.client.post(self.url, self.payload, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertFalse(Material.objects.filter(nombre='Chocolate amargo').exists())

    def test_modificacion_y_borrado_sin_token_rechazados(self):
        self.assertEqual(self.client.patch(self.detail_url, {'nombre': 'Cambiado'}, format='json').status_code, 401)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 401)
        self.assertTrue(Material.objects.filter(pk=self.material.pk).exists())

    def test_registro_inexistente(self):
        self.assertEqual(self.client.get(reverse('api-materiales-detail', args=(999999,))).status_code, 404)

    def test_token_invalido(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer token-invalido')
        self.assertEqual(self.client.post(self.url, self.payload, format='json').status_code, 401)
