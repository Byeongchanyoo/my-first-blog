from django.test import TestCase
from .models import Post, Comment
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from http import HTTPStatus
import json


class TestPost(TestCase):
    def _create_new_post(self, title, text):
        post = Post.objects.create(
            title=title, text=text, published_date=timezone.now()
        )
        return post

    def _create_new_comment(self, post, author, text):
        comment = Comment.objects.create(
            post=post, author=author, text=text
        )

    def test_post_update_should_return_200_ok(self):
        # Given: post 1개를 생성하고,
        post = self._create_new_post(title="update_test", text="update_text")
        # And: 사용자가 수정을 요구한 데이터를 설정한다음
        put_data = {"title": "updated test title", "text": "updated test text"}

        # When: post_update view 를 호출하면,
        response = self.client.put(reverse("post_edit", kwargs={"pk": post.pk}), data=put_data)

        # Then: status_code가 200으로 리턴되어야 한다
        self.assertEqual(response.status_code, HTTPStatus.OK)
        # And: post의 title이 "updated test title" 이어야 한다.
        updated_post = Post.objects.get(id=post.id)
        self.assertEqual(updated_post.title, "updated test title")
        self.assertEqual(updated_post.text, "updated test text")

    def test_post_update_should_return_404_does_not_exist(self):
        # Given: 유효하지않은 pk 가 주어지고,
        invalid_pk = 123456
        # And: 사용자가 수정을 요구한 데이터를 설정한다음
        put_data = {"title": "updated test title", "text": "updated test text"}

        # When: post_update view를 호출하면,
        response = self.client.put(reverse("post_edit", kwargs={"pk": invalid_pk}), data=put_data)

        # Then: status_code가 404로 되어야 한다.
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_post_update_should_return_400_bad_request(self):
        # Given: post 1개를 생성하고,
        post = self._create_new_post(title="update_test", text="update_text")
        # And: 사용자가 수정을 요구한 데이터를 설정한다음
        put_data = {"title": "updated test title"}

        # When : post update 요청
        response = self.client.put(reverse("post_edit", kwargs={"pk": post.pk}), data=put_data)

        # Then : Bad_Request 반환하는지 확인
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_comment_list_should_return_200_ok_when_use_valid_pk_and_list_length_should_be_30(self):
        # Given: post 1개를 생성하고, 그 포스트에 댓글을 단 후에
        post = self._create_new_post(title="comment_list_test", text="comment_list_text")
        for _ in range(30):
            self._create_new_comment(
                post=post, author="list_test_author", text="list_test_text"
            )

        # When: comment_list view 를 호풀하면,
        response = self.client.get(reverse("comment_list", kwargs={"pk": post.pk}))

        # Then: status_code 가 200 OK 이어야 한다.
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # And: list 의 길이가 30이어야 한다.
        comment_list = json.loads(response.json()["comments_list"])
        self.assertEqual(len(comment_list), 30)
