from django.urls import path
from . import views

app_name = "gallery"

urlpatterns = [
    path("", views.index, name="index"),
    path("add/", views.add, name="add"),
    path("view/<int:art_id>/", views.view, name="view"),
    path("edit/<int:art_id>/", views.edit, name="edit"),
    path("delete/<int:art_id>/", views.delete, name="delete"),
    path("favorite/<int:artwork_id>/", views.toggle_favorite, name="toggle_favorite"),
    path("favorites/", views.favorites, name="favorites"),
    path("api/favorite/status/<int:artwork_id>/", views.favorite_status, name="favorite_status"),
]
