from django.urls import path

from . import views

app_name = "cdshelf"
urlpatterns = [
    path("", views.home, name="home"),
    path("artist/<int:artist_id>/", views.artist, name="artist"),
    path("cd/<int:cd_id>/", views.cd, name="cd"),
    path("source_dirs/", views.source_dirs, name="sourc_dirs"),
    path(
        "load_source_dir/<int:source_dir_id>/",
        views.load_source_dir,
        name="load_source_dir",
    ),
]
