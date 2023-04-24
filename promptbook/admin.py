from django.contrib import admin
from .models import Category, Prompt, Label, PromptLabel
from reversion.admin import VersionAdmin

# Register your models here.
@admin.register(Category)
class YourModelAdmin(VersionAdmin):
    pass

admin.site.register([Prompt, Label, PromptLabel])