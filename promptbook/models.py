import hashlib

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import reversion


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to='avatars/', default=None, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    help_text = models.CharField(max_length=255, blank=True, null=True)
    pinned_by = models.ManyToManyField(User, related_name='pinned_categories')  # Renamed field

    def __str__(self):
        return self.name


class Label(models.Model):
    name = models.CharField(max_length=32, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class LLMModel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Prompt(models.Model):
    name = models.CharField(max_length=64, unique=True)
    text = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    text_hash = models.CharField(max_length=32, unique=True)
    labels = models.ManyToManyField(Label, related_name='prompts')
    llm_models = models.ManyToManyField(LLMModel, related_name='prompts')


    def __str__(self):
        txt = self.text[:50] + '...' if len(self.text) > 50 else self.text
        return f"[{self.name}]: {txt}"

    # Generates hash and stores it in text_hash
    def save(self, *args, **kwargs):
        self.text_hash = hashlib.md5((self.text).encode()).hexdigest()
        super().save(*args, **kwargs)

    # Add unique together constraint for text_hash, owner and category
    class Meta:
        unique_together = ['text_hash', 'category']
