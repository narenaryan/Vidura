from rest_framework import serializers
from .models import Prompt, Category, Label, LLMModel


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'help_text']


class PromptSerializer(serializers.ModelSerializer):
    models = serializers.SerializerMethodField()
    labels = serializers.SerializerMethodField()

    # 用于反序列化（接收数据）的字段
    model_names = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)
    label_names = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)

    class Meta:
        model = Prompt
        fields = ['name', 'text', 'labels', 'models', 'label_names', 'model_names']

    def get_labels(self, obj):
        """
        返回包含id和name的labels列表
        """
        return LabelSerializer(obj.labels.all(), many=True).data

    def get_models(self, obj):
        """
        返回包含id和name的llm_models列表
        """
        return LLMModelSerializer(obj.llm_models.all(), many=True).data

    def create(self, validated_data):
        print('create', validated_data)
        model_names = validated_data.pop('model_names', [])
        label_names = validated_data.pop('label_names', [])

        # 创建Prompt实例
        prompt = Prompt.objects.create(**validated_data)

        # 处理模型和标签的关联
        for model_name in model_names:
            model, _ = LLMModel.objects.get_or_create(name=model_name, category=prompt.category)
            prompt.llm_models.add(model)

        for label_name in label_names:
            label, _ = Label.objects.get_or_create(name=label_name, category=prompt.category)
            prompt.labels.add(label)

        return prompt


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'name']


class LLMModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LLMModel
        fields = ['id', 'name']
