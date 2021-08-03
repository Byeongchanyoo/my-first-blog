from django.urls import path
from . import views
urlpatterns = [
    path("post/<int:pk>/edit", views.post_edit, name="post_edit"),
    path("", views.post_list, name="post_list"),

    ]