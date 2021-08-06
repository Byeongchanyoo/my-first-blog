from django.urls import path
from . import views
urlpatterns = [
    path("post/<int:pk>/edit", views.post_edit, name="post_edit"),
    path("post/<int:pk>/comment/<int:id>/", views.comment_edit, name="comment_edit"),
    ]