# Generated by Django 4.2.6 on 2023-10-21 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discounts', '0002_alter_point_create_date_alter_point_expire_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='point',
            old_name='username',
            new_name='user',
        ),
    ]
