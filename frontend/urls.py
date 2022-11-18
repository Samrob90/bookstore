from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.HomeVIew.as_view(), name="home"),
    path("shop/", views.ShopView.as_view(), name="shop"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("faq/", views.FaqView.as_view(), name="faq"),
    path("book/<slug:slug>/", views.ProductView.as_view(), name="book-detail"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
