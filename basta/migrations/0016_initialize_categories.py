from django.db import migrations, transaction, IntegrityError
from django.utils.translation import gettext_lazy as _

CATEGORIES = (
    ('suicide', _('Dumb ways to die')),
    ('clothing', _('Cloting items')),
    ('drinks', _('Drink')),
    ('black', _('Thing that is black')),
    ('rivers', _('River')),
    ('boardgames', _('Board game')),
    ('author', _('Author')),
    ('song', _('Song')),
)

DEFAULTS = [
    'name', 'surname','plant', 'animal',
    'location', 'film', 'object', 'brand'
]

def initialize_categories(apps, schema_editor):
    Category = apps.get_model('basta', 'Category')
    for category in CATEGORIES:
        try:
            with transaction.atomic():
                Category.objects.create(
                    name = category[0],
                    default = category[0] in DEFAULTS
                )
        except IntegrityError:
            pass
        
        
def uninitialize_categories(apps, schema_editor):
    Category = apps.get_model('basta', 'Category')
    for category in CATEGORIES:
        try:
            with transaction.atomic():
                Category.objects.get(
                    name = category[0],
                ).delete()
        except IntegrityError:
            pass


class Migration(migrations.Migration):
    dependencies = [
        ('basta', '0015_auto_20200427_1450')
    ]
    operations = [
        migrations.RunPython(
            initialize_categories,
            uninitialize_categories
        ),
    ]