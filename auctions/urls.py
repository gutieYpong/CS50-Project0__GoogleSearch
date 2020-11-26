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
    path("<str:item_name>/detail", views.detail, name="detail"),


    
]

