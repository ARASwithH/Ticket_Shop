from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'start_date', 'end_date', 'location',
                  'price_per_ticket', 'capacity', 'image', 'category',]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'price_per_ticket': forms.NumberInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.CheckboxSelectMultiple(),
        }


class AddCartForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control mb-2 w-25'})
    )

    def __init__(self, *args, **kwargs):
        capacity = kwargs.pop('capacity', None)
        super().__init__(*args, **kwargs)
        if capacity is not None:
            self.fields['quantity'] = forms.IntegerField(
                min_value=1,
                max_value=capacity,
                widget=forms.NumberInput(attrs={
                    'class': 'form-control mb-2 w-25',
                })
            )
