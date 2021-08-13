from django.views.decorators.http import require_http_methods
from http import HTTPStatus
from django.utils import timezone
from django.http import JsonResponse
from .models import Post, Comment
import json


@require_http_methods(["PUT"])
def post_edit(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
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


@require_http_methods(["DELETE"])
def comment_delete(request, post_id, comment_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse(data={}, status=HTTPStatus.NOT_FOUND)
    else:
        comment = Comment.objects.get(post=post, id=comment_id)
        comment.delete()
    return JsonResponse(data={}, status=HTTPStatus.NO_CONTENT)
