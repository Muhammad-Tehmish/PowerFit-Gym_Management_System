# Generated by Django 3.2.19 on 2023-06-30 21:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='members',
            old_name='Email',
            new_name='EMAIL',
        ),
        migrations.RenameField(
            model_name='members',
            old_name='Name',
            new_name='NAME',
        ),
        migrations.RenameField(
            model_name='members',
            old_name='Password',
            new_name='PASSWORD',
        ),
    ]