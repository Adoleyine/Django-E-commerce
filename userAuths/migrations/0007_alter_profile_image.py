# Generated by Django 5.0.7 on 2024-08-24 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userAuths', '0006_remove_user_role_user_is_vendor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image'),
        ),
    ]
