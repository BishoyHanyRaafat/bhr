# Generated by Django 4.2.6 on 2023-10-21 18:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('discounts', '0003_rename_username_point_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='point',
            name='expire_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='voucher',
            name='expire_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
