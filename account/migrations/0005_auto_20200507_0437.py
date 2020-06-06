# Generated by Django 3.0.5 on 2020-05-07 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20200506_0825'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='show_activity',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='show_email',
            field=models.BooleanField(db_index=True, default=False),
        ),
    ]