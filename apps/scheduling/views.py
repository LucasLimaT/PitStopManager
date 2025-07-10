from datetime import datetime

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

from .forms import AppointmentForm
from .models import Appointment


class AppointmentListView(ListView):
    model = Appointment
    template_name = "scheduling/appointment_list.html"
    context_object_name = "appointments"
    paginate_by = 10

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .select_related("pk_id_carro", "pk_id_ordem_de_servico")
            .order_by("-data_do_agendamento")
        )
        vehicle_id = self.request.GET.get("vehicle_id")
        if vehicle_id:
            queryset = queryset.filter(pk_id_carro__pk=vehicle_id)
        search_query = self.request.GET.get("search", None)
        date_filter = self.request.GET.get("date_filter", None)

        if search_query:
            queryset = queryset.filter(
                Q(pk_id_carro__placa__icontains=search_query)
                | Q(pk_id_carro__marca__icontains=search_query)
                | Q(pk_id_carro__modelo__icontains=search_query)
                | Q(pk_id_ordem_de_servico__id__icontains=search_query)
                | Q(responsavel__icontains=search_query)
            )

        if date_filter:
            queryset = queryset.filter(data_do_agendamento__date=date_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("search", "")
        context["date_filter"] = self.request.GET.get("date_filter", "")
        vehicle_id = self.request.GET.get("vehicle_id")
        context["vehicle_id"] = vehicle_id
        if vehicle_id:
            try:
                context["vehicle_obj"] = Vehicle.objects.get(pk=vehicle_id)
            except Vehicle.DoesNotExist:
                context["vehicle_obj"] = None
        return context


class AppointmentDetailView(DetailView):
    model = Appointment
    template_name = "scheduling/appointment_detail.html"
    context_object_name = "appointment"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("pk_id_carro", "pk_id_ordem_de_servico")
        )


class AppointmentCreateView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "scheduling/appointment_form.html"
    success_url = reverse_lazy("scheduling:appointment_list")

    def form_valid(self, form):
        messages.success(self.request, "Appointment created successfully.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_create_form"] = True
        return context

    def get_initial(self):
        initial = super().get_initial()
        date_param = self.request.GET.get("date")
        if date_param:
            try:
                date_obj = datetime.strptime(date_param, "%Y-%m-%d")
                date_obj = date_obj.replace(hour=9, minute=0)
                initial["data_do_agendamento"] = date_obj
            except ValueError:
                pass
        return initial


class AppointmentUpdateView(UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "scheduling/appointment_form.html"
    success_url = reverse_lazy("scheduling:appointment_list")

    def form_valid(self, form):
        messages.success(self.request, "Appointment updated successfully.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_create_form"] = False
        return context


class AppointmentDeleteView(DeleteView):
    model = Appointment
    success_url = reverse_lazy("scheduling:appointment_list")
    context_object_name = "appointment"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()

        vehicle_info = (
            str(self.object.pk_id_carro)
            if self.object.pk_id_carro
            else "Veículo Desconhecido"
        )
        appointment_date = (
            self.object.data_do_agendamento.strftime("%d/%m/%Y %H:%M")
            if self.object.data_do_agendamento
            else "Data Desconhecida"
        )

        self.object.delete()

        messages.success(
            self.request,
            f"Agendamento para '{vehicle_info}' em '{appointment_date}' excluído com sucesso.",
        )

        return HttpResponseRedirect(success_url)
