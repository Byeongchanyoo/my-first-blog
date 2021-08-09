from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.http import require_http_methods
from http import HTTPStatus
from django.http import JsonResponse
from .models import Post
import json


@require_http_methods(["POST"])
def post_new(request):
    post_data = request.POST
    if post_data.get("title") is None or post_data.get("text") is None:
        return JsonResponse(data={}, status=HTTPStatus.BAD_REQUEST)

    post = Post.objects.create(
        title=post_data["title"], text=post_data["text"]
    )

    return JsonResponse(data={"id": post.id}, status=HTTPStatus.CREATED)


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
