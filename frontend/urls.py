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
    path(
        "book/<slug:slug>/<uuid>/",
        views.ProductView.as_view(),
        name="book-detail",
    ),
    path("shopacc/", views.shopCart.as_view(), name="shopacc"),
    path("cart/", views.CartViews.as_view(), name="cart"),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path(
        "order/success/<ordernumber>/",
        views.OrderSuccess,
        name="ordersuccess",
    ),
    path("reviews/", views.bookReview.as_view(), name="review"),
    path("reviews/<pk>/", views.RatingsView.as_view(), name="allcomment"),
    path("author/<pk>/", views.authorsDetail.as_view(), name="author_single"),
    path("categories/", views.CategoriesView.as_view(), name="categories_list"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
