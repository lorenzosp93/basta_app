# Generated by Django 3.0.5 on 2020-04-19 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basta', '0002_auto_20200419_1135'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='participants',
        ),
        migrations.AddField(
            model_name='round',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Is round active?'),
        ),
        migrations.AddField(
            model_name='round',
            name='number',
            field=models.PositiveIntegerField(default=0, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='session',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Is session active?'),
        ),
        migrations.AddField(
            model_name='session',
            name='name',
            field=models.TextField(blank=True, max_length=30, verbose_name='Session name'),
        ),
        migrations.AlterField(
            model_name='play',
            name='score',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='round',
            name='letter',
            field=models.TextField(editable=False, max_length=1, verbose_name='Letter'),
        ),
    ]
