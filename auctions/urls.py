from django.urls import path

from . import views

app_name = "auctions"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add", views.add_listing, name="add_listing"),
    path("show_listing", views.show_listing, name="show_listing"),
    path("categories", views.categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("<int:product_id>", views.product_view, name="product_view"),
    path("bid", views.bid, name="bid"),
    path("remove", views.remove, name="remove"),
    path("rem", views.rem, name="rem"),
    path("sold", views.sold, name="sold"),
    path("show/<int:category_id>", views.show_category, name="show_category"),
    path("comment", views.user_comments, name="user_comments")
]
