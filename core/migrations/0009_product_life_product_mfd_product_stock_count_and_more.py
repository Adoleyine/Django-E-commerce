# Generated by Django 5.0.7 on 2024-07-28 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_productimages_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='life',
            field=models.CharField(default='100 days', max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='mfd',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='stock_count',
            field=models.CharField(default='10', max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='type',
            field=models.CharField(default='Organic', max_length=100),
        ),
    ]
