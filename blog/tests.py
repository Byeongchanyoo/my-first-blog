from django.test import TestCase
from .models import Post, Comment
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from http import HTTPStatus
import json


class TestPost(TestCase):
    def _create_new_post(self, title, text):
        return Post.objects.create(
            title=title, text=text, published_date=timezone.now()
        )
    def _create_new_comment(self, post, author, text):
        return Comment.objects.create(
            post=post, author=author, text=text
        )

    def test_post_update_should_return_200_ok(self):
        # Given: post 1개를 생성하고,
        post = self._create_new_post(title="update_test", text="update_text")
        # And: 사용자가 수정을 요구한 데이터를 설정한다음
        put_data = {"title": "updated test title", "text": "updated test text"}

        # When: post_update view 를 호출하면,
        response = self.client.put(reverse("post_edit", kwargs={"post_id": post.pk}), data=put_data)

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
        response = self.client.put(reverse("post_edit", kwargs={"post_id": invalid_pk}), data=put_data)

        # Then: status_code가 404로 되어야 한다.
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_post_update_should_return_400_bad_request(self):
        # Given: post 1개를 생성하고,
        post = self._create_new_post(title="update_test", text="update_text")
        # And: 사용자가 수정을 요구한 데이터를 설정한다음
        put_data = {"title": "updated test title"}

        # When : post update 요청
        response = self.client.put(reverse("post_edit", kwargs={"post_id": post.pk}), data=put_data)

        # Then : Bad_Request 반환하는지 확인
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_comment_delete_should_return_204_no_content_and_the_number_of_comments_should_reduce(self):
        # Given: post 와 comment 를 2개 생성하고, 그 pk와 id 를 이용하여
        post = self._create_new_post(title="delete_test_title", text="delete_test_text")
        delete_comment = self._create_new_comment(post=post, author="will_delete_author", text="will_delete_text")
        remain_comment = self._create_new_comment(post=post, author="remain_author", text="remain_author")

        # When: comment delete view 를 호출하면,
        response = self.client.delete(reverse("comment_delete", kwargs={"post_id": post.pk, "comment_id": delete_comment.id}))

        # Then: status_code 가 204 NO_CONTENT 가 되어야 한다.
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

        # And: post 가 가지고 있는 comment 의 개수가 1개가 되어야 한다.
        self.assertEqual(len(post.comments.values()), 1)

    def test_comment_delete_should_return_404_not_found_when_use_invalid_pk(self):
        # Given: invalid 한 pk 가 주어지고
        post = self._create_new_post(title="delete_test_title", text="delete_test_text")
        comment = self._create_new_comment(post=post, author="delete_test_author", text="delete_test_text")
        invalid_pk = 123456

        # When: comment delete view 를 호출하면,
        response = self.client.delete(reverse("comment_delete", kwargs={"post_id": invalid_pk, "comment_id": comment.id}))

        # Then: status_code 가 404 NOT_FOUND 가 되어야 한다.
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)