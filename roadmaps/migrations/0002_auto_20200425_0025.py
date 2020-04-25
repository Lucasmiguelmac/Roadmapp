# Generated by Django 3.0.5 on 2020-04-25 03:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roadmaps', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemmembership',
            name='parent_item_membership',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children_item_memberships', to='roadmaps.ItemMembership'),
        ),
    ]
