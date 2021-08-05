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

    def test_post_list_should_return_200_ok_and_list_length_should_30(self):
        # Given: 30개의 새로운 post 생성하고,
        for _ in range(30):
            post = self._create_new_post(
                title="test_post_list_title", text="test_post_list_text"
            )

        # When: post_list view 를 호출하면,
        response = self.client.get(reverse("post_list"))

        # Then: status_code 가 200이 되어야 한다.
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # And: 생성된 post 의 개수가 30개로 일치해야 한다.
        post_list = json.loads(response.json()["post_data"])
        self.assertEqual(len(post_list), 30)

    def test_post_detail_should_return_200_ok_when_use_vaild_pk_and_post_and_response_contents_should_be_same(self):
        # Given: 1개의 post 를 생성하고,
        post = self._create_new_post(
            title="test_post_detail_title", text="test_post_detail_text"
        )

        # When: post_detail view 를 호출하면,
        response = self.client.get(reverse("post_detail", kwargs={"pk": post.pk}))

        # Then: 리턴된 status_code 가 200이 되어야 한다.
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # And: post 와 response 로 받은 contents 가 같아야 한다.
        post_data = json.loads(response.json()["post_data"])
        self.assertEqual(post_data["title"], post.title)
        self.assertEqual(post_data["text"], post.text)

    def test_post_detail_should_return_404_not_found_when_use_invail_pk(self):
        # Given: invalid 한 pk 값을 정하고,
        invalid_pk = 123456

        # When: 그 값으로 post_detail view 를 호출하면,
        response = self.client.get(reverse("post_detail", kwargs={"pk": invalid_pk}))

        # Then: 리턴된 status_code 가 404이 되어야 한다.
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_post_update_should_return_200_ok(self):
        # Given: post 1개를 생성하고,
        post = self._create_new_post(title="update_test", text="update_text")

        # And: 사용자가 수정을 요구한 데이터를 설정한다음
        put_data = {"title": "updated test title", "text": "updated test text"}

        # When: post_update view 를 호출하면,
        response = self.client.put(reverse("post_edit", kwargs={"pk": post.pk}), data=put_data)

        # Then: status_code 가 200으로 리턴되어야 한다
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