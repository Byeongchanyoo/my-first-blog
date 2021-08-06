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
        return comment

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

    def test_comment_update_should_return_200_ok_when_post_and_comment_are_valid_and_data_and_comment_content_should_be_same(self):
        # Given: valid 한 post 와 comment pk 가 주어지고,
        target_post = self._create_new_post(title="update_test_title", text="update_test_text")
        non_target_post = self._create_new_post(title="second_test_title", text="second_test_text")
        test_comment = self._create_new_comment(post=target_post, author="update_test_author", text="update_test_text")
        for i in range(2):
            self._create_new_comment(post=target_post, author="target_post_comment_author", text="target_post_comment_text")
        self._create_new_comment(post=non_target_post, author="non_target_post_comment_author", text="non_target_post_comment_text")
        valid_update_data = {"author": "fixed_author", "text": "fixed text"}

        # When: comment_update view 를 호출하면,
        response = self.client.put(reverse("comment_edit", kwargs={"pk": target_post.pk, "id": test_comment.id}), data=valid_update_data)

        # Then: status_code 가 200 OK 가 되어야 한다.
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # And: comment 의 내용이 valid_update_data 와 일치해야 한다.
        comment_data = Comment.objects.get(id=test_comment.id)
        self.assertEqual(comment_data.author, valid_update_data["author"])
        self.assertEqual(comment_data.text, valid_update_data["text"])
