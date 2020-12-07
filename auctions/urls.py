from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("category", views.category, name="category"),
    path("category/<str:cate_id>", views.category_listing, name="category_listing"),
    path("newlisting", views.create_listing, name="create_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("<int:item_id>/bidupdate", views.bid_update, name="bid_update"),
    path("<int:item_id>/closebid", views.close_bid, name="close_bid"),
    path("<int:item_id>/add2list", views.add_2_watchlist, name="add_2_watchlist"),
    path("<int:item_id>/comment", views.comment_submit, name="comment_submit"),
    path("<str:item_name>/detail", views.detail, name="detail"),
]