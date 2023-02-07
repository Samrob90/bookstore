from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

LOGIN_URL = "cpanel_login"

urlpatterns = [
    path("", views.CpanelLoginView.as_view(), name="cpanel_login"),
    path(
        "dashboard/",
        login_required(views.CpanelDashboardView.as_view(), login_url=LOGIN_URL),
        name="cpanel_dashboard",
    ),
    path(
        "books/",
        login_required(views.CpanelBooksView.as_view(), login_url=LOGIN_URL),
        name="cpanel_books",
    ),
    path(
        "add-book",
        login_required(views.CpanelAddbookView.as_view(), login_url=LOGIN_URL),
        name="cpanel_addbook",
    ),
    path(
        "orders",
        login_required(views.OrdersViews.as_view(), login_url=LOGIN_URL),
        name="cpanel_new_orders",
    ),
    path(
        "order/<pk>/",
        login_required(views.NewOrderDetails.as_view(), login_url=LOGIN_URL),
        name="cpanel_order_detials",
    ),
    path(
        "orders/in_progress/",
        login_required(views.OrderInProgress.as_view(), login_url=LOGIN_URL),
        name="order_in_progress",
    ),
    path(
        "orders/completed/",
        login_required(views.CompletedOrder.as_view(), login_url=LOGIN_URL),
        name="cpanel_completed_order",
    ),
    path(
        "get_notification/",
        login_required(views.CpanelGet_notigication.as_view(), login_url=LOGIN_URL),
        name="get_notification",
    ),
    path(
        "bookfinder/",
        login_required(views.BookFinder.as_view(), login_url=LOGIN_URL),
        name="bookfinder",
    ),
    path(
        "bookdetail/<pk>/",
        login_required(views.CpanelBookEdit.as_view(), login_url=LOGIN_URL),
        name="cpanel_book_edit",
    ),
    path(
        "dealofweek/",
        login_required(views.DealofWeek.as_view(), login_url=LOGIN_URL),
        name="cpanel_dealofweek",
    ),
    path(
        "onsale/",
        login_required(views.OnSale.as_view(), login_url=LOGIN_URL),
        name="cpanel_onsale",
    ),
    path("logout/", views.CpanelLogoutVIew.as_view(), name="cpanel_logout"),
]
