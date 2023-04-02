from django.contrib import admin
from .models import Category, Prompt, Label, PromptLabel

# Register your models here.

admin.site.register([Category, Prompt, Label, PromptLabel])