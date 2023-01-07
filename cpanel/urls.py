from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", views.CpanelLoginView.as_view(), name="cpanel_login"),
    path(
        "dashboard/",
        login_required(views.CpanelDashboardView.as_view(), login_url="cpanel_login"),
        name="cpanel_dashboard",
    ),
    path(
        "books/",
        login_required(views.CpanelBooksView.as_view(), login_url="cpanel_login"),
        name="cpanel_books",
    ),
    path(
        "add-book",
        login_required(views.CpanelAddbookView.as_view(), login_url="cpanel_login"),
        name="cpanel_addbook",
    ),
    path(
        "orders",
        login_required(views.OrdersViews.as_view(), login_url="cpanel_login"),
        name="cpanel_new_orders",
    ),
    path(
        "order/<pk>/",
        login_required(views.NewOrderDetails.as_view(), login_url="cpanel_login"),
        name="cpanel_order_detials",
    ),
    path("logout/", views.CpanelLogoutVIew.as_view(), name="cpanel_logout"),
]
