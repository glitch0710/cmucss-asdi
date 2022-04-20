# Generated by Django 4.0.3 on 2022-04-20 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cssurvey', '0009_ticket'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneratedLinks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(blank=True, max_length=255, null=True)),
                ('generated_link', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'generated_links',
                'managed': False,
            },
        ),
    ]
