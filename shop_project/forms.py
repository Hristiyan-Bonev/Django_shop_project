from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from .models import Order, Item


class UserCreationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput,
                                help_text="Enter the same password as above, for verification.")
    username = forms.CharField(widget=forms.TextInput(attrs={'id': 'username1'}))
    class Meta:
        model = get_user_model()
        fields = [
            'first_name',
            'last_name',
            'email',
            'country',
            'city',
            'delivery_address',
            'username',
        ]

    def clean(self):
        cleaned_data = super(UserCreationForm, self).clean()
        password = self.cleaned_data.get("password1")
        confirm_password = self.cleaned_data.get("password2")
        if password and confirm_password and password != confirm_password:
             raise forms.ValidationError(
                 self.error_messages['password_mismatch'],
                 code='password_mismatch',
             )
        return cleaned_data

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        pass


class CheckoutForm(forms.ModelForm):

    total_price = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    class Meta:
        model = Order
        fields = ['order_items','total_price']