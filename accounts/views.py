from django.shortcuts import render, redirect
from . import models, forms
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


# Create your views here.

class UserRegistrationView(View):
    form_class = forms.UserRegistrationForm
    template_name = 'accounts/registration.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form,
                                                    'name': 'SignUp'})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            code = models.OTPcode.create_otp(phone_number=cd['phone_number'])
            request.session['user_registration_info'] = {
                'phone_number': cd['phone_number'],
                'id_card': cd['id_card'],
                'first_name': cd['first_name'],
                'last_name': cd['last_name'],
                'age': cd['age'],
                'password': cd['password1'],
            }
            messages.success(request, 'We send you a code', 'success')
            return redirect('accounts:verify')
        return render(request, self.template_name, {'form': form})


class UserVerifyView(View):
    form_class = forms.UserVerificationForm
    template_name = 'accounts/verify.html'
    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        user_info = request.session['user_registration_info']
        phone_number = user_info['phone_number']
        if form.is_valid():
            code = form.cleaned_data['code']
            existed_code = models.OTPcode.objects.filter(phone_number=phone_number)
            if int(code) == int(existed_code[0].code):
                models.OTPcode.objects.filter(phone_number=phone_number).delete()
                user = models.User(
                    phone_number=user_info['phone_number'],
                    id_card=user_info['id_card'],
                    first_name=user_info['first_name'],
                    last_name=user_info['last_name'],
                    age=user_info['age'],
                )
                user.set_password(user_info['password'])
                user.save()
                return redirect('accounts:login')
        return render(request, self.template_name, {'form': form})



class UserLoginView(View):
    form_class = forms.UserLoginForm
    template_name = 'accounts/login.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['phone_number'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, f'{user.last_name} logged in', 'success')
                return redirect('home:home')
        messages.error(request, 'Invalid username or password', 'warning')
        return render(request, self.template_name, {'form': form,
                                                    'name': 'Login'})


class UserSendCodeView(View):
    form_class = forms.UserSendCodeForm
    template_name = 'accounts/send_code.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            models.OTPcode.create_otp(phone_number=phone_number)
            request.session['user_registration_info'] = {
                'phone_number': phone_number,
            }
            messages.success(request, 'We send you a code', 'success')
            return redirect('accounts:send_code_verify')
        messages.error(request, 'Invalid phone number', 'warning')
        return render(request, self.template_name, {'form': form})


class UserLoginVerifyView(View):
    form_class = forms.UserVerificationForm
    template_name = 'accounts/verify.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        phone_number = request.session['user_registration_info']['phone_number']
        if form.is_valid():
            code = form.cleaned_data['code']
            existed_code = models.OTPcode.objects.filter(phone_number=phone_number)
            if int(code) == int(existed_code[0].code):
                models.OTPcode.objects.filter(phone_number=code).delete()
                login(request, authenticate(phone_number=phone_number))
                messages.success(request, 'login successfully', 'success')
                return redirect('home:home')
        return render(request, self.template_name, {'form': form})



class UserLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You have been logged out', 'success')
        return redirect('home:home')








