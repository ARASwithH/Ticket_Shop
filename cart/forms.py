from django import forms


class PaymentMethodForm(forms.Form):
    METHODS = [
        ('credit', 'Credit Cart'),
        ('paypal', 'PatPal'),
        ('cash', 'Cash'),
    ]

    payment_methods = forms.ChoiceField(choices=METHODS, widget=forms.Select(attrs={'class': 'form-control'}))

