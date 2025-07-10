from datetime import timedelta

from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import TemplateView

from apps.customers.models import Customer
from apps.inventory.models import Product
from apps.scheduling.models import Appointment
from apps.services.models import ServiceOrder
from apps.vehicles.models import Vehicle


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total_customers = Customer.active_objects.count()
        total_vehicles = Vehicle.active_objects.count()

        pending_orders = ServiceOrder.active_objects.filter(status="PENDENTE").count()
        completed_orders_last_30_days = (
            ServiceOrder.active_objects.filter(
                data_de_entrega__gte=timezone.now() - timedelta(days=30),
                data_de_entrega__isnull=False,
            )
            .exclude(status="CANCELADA")
            .count()
        )

        current_month = timezone.now().replace(day=1)
        monthly_revenue_centavos = (
            ServiceOrder.active_objects.filter(
                data_de_entrega__gte=current_month, data_de_entrega__isnull=False
            )
            .exclude(status="CANCELADA")
            .aggregate(total=Sum("orcamento"))["total"]
            or 0
        )
        monthly_revenue = monthly_revenue_centavos / 100.0

        vehicles_served_this_month = (
            ServiceOrder.active_objects.filter(data_de_entrada__gte=current_month)
            .values("pk_id_carro")
            .distinct()
            .count()
        )

        today = timezone.now().date()
        end_of_week = today + timedelta(days=7)
        appointments_today = Appointment.active_objects.filter(
            data_do_agendamento__date=today
        ).count()
        appointments_next_7_days = Appointment.active_objects.filter(
            data_do_agendamento__date__range=[today, end_of_week]
        ).count()

        recent_service_orders = ServiceOrder.active_objects.select_related(
            "pk_id_carro__pk_id_cliente"
        ).order_by("-data_de_entrada")[:5]
        upcoming_appointments = (
            Appointment.active_objects.select_related("pk_id_carro__pk_id_cliente")
            .filter(data_do_agendamento__gte=timezone.now())
            .order_by("data_do_agendamento")[:5]
        )

        low_stock_products = Product.active_objects.filter(estoque__lte=5).order_by(
            "estoque"
        )[:5]

        monthly_revenues = []
        for i in range(6):
            month_start = timezone.now().replace(day=1) - timedelta(days=i * 30)
            month_start = month_start.replace(day=1)

            if month_start.month == 12:
                next_month = month_start.replace(year=month_start.year + 1, month=1)
            else:
                next_month = month_start.replace(month=month_start.month + 1)

            revenue_centavos = (
                ServiceOrder.active_objects.filter(
                    data_de_entrega__gte=month_start,
                    data_de_entrega__lt=next_month,
                    data_de_entrega__isnull=False,
                )
                .exclude(status="CANCELADA")
                .aggregate(total=Sum("orcamento"))["total"]
                or 0
            )

            monthly_revenues.append(
                {
                    "month": month_start.strftime("%m/%Y"),
                    "month_name": month_start.strftime("%B"),
                    "revenue": revenue_centavos / 100.0,
                }
            )

        context.update(
            {
                "title": "Dashboard - PitStop Manager",
                "total_customers": total_customers,
                "total_vehicles": total_vehicles,
                "pending_orders": pending_orders,
                "completed_orders_last_30_days": completed_orders_last_30_days,
                "monthly_revenue": monthly_revenue,
                "vehicles_served_this_month": vehicles_served_this_month,
                "appointments_today": appointments_today,
                "appointments_next_7_days": appointments_next_7_days,
                "recent_service_orders": recent_service_orders,
                "upcoming_appointments": upcoming_appointments,
                "low_stock_products": low_stock_products,
                "monthly_revenues": monthly_revenues,
            }
        )

        return context


def home(request):
    return render(
        request,
        "core/home.html",
        {"title": "PitStop Manager - Sistema de Gestão para Oficinas"},
    )
