from rest_framework import serializers
from .models import Prompt, Category, Label

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'help_text']


class PromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = ['text']

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'name']
