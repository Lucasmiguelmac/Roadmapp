# Generated by Django 3.0.5 on 2020-05-04 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20200504_0352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='social_networks',
            field=models.ManyToManyField(blank=True, related_name='social_networks', to='account.SocialNetwork'),
        ),
    ]
