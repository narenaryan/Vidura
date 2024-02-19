from rest_framework import serializers
from .models import Prompt, Category, Label, LLMModel


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'help_text']


class PromptSerializer(serializers.ModelSerializer):
    llm_models = serializers.SerializerMethodField()
    labels = serializers.SerializerMethodField()

    class Meta:
        model = Prompt
        fields = ['name', 'text', 'labels', 'llm_models']

    def get_labels(self, obj):
        """
        返回包含id和name的labels列表
        """
        return LabelSerializer(obj.labels.all(), many=True).data

    def get_llm_models(self, obj):
        """
        返回包含id和name的llm_models列表
        """
        return LLMModelSerializer(obj.llm_models.all(), many=True).data


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'name']


class LLMModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LLMModel
        fields = ['id', 'name']
