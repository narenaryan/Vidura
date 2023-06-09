# Generated by Django 4.1.7 on 2023-04-10 01:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('promptbook', '0011_auto_20230410_0104'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='prompt',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='prompt',
            name='text_hash',
            field=models.CharField(max_length=32, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='prompt',
            unique_together={('text_hash', 'owner', 'category')},
        ),
    ]
