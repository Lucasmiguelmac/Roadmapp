# Generated by Django 3.0.5 on 2020-04-12 19:52

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Roadmap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(2, 'Title must be greater than 2 characters')])),
                ('image', models.ImageField(upload_to='')),
                ('about', models.TextField()),
                ('members', models.ManyToManyField(related_name='roadmaps', through='roadmaps.Membership', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(2, 'Title must be greater than 2 characters')])),
                ('about', models.TextField()),
                ('roadmap', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roadmaps.Roadmap')),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(2, 'Title must be greater tahn 2 characters')])),
                ('image', models.ImageField(upload_to='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('roadmaps', models.ManyToManyField(to='roadmaps.Roadmap')),
            ],
        ),
        migrations.AddField(
            model_name='membership',
            name='roadmap',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roadmaps.Roadmap'),
        ),
        migrations.AddField(
            model_name='membership',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(2, 'Title must be greater than 2 characters')])),
                ('about', models.TextField()),
                ('link', models.TextField()),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roadmaps.Unit')),
            ],
        ),
    ]
