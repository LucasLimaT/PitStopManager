from django.urls import path

from . import views

app_name = "services"

urlpatterns = [
    path("", views.ServiceOrderListView.as_view(), name="service_order_list"),
    path(
        "create/", views.ServiceOrderCreateView.as_view(), name="service_order_create"
    ),
    path(
        "<int:pk>/", views.ServiceOrderDetailView.as_view(), name="service_order_detail"
    ),
    path(
        "<int:pk>/edit/",
        views.ServiceOrderUpdateView.as_view(),
        name="service_order_edit",
    ),
    path(
        "<int:pk>/delete/",
        views.ServiceOrderDeleteView.as_view(),
        name="service_order_delete",
    ),
]
