# Generated by Django 3.0.5 on 2020-04-16 10:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('roadmaps', '0010_auto_20200415_1503'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roadmap',
            name='members',
        ),
        migrations.RemoveField(
            model_name='unit',
            name='place',
        ),
        migrations.AddField(
            model_name='item',
            name='completed_by',
            field=models.ManyToManyField(related_name='finished_items', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='roadmap',
            name='completed_by',
            field=models.ManyToManyField(related_name='finished_roadmaps', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='unit',
            name='completed_by',
            field=models.ManyToManyField(related_name='finished_units', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Membership',
        ),
    ]
