from django import forms
from .models import User
from django.core.exceptions import ValidationError


class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'id_card',
            'phone_number',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'id_card',
            'phone_number',
        )
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'id_card': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'phone_number': 'Phone Number',
            'id_card': 'ID',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True



class UserRegistrationForm(forms.Form):
    phone_number = forms.RegexField(
        regex=r'^\d{10,15}$',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
        error_messages={'invalid': 'Enter a valid phone number (10-15 digits).'}
    )

    id_card = forms.RegexField(
        regex=r'^\d{10,15}$',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ID Card'}),
        error_messages={'invalid': 'Enter a valid phone number (10-15 digits).'}
    )

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Password'}))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Confirm Password'}))

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        user = User.objects.filter(phone_number=phone_number)
        if user:
            raise forms.ValidationError("Phone number already exist")
        return phone_number

    def clean_id_card(self):
        id_card = self.cleaned_data.get('id_card')
        user = User.objects.filter(id_card=id_card)
        if user:
            raise forms.ValidationError("id_card already exist")
        return id_card


class UserVerificationForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Code'}))


class UserLoginForm(forms.Form):
    phone_number = forms.RegexField(
        regex=r'^\d{10,15}$',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
        error_messages={'invalid': 'Enter your phone number (10-15 digits).'}
    )

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Password'}))


class UserSendCodeForm(forms.Form):
    phone_number = forms.RegexField(
        regex=r'^\d{10,15}$',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
        error_messages={'invalid': 'Enter your phone number (10-15 digits).'}
    )

