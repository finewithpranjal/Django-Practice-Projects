from accounts.models import User
from django import forms 

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'confirm_password']

    def clean(self):
            cleaned_data = super().clean()
            password = cleaned_data.get('password')
            confirm_password = cleaned_data.get('confirm_password')

            if password != confirm_password:
                raise forms.ValidationError("Passwords do not match.")

            return cleaned_data

    def clean_email(self):
            email = self.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("A user with this Email already exists.")
            return email


class PasswordResetForm(forms.Form):
        email = forms.EmailField(
             max_length=254,
             widget=forms.EmailInput(attrs={'placeholder': 'you@example.com'})
        )

        def clean_email(self):
            email = self.cleaned_data.get('email')
            if not User.objects.filter(email=email).exists():
                raise forms.ValidationError("No user is associated with this email address.")
            return email

        