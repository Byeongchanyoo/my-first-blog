from django.urls import path
from . import views
urlpatterns = [
    path("post/<int:pk>/edit", views.post_edit, name="post_edit"),
    path("post/<int:pk>/comment", views.comment_new, name="comment_new"),
    ]