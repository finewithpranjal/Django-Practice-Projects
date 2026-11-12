from django.shortcuts import render
from django.views import View
from django.views.generic import FormView
from accounts.forms import RegistrationForm, PasswordResetForm
from accounts.models import *
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from django.contrib import messages
from accounts.utils import send_activation_email, send_password_reset_email
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.contrib.auth.forms import SetPasswordForm

# Create your views here.


class HomeView(View):
    def get(self, req, *args, **kwargs):
        return render(req, 'accounts/home.html')


class LoginView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_seller:
                return redirect('seller_dashboard')
            elif request.user.is_customer:
                return redirect('customer_dashboard')
            else:
                messages.error(
                    request, "User role is not defined. Please contact support.")
                return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, req, *args, **kwargs):
        return render(req, 'accounts/login.html')

    def post(self, req, *args, **kwargs):
        email = req.POST.get('email')
        password = req.POST.get('password')
        if not email or not password:
            messages.error(req, 'Please provide both email and password.')
            return redirect('login')

        # Check if the user exists.
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(req, "Invalid Credentials. Please try again.")
            return redirect('login')

        # Check if the password is inactive.
        if not user.is_active:
            messages.error(
                req, "Your account is inactive. Please check your email for activation link.")
            return redirect('login')

        # Authenticate the user.
        user = authenticate(req, email=email, password=password)
        if user is not None:
            # Log the user in and redirect to the dashboard.
            login(req, user)
            if user.is_seller:
                return redirect('seller_dashboard')

            elif user.is_customer:
                return redirect('customer_dashboard')

            else:
                messages.error(
                    req, "User role is not defined. Please contact support.")
                return redirect('home')
        else:
            messages.error(req, "Invalid Credentials. Please try again.")
            return redirect('login')


class RegisterView(FormView):
    form_class = RegistrationForm
    template_name = 'accounts/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.is_active = False  # Deactivate account unitll email is verified.
        user.save()

        # Send verification email logic here
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        # You can use the uidb64 and token to create a verification link
        activation_link = reverse(
            'activate', kwargs={'uidb64': uidb64, 'token': token}
        )

        # Send the activation link via email to the user
        activation_url = f'{settings.SITE_DOMAIN}{activation_link}'

        send_activation_email(user.email, activation_url)
        messages.success(
            self.request, f'Account created successfully! Please check your email to activate your account.')

        return redirect('login')


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if user.is_active:
            messages.warning(
                request, 'Account is already activated. Please log in.')
            return redirect('account:login')

        if default_token_generator.check_token(user, token):
            user.is_active = True  # Activate the user account
            user.save()
            messages.success(
                request, 'Your account has been activated successfully! You can now log in.')
            return redirect('login')
        else:
            messages.error(
                request, 'Activation link is invalid or has expired.')
            return redirect('login')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, 'Activation link is invalid or has expired.')
        return redirect('login')


class CustomPasswordResetView(FormView):
    template_name = 'accounts/password_reset.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        user = User.objects.filter(email=email).first()
        

        if user:
            reset_url = self.get_reset_url(user)
            send_password_reset_email(user.email, reset_url)
            messages.success(
        self.request,
        'Please check your email for password reset instructions.'
    )

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, 'No account with that email address exists.')
        return super().form_invalid(form)

    def get_reset_url(self, user):
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_url = reverse_lazy('password_reset_done', kwargs={
                                 'uidb64': uid, 'token': token})
        return f"{self.request.build_absolute_uri(reset_url)}"


class PasswordResetDoneView(View):
    template_name = 'accounts/password_reset_done.html'

    def get(self, req, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)

            # check the token validity
            if default_token_generator.check_token(user, token):
                form = SetPasswordForm(user=user)
                return render(req, self.template_name, {'form': form, 'uidb64': uidb64, 'token': token,  'validlink': True})

            else:
                messages.error(
                    req, 'Password reset link is invalid or has expired.')
                return redirect('password_forgot')

        except Exception as e:
            print("PASSWORD RESET ERROR:", repr(e))
            messages.error(req, 'An error occurred while processing your request. Please try again later.')
            return redirect('password_forgot')

        # except Exception as e:
        #     messages.error(
        #         req, 'An error occurred while processing your request. Please try again later.')
        #     return redirect('password_forgot')

    def post(self, req, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)

            # check the token validity
            if default_token_generator.check_token(user, token):
                form = SetPasswordForm(user=user, data=req.POST)
                if form.is_valid():
                    form.save()
                    messages.success(
                        req, 'Your password has been reset successfully. You can now log in.')
                    return redirect('login')
                else:
                    for field, errors in form.errors.items():
                        for error in errors:
                            messages.error(req, error)
                    return render(req, self.template_name, {'form': form, 'uidb64': uidb64, 'token': token, 'validlink': True})
            else:
                messages.error(
                    req, 'Password reset link is invalid or has expired.')
                return redirect('password_forgot')
        except Exception as e:
            messages.error(
                req, 'An error occurred while processing your request. Please try again later.')
            return redirect('password_forgot')
