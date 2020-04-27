from django import forms
from .models import Play, PlayCategory, CATEGORIES

# Create your forms here
PlayCategoryFormSet = forms.inlineformset_factory(
    Play,
    PlayCategory,
    localized_fields=('__all__',),
    fields=['value',],
    widgets={
        'value': forms.TextInput(
            attrs={
                'required': False,
                'class': 'form-control',
                'autocomplete': 'off',
            },
        ),
        'id': forms.HiddenInput(),
        'play': forms.HiddenInput()
    },
    can_delete=False,
    extra=0,
)

class PlayForm(forms.ModelForm):
    class Meta:
        model = Play
        fields = ['id']
        widgets = {
            'id': forms.HiddenInput(),
        }