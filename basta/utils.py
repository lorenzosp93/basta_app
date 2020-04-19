from django.core.validators import ValidationError

def validate_letter(letter, word):
    if not word.startswith(letter):
                raise ValidationError(
                    _("%(w)s does not start with %(l)s"),
                    params={
                        "w": word,
                        "l": letter,
                    }
                )
