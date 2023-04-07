
import json
from io import BytesIO
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from PIL import Image

from .models import Category

class CreateCategoryTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        self.url = reverse("create_category")

    def test_create_category_success(self):
        data = {"name": "Test Category", "helpText": "This is a test category"}
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.first().name, "Test Category")
        self.assertEqual(Category.objects.first().help_text, "This is a test category")
        self.assertEqual(response.json()["status"], "success")

    def test_create_category_failure(self):
        response = self.client.post(self.url, data=json.dumps({}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Category.objects.count(), 0)
        self.assertEqual(response.json()["status"], "error")

class UploadAvatarTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        self.url = reverse("upload_avatar")

    def test_upload_avatar_success(self):
        # Create a test image file
        file = BytesIO()
        image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)

        response = self.client.post(self.url, {'name': 'avatar','avatar': file}, enctype="multipart/form-data")
        self.assertEqual(response.status_code, 302)
        # self.assertEqual(self.user.profile.avatar.url, "/media/test.png")

    def test_upload_avatar_failure(self):
        response = self.client.post(self.url, {'not_avatar': 'test'}, enctype="multipart/form-data")
        self.assertEqual(response.status_code, 400)
