# Generated by Django 2.1.1 on 2018-10-16 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolists', '0002_item_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
