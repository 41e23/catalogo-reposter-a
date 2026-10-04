from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import Material


class MaterialCrudTests(TestCase):
    def setUp(self):
        self.material = Material.objects.create(
            nombre="Harina 0000",
            categoria="Ingredientes",
            stock=25,
            precio=150.00,
            descripcion="Harina para pan y repostería.",
        )
        self.list_url = reverse("materiales:lista")
        self.crear_url = reverse("materiales:crear")
        self.editar_url = reverse("materiales:editar", args=[self.material.pk])
        self.eliminar_url = reverse("materiales:eliminar", args=[self.material.pk])

    def test_listado_muestra_materiales(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Harina 0000")
        self.assertTemplateUsed(response, "materiales/lista.html")

    def test_materiales_disponibles_en_admin(self):
        user = get_user_model().objects.create_superuser(
            username="admin-test",
            email="admin-test@example.com",
            password="test-only-password",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("admin:materiales_material_changelist"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Harina 0000")

    def test_creacion_valida(self):
        payload = {
            "nombre": "Azúcar impalpable",
            "categoria": "Ingredientes",
            "stock": 10,
            "precio": 180.50,
            "descripcion": "Azúcar para decorar y glasear.",
        }

        response = self.client.post(self.crear_url, payload)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.list_url)
        self.assertTrue(Material.objects.filter(nombre="Azúcar impalpable").exists())

    def test_campos_vacios(self):
        response = self.client.post(
            self.crear_url,
            {"nombre": "", "categoria": "", "stock": "", "precio": "", "descripcion": ""},
        )

        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertIn("nombre", form.errors)
        self.assertIn("categoria", form.errors)
        self.assertIn("stock", form.errors)
        self.assertIn("precio", form.errors)

    def test_dato_invalido(self):
        payload = {
            "nombre": "Material inválido",
            "categoria": "Decoración",
            "stock": -3,
            "precio": 0,
            "descripcion": "Precio y stock inválidos.",
        }

        response = self.client.post(self.crear_url, payload)

        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertIn("stock", form.errors)
        self.assertIn("precio", form.errors)

    def test_editar_material(self):
        payload = {
            "nombre": "Harina refinada",
            "categoria": "Ingredientes",
            "stock": 30,
            "precio": 180,
            "descripcion": "Actualizada.",
        }

        response = self.client.post(self.editar_url, payload)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.list_url)
        self.material.refresh_from_db()
        self.assertEqual(self.material.nombre, "Harina refinada")
        self.assertEqual(self.material.stock, 30)

    def test_cancelar_eliminacion_no_borra_registro(self):
        response = self.client.get(self.eliminar_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cancelar")
        self.assertTrue(Material.objects.filter(pk=self.material.pk).exists())

    def test_confirmar_eliminacion(self):
        response = self.client.post(self.eliminar_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.list_url)
        self.assertFalse(Material.objects.filter(pk=self.material.pk).exists())

    def test_error_404_para_registro_inexistente(self):
        response = self.client.get(reverse("materiales:editar", args=[9999]))
        self.assertEqual(response.status_code, 404)

        response = self.client.get(reverse("materiales:eliminar", args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_csrf_requiere_token(self):
        client = Client(enforce_csrf_checks=True)
        payload = {
            "nombre": "Material csrf",
            "categoria": "Utensilios",
            "stock": 5,
            "precio": 200,
            "descripcion": "Sin token.",
        }

        response = client.post(self.crear_url, payload)

        self.assertEqual(response.status_code, 403)
