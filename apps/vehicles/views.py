from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View,
)

from apps.customers.models import Customer

from .forms import VehicleForm
from .models import Vehicle


class VehicleListView(ListView):
    model = Vehicle
    template_name = "vehicles/vehicle_list.html"
    context_object_name = "vehicles"
    paginate_by = 10
    queryset = Vehicle.active_objects.all()

    def get_queryset(self):
        queryset = super().get_queryset().select_related("pk_id_cliente")
        search_query = self.request.GET.get("search", "")
        if search_query:
            queryset = queryset.filter(
                Q(marca__icontains=search_query)
                | Q(modelo__icontains=search_query)
                | Q(placa__icontains=search_query)
                | Q(pk_id_cliente__nome__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("search", "")
        return context


class VehicleDetailView(DetailView):
    model = Vehicle
    template_name = "vehicles/vehicle_detail.html"
    context_object_name = "vehicle"

    def get_queryset(self):
        return super().get_queryset().select_related("pk_id_cliente")


class VehicleCreateView(CreateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = "vehicles/vehicle_form.html"
    success_url = reverse_lazy("vehicles:vehicle_list")

    def form_valid(self, form):
        messages.success(self.request, "Veículo criado com sucesso.")
        return super().form_valid(form)

    def form_invalid(self, form):
        placa_errors = form.errors.get("placa", [])
        for error in placa_errors:
            if str(error).startswith("DELETED_VEHICLE_EXISTS:"):
                vehicle_id = str(error).split(":")[1]
                deleted_vehicle = Vehicle.objects.get(pk=vehicle_id)
                messages.warning(
                    self.request,
                    f"Existe um veículo deletado com a placa {deleted_vehicle.placa}. "
                    f"Veículo: {deleted_vehicle.marca} {deleted_vehicle.modelo} {deleted_vehicle.ano}. "
                    f"Deseja reativá-lo?",
                )
                context = self.get_context_data(form=form)
                context["deleted_vehicle"] = deleted_vehicle
                context["show_reactivate_option"] = True
                return self.render_to_response(context)

        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_create_form"] = True
        return context

    def get_initial(self):
        initial = super().get_initial()
        customer_id = self.request.GET.get("customer")
        if customer_id:
            try:
                customer = Customer.objects.get(pk=customer_id)
                initial["pk_id_cliente"] = customer
            except Customer.DoesNotExist:
                pass
        return initial


class VehicleReactivateView(View):
    def post(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk, is_active=False)
        vehicle.reactivate()
        messages.success(request, f"Veículo {vehicle.placa} reativado com sucesso!")
        return redirect("vehicles:vehicle_detail", pk=vehicle.pk)


class VehicleUpdateView(UpdateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = "vehicles/vehicle_form.html"
    success_url = reverse_lazy("vehicles:vehicle_list")

    def form_valid(self, form):
        messages.success(self.request, "Veículo atualizado com sucesso.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_create_form"] = False
        return context


class VehicleDeleteView(DeleteView):
    model = Vehicle
    success_url = reverse_lazy("vehicles:vehicle_list")
    context_object_name = "vehicle"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()

        vehicle_info = f"{self.object.marca} {self.object.modelo} ({self.object.placa})"
        self.object.delete()

        messages.success(self.request, f"Veículo {vehicle_info} excluído com sucesso.")

        return HttpResponseRedirect(success_url)
