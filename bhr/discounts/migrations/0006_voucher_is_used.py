# Generated by Django 4.2.6 on 2023-10-22 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discounts', '0005_alter_point_expire_date_alter_voucher_expire_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='voucher',
            name='is_used',
            field=models.BooleanField(default=False),
        ),
    ]
