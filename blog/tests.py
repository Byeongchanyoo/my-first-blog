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

    def test_comment_new_should_return_201_created_when_use_valid_pk_and_valid_data_and_response_should_be_same(self):
        # Given: post 객체를 생성하고, valid 한 pk와 valid 한 데이터로,
        post = self._create_new_post(title="comment_test_title", text="comment_test_text")
        valid_data = {"author": "test_comment_author", "text": "test_comment_author"}

        # When: comment_new view 를 호출하면,
        response = self.client.post(reverse("comment_new", kwargs={"pk": post.pk}),data=valid_data)

        # Then: status_code 가 201 CREATED 이어야 한다.
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

        # And: 전달받은 content 와 valid_data 의 content 가 같아야 한다.
        comment_data = Comment.objects.get(post=post)
        self.assertEqual(comment_data.author, valid_data["author"])
        self.assertEqual(comment_data.text, valid_data["text"])

    def test_comment_new_should_return_404_not_found_when_use_invalid_pk(self):
        # Given: invalid 한 pk를 이용하여,
        invalid_pk = 123456
        valid_data = {"author": "test_comment_author", "text": "test_comment_author"}

        # When: comment_new view 를 호출하면,
        response = self.client.post(reverse("comment_new", kwargs={"pk": invalid_pk}), data=valid_data)

        # Then: status_code 가 404 NOT FOUND 가 되어야 한다.
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)