from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.http import require_http_methods
from http import HTTPStatus
from django.http import JsonResponse
from .models import Post
import json
import datetime


def date_time_handler(value):
    if isinstance(value, datetime.date):
        return value.strftime("%Y-%m-%d")
    raise TypeError("not JSON serializable")


@require_http_methods(["GET"])
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by("published_date")
    post_data = json.dumps([post for post in posts.values()], default=date_time_handler)
    return JsonResponse(data={"post_data": post_data}, status=HTTPStatus.OK)


@require_http_methods(["GET"])
def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return JsonResponse(data={}, status=HTTPStatus.NOT_FOUND)
    else:
        post_data = json.dumps(
            {
                "title": post.title,
                "text": post.text,
                "created_date": post.created_date,
                "published_date": post.published_date,
            }, default=date_time_handler
        )

    return JsonResponse(data={"post_data": post_data}, status=HTTPStatus.OK)



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
