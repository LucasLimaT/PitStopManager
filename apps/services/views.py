from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from apps.vehicles.models import Vehicle

from .forms import ServiceOrderForm
from .models import ServiceOrder

SERVICE_ORDER_LIST_URL = reverse_lazy("services:service_order_list")


class ServiceOrderListView(ListView):
    model = ServiceOrder
    template_name = "services/service_order_list.html"
    context_object_name = "service_orders"
    paginate_by = 10
    queryset = ServiceOrder.active_objects.all()

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .select_related("pk_id_carro", "pk_id_carro__pk_id_cliente")
        )
        vehicle_id = self.request.GET.get("vehicle_id")
        if vehicle_id:
            queryset = queryset.filter(pk_id_carro__pk=vehicle_id)
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(pk_id_carro__placa__icontains=query)
                | Q(pk_id_carro__modelo__icontains=query)
                | Q(pk_id_carro__marca__icontains=query)
                | Q(pk_id_carro__pk_id_cliente__nome__icontains=query)
                | Q(status__icontains=query)
                | Q(descricao_problema__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "")
        service_orders = self.get_queryset()
        context["count_concluidas"] = service_orders.filter(status="CONCLUIDA").count()
        context["count_andamento"] = service_orders.filter(
            status="EM_ANDAMENTO"
        ).count()
        context["count_pendentes"] = service_orders.filter(status="PENDENTE").count()
        vehicle_id = self.request.GET.get("vehicle_id")
        context["vehicle_id"] = vehicle_id
        if vehicle_id:
            try:
                context["vehicle_obj"] = Vehicle.objects.get(pk=vehicle_id)
            except Vehicle.DoesNotExist:
                context["vehicle_obj"] = None
        return context


class ServiceOrderDetailView(DetailView):
    model = ServiceOrder
    template_name = "services/service_order_detail.html"
    context_object_name = "service_order"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("pk_id_carro", "pk_id_carro__pk_id_cliente")
        )


class ServiceOrderCreateView(CreateView):
    model = ServiceOrder
    form_class = ServiceOrderForm
    template_name = "services/service_order_form.html"
    success_url = SERVICE_ORDER_LIST_URL

    def form_valid(self, form):
        messages.success(self.request, "Ordem de Serviço criada com sucesso!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_create_form"] = True
        context["page_title"] = "Nova Ordem de Serviço"
        return context


class ServiceOrderUpdateView(UpdateView):
    model = ServiceOrder
    form_class = ServiceOrderForm
    template_name = "services/service_order_form.html"
    success_url = SERVICE_ORDER_LIST_URL

    def form_valid(self, form):
        messages.success(self.request, "Ordem de Serviço atualizada com sucesso!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_create_form"] = False
        context["page_title"] = "Editar Ordem de Serviço"
        return context


class ServiceOrderDeleteView(DeleteView):
    model = ServiceOrder
    context_object_name = "service_order"
    success_url = SERVICE_ORDER_LIST_URL

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()

        self.object.delete()

        messages.success(
            self.request, f"Ordem de Serviço #{self.object.pk} excluída com sucesso."
        )

        return HttpResponseRedirect(success_url)
