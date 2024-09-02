# Generated by Django 5.0.7 on 2024-08-29 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userAuths', '0013_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('vendor', 'Vendor'), ('customer', 'Customer')], default='customer', max_length=20),
        ),
    ]
