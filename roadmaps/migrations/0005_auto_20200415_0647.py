# Generated by Django 3.0.5 on 2020-04-15 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roadmaps', '0004_auto_20200414_0342'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roadmap',
            name='about',
        ),
        migrations.AddField(
            model_name='roadmap',
            name='estimated_time',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='roadmap',
            name='methods_and_resources',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AddField(
            model_name='roadmap',
            name='objectives',
            field=models.CharField(default='', max_length=500),
        ),
    ]
