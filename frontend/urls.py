from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeVIew.as_view(), name="home"),
    path("shop", views.ShopView.as_view(), name="shop"),
]
