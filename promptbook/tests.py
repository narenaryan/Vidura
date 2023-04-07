
import json
from io import BytesIO
from PIL import Image

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Category, Prompt, PromptLabel, Label

from .models import Category

class ListCategoriesViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.category1 = Category.objects.create(
            name='Test Category 1',
            help_text='This is a test category'
        )
        self.category2 = Category.objects.create(
            name='Test Category 2',
            help_text='This is another test category'
        )

    def test_list_categories_authenticated_user(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('list_categories'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Category 1')
        self.assertContains(response, 'Test Category 2')

    def test_list_categories_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(reverse('list_categories'))
        self.assertEqual(response.status_code, 302)

class CreateCategoryViewTestCase(TestCase):
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

class UploadAvatarViewTestCase(TestCase):
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

    def test_upload_avatar_failure(self):
        response = self.client.post(self.url, {'not_avatar': 'test'}, enctype="multipart/form-data")
        self.assertEqual(response.status_code, 400)

class SearchViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.category = Category.objects.create(
            name='Test Category',
            help_text='This is a test category'
        )
        self.prompt = Prompt.objects.create(
            text='This is a test prompt',
            category=self.category,
            owner=self.user,
            is_public=True
        )
        self.client.login(username="testuser", password="testpass")

    # No categories or prompts matches
    def test_search_no_results(self):
        response = self.client.get(reverse('search'), {'q': 'nonexistent'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No categories found.")
        self.assertContains(response, "No prompts found.")

    # A category and prompt matches
    def test_search_categories(self):
        response = self.client.get(reverse('search'), {'q': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Category')
        self.assertContains(response, 'This is a test prompt')

    # Only a prompt matches
    def test_search_prompts(self):
        response = self.client.get(reverse('search'), {'q': 'prompt'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is a test prompt')
        self.assertContains(response, "No categories found.")

    # Test unauthenticated user
    def test_search_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(reverse('search'), {'q': 'test'})
        self.assertEqual(response.status_code, 302)

class ListPromptsViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='testuser1',
            password='testpass1'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='testpass2'
        )
        self.category = Category.objects.create(
            name='Test Category',
            help_text='This is a test category'
        )
        self.label = Label.objects.create(
            name='Test Label'
        )
        self.prompt1 = Prompt.objects.create(
            text='This is a test prompt',
            category=self.category,
            owner=self.user1,
            is_public=True
        )
        self.prompt2 = Prompt.objects.create(
            text='This is another test prompt',
            category=self.category,
            owner=self.user2,
            is_public=False
        )
        self.prompt_label = PromptLabel.objects.create(
            prompt=self.prompt1,
            label=self.label
        )

    def test_list_prompts_authenticated_user(self):
        self.client.login(username='testuser1', password='testpass1')
        url = reverse('list_prompts', args=[self.category.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is a test prompt')
        self.assertNotContains(response, 'This is another test prompt')
        self.assertContains(response, 'Test Label')

    def test_list_prompts_unauthenticated_user(self):
        self.client.logout()
        url = reverse('list_prompts', args=[self.category.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

class ListPromptsByLabelViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.category = Category.objects.create(
            name='Test Category',
            help_text='This is a test category'
        )
        self.label1 = Label.objects.create(
            name='Test Label 1'
        )
        self.label2 = Label.objects.create(
            name='Test Label 2'
        )
        self.prompt1 = Prompt.objects.create(
            text='This is a test prompt',
            category=self.category,
            owner=self.user,
            is_public=True
        )
        self.prompt2 = Prompt.objects.create(
            text='This is another test prompt',
            category=self.category,
            owner=self.user,
            is_public=True
        )
        self.prompt_label1 = PromptLabel.objects.create(
            prompt=self.prompt1,
            label=self.label1
        )
        self.prompt_label2 = PromptLabel.objects.create(
            prompt=self.prompt2,
            label=self.label2
        )

    def test_list_prompts_by_label_authenticated_user(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('list_prompts_by_label', args=[self.label1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is a test prompt')
        self.assertNotContains(response, 'This is another test prompt')
        self.assertContains(response, 'Test Label 1')
        self.assertNotContains(response, 'Test Label 2')

    def test_list_prompts_by_label_unauthenticated_user(self):
        self.client.logout()
        url = reverse('list_prompts_by_label', args=[self.label1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_list_prompts_by_label_invalid_label_id(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('list_prompts_by_label', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
