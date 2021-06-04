from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import *


class BlogTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testUser',
            email='test@user.com',
            password='test'
        )
        self.post = Post.objects.create(
            title='test title',
            body='test body content',
            author=self.user,
        )

    # Model Tests

    def test_string_representation(self):
        post = Post(title='test string repres')
        self.assertEqual(str(post), post.title)

    def test_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), '/post/1/')

    # Views test

    def test_post_content(self):
        self.assertEqual(f"{self.post.title}", "test title")
        self.assertEqual(f"{self.post.body}", "test body content")
        self.assertEqual(f"{self.post.author}", "testUser")

    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test body content')
        self.assertTemplateUsed(response, 'home.html')

    def test_post_detail_view(self):
        response = self.client.get('/post/1/')
        no_response = self.client.get('/post/100000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'test title')
        self.assertTemplateUsed(response, 'post_detail.html')

    def test_post_create_view(self):
        response = self.client.post(reverse('post_new'), {
            'title': 'New title',
            'body': 'New text',
            'author': self.user,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New title')
        self.assertContains(response, 'New text')
        self.assertTemplateUsed(response, 'post_new.html')

    def test_post_update_view(self):
        response = self.client.get(reverse('post_update', args='1'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test title')
        self.assertContains(response, 'test body content')
        self.assertTemplateUsed(response, 'post_update.html')

        response_post = self.client.post(reverse('post_update', args='1'), {
            'title': 'Updated title',
            'body': 'Updated text',
        })
        self.assertEqual(response_post.status_code, 302)

    def test_post_delete_view(self):
        response = self.client.post(
            reverse('post_delete', args='1'))
        self.assertEqual(response.status_code, 302)
