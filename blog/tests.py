from django.test import TestCase
from .models import Post, Comment
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

    def test_post_new_should_return_201_created_and_created_post_instance_and_test_data_should_be_same(self):
        # Given: 사용자가 적합한 data 를 넣어주고
        valid_data = {"title": "post_new_test_title", "text": "post_new_test_text"}

        # When: post_new view 를 호출하면,
        response = self.client.post(reverse("post_new"), data=valid_data)

        # Then: 리턴된 status_code 가 201 이어야 한다.
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

        # And: 생성된 post 가 valid_data 와 contents 가 같아야 한다
        created_post = Post.objects.get(id=response.json()["id"])
        self.assertEqual(created_post.title, valid_data["title"])
        self.assertEqual(created_post.text, valid_data["text"])

    def test_post_new_should_return_400_bad_request_when_post_invalid_data(self):
        # Given: 사용자가 적합하지 않은 data 를 넣어주고
        invalid_data = {"title": "invalid_data_no_text_data"}

        # When: post_new view 를 호출하면,
        response = self.client.post(reverse("post_new"), data=invalid_data)

        # Then: 리턴된 status_code 가 400 이어야 한다.
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_post_update_should_return_200_ok(self):
        # Given: post 1개를 생성하고,
        post = self._create_new_post(title="update_test", text="update_text")
        # And: 사용자가 수정을 요구한 데이터를 설정한다음
        put_data = {"title": "updated test title", "text": "updated test text"}

        # When: post_update view 를 호출하면,
        response = self.client.put(reverse("post_edit", kwargs={"pk": post.pk}), data=put_data)

        # Then: status_code 가 200으로 리턴되어야 한다
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # And: post 의 title 이 "updated test title" 이어야 한다.
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

        # Then: status_code 가 404로 되어야 한다.
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