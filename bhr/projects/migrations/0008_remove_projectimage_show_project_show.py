# Generated by Django 4.2.6 on 2023-11-23 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_projectimage_show_alter_projectimage_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectimage',
            name='show',
        ),
        migrations.AddField(
            model_name='project',
            name='show',
            field=models.BooleanField(default=True),
        ),
    ]