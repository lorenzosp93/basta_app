from django import forms
from .models import Session, Play, PlayCategory, CATEGORIES


# Create your forms here
PlayCategoryFormSet = forms.inlineformset_factory(
    Play,
    PlayCategory,
    localized_fields=('__all__',),
    fields=['value',],
    widgets={
        'value': forms.TextInput(
            attrs={
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

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['name', 'categories','random_categories']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'random_categories': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

