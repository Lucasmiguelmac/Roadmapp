# Generated by Django 3.0.5 on 2020-04-15 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roadmaps', '0005_auto_20200415_0647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roadmap',
            name='objectives',
            field=models.CharField(default='', max_length=1200),
        ),
    ]
