from django.urls import path

from . import views

app_name = "inventory"

urlpatterns = [
    path("", views.ProductListView.as_view(), name="product_list"),
    path("products/create/", views.ProductCreateView.as_view(), name="product_create"),
    path(
        "products/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"
    ),
    path(
        "products/<int:pk>/edit/",
        views.ProductUpdateView.as_view(),
        name="product_edit",
    ),
    path(
        "products/<int:pk>/delete/",
        views.ProductDeleteView.as_view(),
        name="product_delete",
    ),
]
