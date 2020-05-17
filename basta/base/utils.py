from django.core.validators import ValidationError
from django.utils.translation import gettext_lazy as _
import doctest
doctest.IGNORE_EXCEPTION_DETAIL = True

def validate_starts(letter, word, field=None):
    if not word.lower().startswith(letter.lower()) and word:
        err = ValidationError(
            _("%(word)s does not start with %(letter)s"),
            params={
                "word": word,
                "letter": letter,
            }
        )
        if not field:
            raise err
        raise ValidationError({
                field: err
            })
