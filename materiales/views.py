from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import MaterialForm
from .models import Material


@require_http_methods(["GET"])
def listar_materiales(request):
    materiales = Material.objects.all()
    return render(request, "materiales/lista.html", {"materiales": materiales})


@require_http_methods(["GET", "POST"])
def crear_material(request):
    if request.method == "POST":
        form = MaterialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("materiales:lista")
    else:
        form = MaterialForm()

    return render(request, "materiales/formulario.html", {"form": form, "accion": "Crear"})


@require_http_methods(["GET", "POST"])
def editar_material(request, pk):
    material = get_object_or_404(Material, pk=pk)

    if request.method == "POST":
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            return redirect("materiales:lista")
    else:
        form = MaterialForm(instance=material)

    return render(
        request,
        "materiales/formulario.html",
        {"form": form, "accion": "Editar", "material": material},
    )


@require_http_methods(["GET", "POST"])
def eliminar_material(request, pk):
    material = get_object_or_404(Material, pk=pk)

    if request.method == "POST":
        material.delete()
        return redirect("materiales:lista")

    return render(request, "materiales/eliminar.html", {"material": material})
