from django.forms import ModelForm
from .models import Play

# Create your forms here

class PlayForm(ModelForm):
    class Meta:
        model = Play
        exclude = ["cur_round", "user"]