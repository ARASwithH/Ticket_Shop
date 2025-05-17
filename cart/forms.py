from django import forms


class PaymentMethodForm(forms.Form):
    METHODS = [
        ('credit', 'Credit Cart'),
        ('paypal', 'PatPal'),
        ('cash', 'Cash'),
    ]

    payment_methods = forms.ChoiceField(choices=METHODS, widget=forms.Select(attrs={'class': 'form-control'}))


class DiscountForm(forms.Form):
    code = forms.CharField(max_length=10, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control me-3'}))

