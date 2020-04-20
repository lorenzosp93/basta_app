from django.core.validators import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_letter(letter, word):
    if not word.startswith(letter) and word:
        raise ValidationError(
            _("%(w)s does not start with %(l)s"),
            params={
                "w": word,
                "l": letter,
            }
        )
