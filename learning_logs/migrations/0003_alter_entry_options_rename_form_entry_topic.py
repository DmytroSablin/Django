# Generated by Django 4.1 on 2022-08-21 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learning_logs', '0002_alter_topic_date_added_entry'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entry',
            options={'verbose_name_plural': 'entries'},
        ),
        migrations.RenameField(
            model_name='entry',
            old_name='form',
            new_name='topic',
        ),
    ]