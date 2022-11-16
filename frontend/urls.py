from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeVIew.as_view(), name="home"),
    path("shop/", views.ShopView.as_view(), name="shop"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("faq/", views.FaqView.as_view(), name="faq"),
]
