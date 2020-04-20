from django.core.validators import ValidationError
from django.utils.translation import gettext_lazy as _
import doctest
doctest.IGNORE_EXCEPTION_DETAIL = True

def validate_starts(letter, word):
    """
    >>> validate_starts('a', 'airplane')

    """
    if not word.startswith(letter) and word:
        raise ValidationError(
            _("%(word)s does not start with %(letter)s"),
            params={
                "word": word,
                "letter": letter,
            }
        )
