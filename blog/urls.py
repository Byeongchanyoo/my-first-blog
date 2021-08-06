from django.urls import path
from . import views
urlpatterns = [
    path("post/<int:pk>/edit", views.post_edit, name="post_edit"),
    path("post/<int:pk>/commentlist", views.comment_list, name="comment_list"),
    ]