from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path('', views.home_view, name="admin_home"),

    path('customer', views.customer_view, name="customer"),
    path('customer/<int:pk>', views.customer_detail_view, name="customer-detail"),

    path('login', views.login_view, name="login"),
    path('logout', views.user_logout, name="logout"),

    path('local-transfer', views.local_transfer_view, name="local-transfer"),
    path('external-transfer', views.external_transfer_view, name="external-transfer"),

    path('airtime', views.airtime_view, name="airtime"),
    path('data', views.data_view, name="data"),
    path('cable', views.cable_view, name="cable"),
]
