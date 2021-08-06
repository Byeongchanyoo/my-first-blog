from django.views.decorators.http import require_http_methods
from http import HTTPStatus
from django.utils import timezone
from django.http import JsonResponse
from .models import Post, Comment
import json

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


@require_http_methods(["PUT"])
def comment_edit(request, pk, id):
    try:
        comment = Comment.objects.select_related('post').get(id=id, pk=pk)
    except Comment.DoesNotExist:
        return JsonResponse(data={}, status=HTTPStatus.NOT_FOUND)
    request_body = json.loads(request.body.decode("utf-8").replace("'", '"'))
    comment.author = request_body["author"]
    comment.text = request_body["text"]
    comment.save()
    return JsonResponse(data={}, status=HTTPStatus.OK)

