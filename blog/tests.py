from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import *


class BlogTests(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(
				username = 'testUser',
				email = 'test@user.com',
				password = 'test'
			)
		self.post = Post.objects.create(
				title = 'test title',
				body='test body content',
				author = self.user,
			)


	def test_string_representation(self):
		post = Post(title='test string repres')
		self.assertEqual(str(post), post.title)


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







		