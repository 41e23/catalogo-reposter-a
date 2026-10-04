from django.shortcuts import get_object_or_404, redirect, render

from .forms import MaterialForm
from .models import Material


def listar_materiales(request):
    materiales = Material.objects.all().order_by("nombre")
    return render(request, "materiales/lista.html", {"materiales": materiales})


def crear_material(request):
    if request.method == "POST":
        form = MaterialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("materiales:lista")
    else:
        form = MaterialForm()

    return render(request, "materiales/formulario.html", {"form": form, "accion": "Crear"})


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


def eliminar_material(request, pk):
    material = get_object_or_404(Material, pk=pk)

    if request.method == "POST":
        material.delete()
        return redirect("materiales:lista")

    return render(request, "materiales/eliminar.html", {"material": material})
