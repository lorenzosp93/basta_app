from django.db import migrations, transaction, IntegrityError
from django.utils.translation import gettext_lazy as _

CATEGORIES = (
    ('name', _("Name")),
    ('surname', _("Surname")),
    ('plant', _("Flower / Fruit / Vegetable")),
    ('animal', _("Animal")),
    ('location', _("City / Country")),
    ('film', _("Movie / Series")),
    ('object', _("Object")),
    ('brand', _("Brand")),
    ('band', _("Musician / Band")),
    ('color', _("Color")),
    ('profession', _("Profession")),
    ('sport', _("Sport")),
    ('historical', _("Historical figure")),
    ('art', _("Monument / Art piece")),
    ('gifts', _("Gift / Present")),
    ('bad_habits', _("Bad habit")),
    ('reasons911', _("Reason to call 911")),
    ('food', _("Food")),
    ('athletes', _("Athlete")),
    ('fictional', _("Fictional character")),
    ('instruments', _("Instrument / Tool")),
    ('halloween', _("Halloween costume")),
    ('bodyparts', _("Body part")),
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
        ('basta', '0013_auto_20200426_1944')
    ]
    operations = [
        migrations.RunPython(
            initialize_categories,
            uninitialize_categories
        ),
    ]