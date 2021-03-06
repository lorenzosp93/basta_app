# Generated by Django 3.0.5 on 2020-04-18 23:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('participants', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Participants')),
            ],
            options={
                'verbose_name': 'Session',
                'verbose_name_plural': 'Sessions',
            },
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('letter', models.TextField(max_length=1, verbose_name='Letter')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basta.Session', verbose_name='Session')),
            ],
            options={
                'verbose_name': 'Round',
                'verbose_name_plural': 'Rounds',
                'unique_together': {('letter', 'session')},
            },
        ),
        migrations.CreateModel(
            name='Play',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15, verbose_name='Name')),
                ('surname', models.CharField(max_length=15, verbose_name='Surname')),
                ('plant', models.CharField(max_length=15, verbose_name='Flower / Fruit / Vegetable')),
                ('animal', models.CharField(max_length=15, verbose_name='Animal')),
                ('place', models.CharField(max_length=15, verbose_name='City / Country')),
                ('film', models.TextField(max_length=40, verbose_name='Movie / Series')),
                ('obj', models.CharField(max_length=15, verbose_name='Object')),
                ('brand', models.CharField(max_length=15, verbose_name='Brand')),
                ('score', models.IntegerField(default=0, editable=False)),
                ('cur_round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basta.Round')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Play',
                'verbose_name_plural': 'Plays',
            },
        ),
    ]
