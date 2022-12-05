from django.urls import path, include
from . import views

urlpatterns = [path("", views.BlogIndex.as_view(), name="blog")]
