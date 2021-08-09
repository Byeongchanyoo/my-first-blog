from django.urls import path
from . import views
urlpatterns = [
    path("post/<int:pk>/edit", views.post_edit, name="post_edit"),
    path("post/new/", views.post_new, name="post_new"),
    ]