# Generated by Django 4.1.7 on 2023-03-20 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_variation_managers'),
        ('cart', '0002_cart_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart_item',
            name='variations',
            field=models.ManyToManyField(blank=True, to='store.variation'),
        ),
    ]