# Generated by Django 3.2.24 on 2024-02-19 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('queues', '0004_alter_queue_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='queue',
            name='type',
            field=models.CharField(choices=[('hardware', 'Hardware Issue'), ('software', 'Software Issue'), ('phone', 'Phone Issue'), ('account', 'Account Issue')], max_length=200),
        ),
    ]
