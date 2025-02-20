# Generated by Django 5.1.2 on 2025-02-20 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='account',
            fields=[
                ('email', models.EmailField(max_length=254, unique=True)),
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'account',
            },
        ),
    ]
