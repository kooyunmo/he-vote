# Generated by Django 4.0.5 on 2022-06-09 08:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BFVCandidateBallot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('washington', models.BinaryField()),
                ('adams', models.BinaryField()),
                ('jefferson', models.BinaryField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PaillierCandidateBallot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('washington', models.BigIntegerField()),
                ('adams', models.BigIntegerField()),
                ('jefferson', models.BigIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RenameModel(
            old_name='CandidateBallot',
            new_name='ASHECandidateBallot',
        ),
    ]