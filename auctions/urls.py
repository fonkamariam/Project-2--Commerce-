from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("show_watchlist", views.show_watchlist, name="show_watchlist"),
    path("add_to_watchlist", views.add_to_watchlist, name="add_to_watchlist"),
    path("remove_from_watchlist", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>", views.get_by_category ,name="get_by_category"),
    path("add_bid", views.add_bid, name="add_bid"),
    path("<int:x>", views.get , name="get")
]
