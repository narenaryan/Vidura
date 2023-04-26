from django.contrib import admin
from .models import Category, Prompt, Label, PromptLabel, Profile
from reversion.admin import VersionAdmin

# Register your models here.



class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'modified_at', 'help_text')
    search_fields = ('name',)
    list_filter = ('created_at', 'modified_at')


class PromptAdmin(admin.ModelAdmin):
    list_display = ('text', 'category', 'created_at', 'modified_at', 'owner', 'is_public', 'text_hash')
    search_fields = ('text', 'owner__username')
    list_filter = ('category', 'created_at', 'modified_at', 'owner', 'is_public')


class LabelAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'modified_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'modified_at')


class PromptLabelAdmin(admin.ModelAdmin):
    list_display = ('label', 'prompt')
    search_fields = ('label__name', 'prompt__text')
    list_filter = ('label', 'prompt')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Prompt, PromptAdmin)
admin.site.register(Label, LabelAdmin)
admin.site.register(PromptLabel, PromptLabelAdmin)