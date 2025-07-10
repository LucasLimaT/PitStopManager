from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from apps.services.models import ServiceOrder

from .forms import CustomerForm
from .models import Customer


class CustomerListView(ListView):
    model = Customer
    template_name = "customers/customer_list.html"
    context_object_name = "customers"
    paginate_by = 20
    queryset = Customer.active_objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(nome__icontains=search) | queryset.filter(
                telefone__icontains=search
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        now = timezone.now()
        customers_with_appointments = (
            Customer.active_objects.filter(
                vehicles__appointments__data_do_agendamento__gte=now
            )
            .distinct()
            .count()
        )
        context["customers_with_appointments"] = customers_with_appointments

        context["new_customers_this_month"] = Customer.active_objects.filter(
            created_at__year=now.year, created_at__month=now.month
        ).count()

        context["customers_with_vehicles"] = (
            Customer.active_objects.filter(vehicles__isnull=False).distinct().count()
        )
        return context


class CustomerDetailView(DetailView):
    model = Customer
    template_name = "customers/customer_detail.html"
    context_object_name = "customer"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.get_object()

        context["customer_vehicles"] = customer.vehicles.filter(is_active=True)

        try:
            context["customer_service_orders"] = (
                ServiceOrder.objects.filter(
                    pk_id_carro__pk_id_cliente=customer, is_active=True
                )
                .select_related("pk_id_carro")
                .order_by("-created_at")[:10]
            )
        except ImportError:
            context["customer_service_orders"] = []

        return context


class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = "customers/customer_form.html"
    success_url = reverse_lazy("customers:customer_list")

    def form_valid(self, form):
        messages.success(self.request, "Cliente criado com sucesso!")
        return super().form_valid(form)


class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = "customers/customer_form.html"
    success_url = reverse_lazy("customers:customer_list")

    def form_valid(self, form):
        messages.success(self.request, "Cliente atualizado com sucesso!")
        return super().form_valid(form)


class CustomerDeleteView(DeleteView):
    model = Customer
    context_object_name = "customer"
    success_url = reverse_lazy("customers:customer_list")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()

        customer_name = self.object.nome
        self.object.delete()

        messages.success(self.request, f"Cliente {customer_name} excluído com sucesso.")

        return HttpResponseRedirect(success_url)
