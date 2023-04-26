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
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    help_text = models.CharField(max_length=255)
    pinned_by = models.ManyToManyField(User, related_name='pinned_categories')  # Renamed field


    def __str__(self):
        return self.name


class Prompt(models.Model):
    text = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)
    text_hash = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.text[:50] + '...' if len(self.text) > 50 else self.text

    # Generates hash and stores it in text_hash
    def save(self, *args, **kwargs):
        self.text_hash = hashlib.md5((self.text + self.owner.username).encode()).hexdigest()
        super().save(*args, **kwargs)

    # Add unique together constraint for text_hash, owner and category
    class Meta:
        unique_together = ['text_hash', 'owner', 'category']


class Label(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class PromptLabel(models.Model):
    label = models.ForeignKey(Label, on_delete=models.DO_NOTHING)
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE)

    def __str__(self):
        return f"Label: {self.label.__str__()}, Prompt: {self.prompt.__str__()}"
