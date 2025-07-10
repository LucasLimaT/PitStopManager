from django.urls import path

from . import views

app_name = "vehicles"

urlpatterns = [
    path("", views.VehicleListView.as_view(), name="vehicle_list"),
    path("create/", views.VehicleCreateView.as_view(), name="vehicle_create"),
    path("<int:pk>/", views.VehicleDetailView.as_view(), name="vehicle_detail"),
    path("<int:pk>/edit/", views.VehicleUpdateView.as_view(), name="vehicle_edit"),
    path("<int:pk>/delete/", views.VehicleDeleteView.as_view(), name="vehicle_delete"),
    path(
        "<int:pk>/reactivate/",
        views.VehicleReactivateView.as_view(),
        name="vehicle_reactivate",
    ),
]
