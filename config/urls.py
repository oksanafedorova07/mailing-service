from django.contrib import admin
from django.urls import include, path

from mailings.views import home_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("clients/", include("clients.urls", namespace="clients")),
    path("mailings/", include("mailings.urls", namespace="mailings")),
    path("", include("mailings.urls", namespace="mailings")),
    path("users/", include("users.urls", namespace="users")),
    path("", home_view, name="home"),
]
