from django.views.decorators.http import require_http_methods
from http import HTTPStatus
from django.http import JsonResponse
from .models import Post, Comment
import json
import datetime


def date_time_handler(value):
    if isinstance(value, datetime.date):
        return value.strftime("%Y-%m-%d")
    raise TypeError("not JSON serializable")


@require_http_methods(["PUT"])
def post_edit(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return JsonResponse(data={}, status=HTTPStatus.NOT_FOUND)
    request_body = json.loads(request.body.decode("utf-8").replace("'", '"'))

    try:
        post.title = request_body["title"]
        post.text = request_body["text"]
    except KeyError:
        return JsonResponse(data={}, status=HTTPStatus.BAD_REQUEST)
    else:
        post.save()
    return JsonResponse(data={}, status=HTTPStatus.OK)


@require_http_methods(["GET"])
def comment_list(request, pk):
    post = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(post=post)
    comments_list = json.dumps([comment for comment in comments.values()], default=date_time_handler)
    return JsonResponse(data={"comments_list": comments_list}, status=HTTPStatus.OK)