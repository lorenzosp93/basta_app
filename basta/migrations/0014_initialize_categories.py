from django.db import migrations, transaction, IntegrityError
from ..models import (
    CATEGORIES,
    DEFAULTS
)


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