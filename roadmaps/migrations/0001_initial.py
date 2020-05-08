# Generated by Django 3.0.5 on 2020-05-06 07:37

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
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Title', max_length=50, validators=[django.core.validators.MinLengthValidator(2, 'Title must be greater than 2 characters')])),
                ('place', models.IntegerField(default=1)),
                ('objectives', models.CharField(default='', max_length=1200)),
                ('link', models.URLField(blank=True, db_index=True, max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Roadmap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.IntegerField(blank=True, null=True)),
                ('title', models.CharField(default='Title', max_length=50, validators=[django.core.validators.MinLengthValidator(2, 'Title must be greater than 2 characters')])),
                ('image', models.ImageField(blank=True, null=True, upload_to='roadmap_images')),
                ('objectives', models.CharField(default='', max_length=1200)),
                ('methods_and_resources', models.CharField(default='', max_length=250)),
                ('estimated_time', models.CharField(default='', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('privacy', models.CharField(choices=[('PR', 'Private'), ('HI', 'Hidden'), ('PU', 'Public')], default='PU', max_length=2)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('parent_roadmap', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children_roadmaps', to='roadmaps.Roadmap')),
            ],
        ),
        migrations.CreateModel(
            name='RoadmapMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finished', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('roadmap', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roadmaps.Roadmap')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Title', max_length=30, validators=[django.core.validators.MinLengthValidator(2, 'Title must be greater than 2 characters')])),
                ('image', models.ImageField(upload_to='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Title', max_length=50, validators=[django.core.validators.MinLengthValidator(2, 'Title must be greater than 2 characters')])),
                ('place', models.IntegerField(default=1)),
                ('objectives', models.CharField(default='', max_length=1200)),
                ('roadmap', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='units', to='roadmaps.Roadmap')),
            ],
        ),
        migrations.CreateModel(
            name='UnitMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finished', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('roadmap_membership', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roadmaps.RoadmapMembership')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roadmaps.Unit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='unit',
            name='unit_members',
            field=models.ManyToManyField(related_name='units', through='roadmaps.UnitMembership', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='RoadmapTagRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('roadmap', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roadmaps.Roadmap')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roadmaps.Tag')),
            ],
        ),
        migrations.AddField(
            model_name='roadmap',
            name='roadmap_members',
            field=models.ManyToManyField(related_name='roadmaps', through='roadmaps.RoadmapMembership', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='roadmap',
            name='tags',
            field=models.ManyToManyField(through='roadmaps.RoadmapTagRelationship', to='roadmaps.Tag'),
        ),
        migrations.AddField(
            model_name='roadmap',
            name='topics',
            field=models.ManyToManyField(related_name='roadmaps', to='roadmaps.Topic'),
        ),
        migrations.CreateModel(
            name='ItemMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finished', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roadmaps.Item')),
                ('parent_item_membership', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children_item_memberships', to='roadmaps.ItemMembership')),
                ('unit_membership', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roadmaps.UnitMembership')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='item_members',
            field=models.ManyToManyField(related_name='items', through='roadmaps.ItemMembership', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='item',
            name='parent_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children_items', to='roadmaps.Item'),
        ),
        migrations.AddField(
            model_name='item',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roadmaps.Unit'),
        ),
    ]
