# Generated by Django 4.1.7 on 2024-02-19 09:17
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import now


def generate_prompt_name(apps, schema_editor):
    Prompt = apps.get_model('promptbook', 'Prompt')
    for prompt in Prompt.objects.all():
        prompt.name = prompt.text[:8]  # 取text字段的前8位作为name
        prompt.save(update_fields=['name'])


def create_default_llmmodel_and_assign_to_prompts(apps, schema_editor):
    Category = apps.get_model('promptbook', 'Category')
    LLMModel = apps.get_model('promptbook', 'LLMModel')
    Prompt = apps.get_model('promptbook', 'Prompt')

    # 创建默认的LLMModel实例
    try:
        default_category = Category.objects.get(id=1)
    except Category.DoesNotExist:
        return

    llmmodel, created = LLMModel.objects.get_or_create(
        name='all',
        defaults={'category': default_category}
    )

    # 将所有Prompt的 llm_models 设置为这个LLMModel实例
    for prompt in Prompt.objects.all():
        prompt.llm_models.add(llmmodel)


class Migration(migrations.Migration):
    dependencies = [
        ("promptbook", "0017_alter_label_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="prompt",
            name="name",
            field=models.CharField(
                default='',  # 设置一个临时默认值
                max_length=64,
            ),
            preserve_default=False,
        ),

        migrations.RunPython(
            generate_prompt_name,
            reverse_code=migrations.RunPython.noop
        ),
        migrations.AlterField(
            model_name="prompt",
            name="name",
            field=models.CharField(
                max_length=64,
                unique=True
            ),
        ),

        migrations.CreateModel(
            name="LLMModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="promptbook.category",
                    ),
                ),
            ],
        ),

        migrations.AddField(
            model_name="prompt",
            name="llm_models",
            field=models.ManyToManyField(
                related_name="prompts", to="promptbook.llmmodel"
            ),
        ),
        migrations.RunPython(
            create_default_llmmodel_and_assign_to_prompts,
            reverse_code=migrations.RunPython.noop
        ),
    ]
