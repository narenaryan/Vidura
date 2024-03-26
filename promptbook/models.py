import hashlib

from django.db import models
from django.db.models import UniqueConstraint
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
from gettext import gettext as _

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


# 定义验证器
code_validator = RegexValidator(
    regex=r'^[a-z][a-z0-9_]*$',
    message=_('Must be start with a lowercase letter and '
              'contain only lowercase letters, numbers, and underscores.'),
)


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True, validators=[code_validator])
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    display_name = models.CharField(max_length=64)
    pinned_by = models.ManyToManyField(User, related_name='pinned_categories')  # Renamed field

    def __str__(self):
        return self.name


class Label(models.Model):
    name = models.CharField(max_length=32)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            UniqueConstraint(fields=['category', 'name',], name='label_unique_name_category')
        ]

class LLMModel(models.Model):
    name = models.CharField(max_length=64)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            UniqueConstraint(fields=['category', 'name',], name='model_unique_name_category')
        ]


class Prompt(models.Model):
    name = models.CharField(max_length=64)
    text = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    last_used_at = models.DateTimeField(auto_now=True)  # API usage tracking（Web访问不计算在内）
    text_hash = models.CharField(max_length=32, unique=True)
    labels = models.ManyToManyField(Label, related_name='prompts')
    llm_models = models.ManyToManyField(LLMModel, related_name='prompts')
    output_format = models.CharField(max_length=32, default='str', choices=[('json', 'JSON'), ('str', 'String')])


    def __str__(self):
        txt = self.text[:50] + '...' if len(self.text) > 50 else self.text
        return f"[{self.name}]: {txt}"

    # Generates hash and stores it in text_hash
    def save(self, *args, **kwargs):
        self.text_hash = hashlib.md5((self.text).encode()).hexdigest()
        super().save(*args, **kwargs)

    # Add unique together constraint for text_hash, owner and category
    class Meta:
        constraints = [
            UniqueConstraint(fields=['text_hash', 'category'], name='unique_text_hash_category'),
            UniqueConstraint(fields=['name', 'category'], name='prompt_unique_name_category')
        ]