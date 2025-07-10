from django.urls import path

from . import views

app_name = "scheduling"

urlpatterns = [
    path("", views.AppointmentListView.as_view(), name="appointment_list"),
    path("create/", views.AppointmentCreateView.as_view(), name="appointment_create"),
    path("<int:pk>/", views.AppointmentDetailView.as_view(), name="appointment_detail"),
    path(
        "<int:pk>/edit/", views.AppointmentUpdateView.as_view(), name="appointment_edit"
    ),
    path(
        "<int:pk>/delete/",
        views.AppointmentDeleteView.as_view(),
        name="appointment_delete",
    ),
]
