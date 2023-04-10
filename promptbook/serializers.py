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
    category = CategorySerializer()
    labels = LabelSerializer(many=True)

    class Meta:
        model = Prompt
        fields = ('id', 'text', 'category', 'created_at',
                  'modified_at', 'owner', 'is_public', 'labels')

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        labels_data = validated_data.pop('labels')
        category = Category.objects.create(**category_data)
        prompt = Prompt.objects.create(category=category, **validated_data)
        for label_data in labels_data:
            try:
                label = Label.objects.get(**label_data)
                prompt.labels.add(label)
            except Label.DoesNotExist:
                # Ignore if label does not exist, do not add it to the prompt
                pass
        return prompt
