# Generated by Django 3.0.5 on 2020-05-06 07:37

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Follows',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SocialNetwork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('whatsapp_number', models.IntegerField(blank=True, db_index=True, null=True)),
                ('telegram_username', models.CharField(blank=True, db_index=True, max_length=32, null=True, validators=[django.core.validators.MinLengthValidator(5)])),
                ('personal_site', models.URLField(blank=True, db_index=True, max_length=128, null=True)),
                ('linkedin_profile', models.CharField(blank=True, db_index=True, max_length=128, null=True, validators=[django.core.validators.MinLengthValidator(5)])),
                ('github_profile', models.URLField(blank=True, db_index=True, max_length=128, null=True)),
                ('twitter_username', models.CharField(blank=True, db_index=True, max_length=32, null=True, validators=[django.core.validators.MinLengthValidator(5)])),
                ('instagram_username', models.CharField(blank=True, db_index=True, max_length=32, null=True, validators=[django.core.validators.MinLengthValidator(5)])),
                ('blog', models.URLField(blank=True, db_index=True, max_length=128, null=True)),
                ('youtube_channel', models.URLField(blank=True, db_index=True, max_length=128, null=True)),
                ('stackoverflow_profile', models.URLField(blank=True, db_index=True, max_length=128, null=True)),
                ('reddit_username', models.CharField(blank=True, db_index=True, max_length=32, null=True, validators=[django.core.validators.MinLengthValidator(5)])),
                ('facebook_profile', models.URLField(blank=True, db_index=True, max_length=128, null=True)),
                ('show_email', models.BooleanField(blank=True, db_index=True, default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', models.ImageField(default='images/logo.png', upload_to='profile_pics')),
                ('bio', models.CharField(blank=True, max_length=450, null=True)),
                ('profession', models.CharField(blank=True, max_length=200, null=True)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('following', models.ManyToManyField(blank=True, related_name='followers', through='account.Follows', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
