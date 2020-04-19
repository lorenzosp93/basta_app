from django.forms import ModelForm
from .models import Play

# Create your forms here

class PlayForm(ModelForm):
    "Form for the Play model"
    class Meta:
        model = Play
        exclude = ["cur_round", "user"]