from django.urls import path
from . import views
urlpatterns = [
    path("post/<int:post_id>/edit", views.post_edit, name="post_edit"),
    path("post/<int:post_id>/delete/comment/<int:comment_id>", views.comment_delete, name="comment_delete")
    ]