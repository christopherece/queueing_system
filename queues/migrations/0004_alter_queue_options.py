# Generated by Django 4.2.1 on 2023-05-16 21:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('queues', '0003_alter_queue_status_alter_queue_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='queue',
            options={'ordering': ('queue_id',)},
        ),
    ]
