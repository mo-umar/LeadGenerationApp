# Generated by Django 5.1.2 on 2024-10-28 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserQuery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_market', models.CharField(max_length=255)),
                ('desired_role', models.CharField(max_length=255)),
                ('specific_criteria', models.TextField()),
            ],
        ),
    ]
