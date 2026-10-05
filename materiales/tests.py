from django.contrib import admin
from django.test import Client, TestCase
from django.urls import reverse

from .models import Material


class MaterialCrudTests(TestCase):
    def setUp(self):
        self.material = Material.objects.create(
            nombre="Harina 0000",
            categoria="harinas",
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
        self.assertContains(response, "Harinas y secos")
        self.assertTemplateUsed(response, "materiales/lista.html")

    def test_material_esta_registrado_en_admin(self):
        self.assertIn(Material, admin.site._registry)

    def test_creacion_valida(self):
        payload = {
            "nombre": "Azúcar impalpable",
            "categoria": "azucares",
            "precio": "180.50",
            "descripcion": "Azúcar para decorar y glasear.",
        }

        response = self.client.post(self.crear_url, payload)

        self.assertRedirects(response, self.list_url)
        self.assertTrue(Material.objects.filter(nombre="Azúcar impalpable").exists())

    def test_campos_requeridos_vacios(self):
        response = self.client.post(
            self.crear_url,
            {"nombre": "", "categoria": "", "precio": "", "descripcion": ""},
        )

        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertIn("nombre", form.errors)
        self.assertIn("categoria", form.errors)
        self.assertIn("precio", form.errors)

    def test_validaciones_propias_del_formulario(self):
        for nombre, precio, campo_esperado in [
            ("12", "150", "nombre"),
            ("Material válido", "99.99", "precio"),
        ]:
            with self.subTest(nombre=nombre, precio=precio):
                response = self.client.post(
                    self.crear_url,
                    {
                        "nombre": nombre,
                        "categoria": "otros",
                        "precio": precio,
                        "descripcion": "",
                    },
                )
                self.assertEqual(response.status_code, 200)
                self.assertIn(campo_esperado, response.context["form"].errors)

    def test_editar_material(self):
        payload = {
            "nombre": "Harina refinada",
            "categoria": "harinas",
            "precio": "180.00",
            "descripcion": "Actualizada.",
        }

        response = self.client.post(self.editar_url, payload)

        self.assertRedirects(response, self.list_url)
        self.material.refresh_from_db()
        self.assertEqual(self.material.nombre, "Harina refinada")
        self.assertEqual(self.material.precio, 180.00)

    def test_cancelar_eliminacion_no_borra_registro(self):
        response = self.client.get(self.eliminar_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cancelar")
        self.assertContains(response, 'name="csrfmiddlewaretoken"')
        self.assertTrue(Material.objects.filter(pk=self.material.pk).exists())

    def test_eliminacion_solo_acepta_post(self):
        response = self.client.delete(self.eliminar_url)

        self.assertEqual(response.status_code, 405)
        self.assertTrue(Material.objects.filter(pk=self.material.pk).exists())

    def test_confirmar_eliminacion(self):
        response = self.client.post(self.eliminar_url)

        self.assertRedirects(response, self.list_url)
        self.assertFalse(Material.objects.filter(pk=self.material.pk).exists())

    def test_error_404_para_registro_inexistente(self):
        response = self.client.get(reverse("materiales:editar", args=[9999]))
        self.assertEqual(response.status_code, 404)

        response = self.client.get(reverse("materiales:eliminar", args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_post_sin_token_csrf_es_rechazado(self):
        client = Client(enforce_csrf_checks=True)
        response = client.post(
            self.crear_url,
            {
                "nombre": "Material csrf",
                "categoria": "utensilios",
                "precio": "200",
                "descripcion": "Sin token.",
            },
        )

        self.assertEqual(response.status_code, 403)
