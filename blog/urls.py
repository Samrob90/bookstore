from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.BlogIndex.as_view(), name="blog"),
    path("<uuid:uuid>/<slug:slug>", views.BlogDetail.as_view(), name="blog_detail"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
