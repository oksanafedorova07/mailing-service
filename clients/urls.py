from django.urls import path

from .views import (ClientCreateView, ClientDeleteView, ClientDetailView,
                    ClientListView, ClientUpdateView)

app_name = "clients"

urlpatterns = [
    path("", ClientListView.as_view(), name="client_list"),
    path("<int:pk>/", ClientDetailView.as_view(), name="client_detail"),
    path("create/", ClientCreateView.as_view(), name="client_create"),
    path("<int:pk>/update/", ClientUpdateView.as_view(), name="client_update"),
    path("<int:pk>/delete/", ClientDeleteView.as_view(), name="client_delete"),
]
