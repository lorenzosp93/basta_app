from django.db import migrations, transaction, IntegrityError
from django.utils.translation import gettext_lazy as _

CATEGORIES = (
    ('elements', _('Chemical element')),
    ('petnames', _('Pet name')),
    ('transportation', _('Means of transportation')),
    ('furniture', _('Furniture')),
    ('disease', _('Disease / Illness')),
    ('genres', _('Musical genre')),
    ('villains', _('Villain')),
    ('excuses', _('Excuses not to go to a party')),
    ('reasonsquitjob',_('Reasons to quit your job')),
    ('doatdate', _('Things to do on a date')),
    ('hobbies', _('Hobby / Activity')),
    ('uniforms', _('People in uniform')),
    ('literary', _('Work of literature'))
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
        ('basta', '0017_auto_20200503_2155')
    ]
    operations = [
        migrations.RunPython(
            initialize_categories,
            uninitialize_categories
        ),
    ]