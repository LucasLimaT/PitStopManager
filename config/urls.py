from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("customers/", include("apps.customers.urls")),
    path("vehicles/", include("apps.vehicles.urls")),
    path("inventory/", include("apps.inventory.urls")),
    path("services/", include("apps.services.urls")),
    path("scheduling/", include("apps.scheduling.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
