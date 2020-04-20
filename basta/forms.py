from django import forms
from .models import Play

# Create your forms here

class PlayForm(forms.ModelForm):
    class Meta:
        model = Play
        exclude = ["cur_round", "user"]
        widgets = {
            fieldname: forms.TextInput(attrs={
                'id': fieldname, 
                'required': False,
                'class': "form-control",
                'autocomplete': 'off'
            }) for fieldname in Play.__dict__.keys()
        }
