from django.urls import path

urlpatterns = [
    path('', views.list_orders, name="orders"),
]
