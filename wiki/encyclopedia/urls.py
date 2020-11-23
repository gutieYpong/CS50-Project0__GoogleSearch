from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("newpage/", views.newpage, name="newpage"),
    path("randompage/", views.randompage, name="randompage"),
    path("edit/<str:subject>", views.editpage, name="editpage"),
    path("<str:title>", views.content, name="content"),
]