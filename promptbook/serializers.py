from rest_framework import serializers
from .models import Prompt, Category, Label


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = '__all__'


class PromptSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all())
    labels = serializers.PrimaryKeyRelatedField(
        queryset=Label.objects.all(), many=True)
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Prompt
        fields = ('id', 'text', 'category', 'created_at',
                  'modified_at', 'owner', 'is_public', 'labels')

    def create(self, validated_data):
        labels_data = validated_data.pop('labels')
        prompt = Prompt.objects.create(**validated_data)
        prompt.labels.set(labels_data)
        return prompt
