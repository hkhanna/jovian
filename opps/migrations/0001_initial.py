# Generated by Django 3.2.10 on 2022-01-29 00:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('email', models.EmailField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(blank=True, max_length=255)),
                ('last_name', models.CharField(blank=True, max_length=255)),
                ('email', models.EmailField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='opps.organization')),
            ],
        ),
        migrations.CreateModel(
            name='InterestedIn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interested_in', to='opps.user')),
            ],
        ),
    ]
