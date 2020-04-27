# Generated by Django 3.0.5 on 2020-04-26 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basta', '0012_auto_20200426_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('name', 'Name'), ('surname', 'Surname'), ('plant', 'Flower / Fruit / Vegetable'), ('animal', 'Animal'), ('location', 'City / Country'), ('film', 'Movie / Series'), ('object', 'Object'), ('brand', 'Brand'), ('band', 'Musician / Band'), ('color', 'Color'), ('profession', 'Profession'), ('sport', 'Sport'), ('historical', 'Historical figure'), ('art', 'Monument / Art piece'), ('gifts', 'Gift / Present'), ('bad_habits', 'Bad habit'), ('reasons911', 'Reason to call 911'), ('food', 'Food'), ('athletes', 'Athlete'), ('fictional', 'Fictional character'), ('instruments', 'Instrument / Tool'), ('halloween', 'Halloween costume'), ('bodyparts', 'Body part')], max_length=15, unique=True, verbose_name='Category name'),
        ),
    ]