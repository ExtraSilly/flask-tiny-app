# Generated by Django 5.1.5 on 2025-02-26 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_orderitem_order_remove_shippingaddress_order_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='is_blocked',
            field=models.BooleanField(default=False),
        ),
    ]
