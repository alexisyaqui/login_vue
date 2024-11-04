# Generated by Django 5.1.1 on 2024-10-21 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='roles',
            field=models.CharField(choices=[('admin', 'Admin'), ('editor', 'Editor'), ('vista', 'Vista')], default=1, max_length=10),
            preserve_default=False,
        ),
    ]