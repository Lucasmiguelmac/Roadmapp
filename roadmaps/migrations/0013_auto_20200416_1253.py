# Generated by Django 3.0.5 on 2020-04-16 15:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('roadmaps', '0012_auto_20200416_0746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roadmap',
            name='completed_by',
            field=models.ManyToManyField(blank=True, related_name='finished_roadmaps', to=settings.AUTH_USER_MODEL),
        ),
    ]
