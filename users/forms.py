from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms
from users.models import User


class StyleFormsMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if isinstance(field, forms.BooleanField):
                field.widget.attrs.update({'class': 'form-check-input'})


class UserLoginForm(StyleFormsMixin, AuthenticationForm):
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('email', 'password')


class UserRegisterForm(StyleFormsMixin, UserCreationForm):
    email = forms.EmailField(
        label='Электоронная почта'
    )
    password1 = forms.CharField(
        min_length=8,
        label="Придумайте пароль", widget=forms.PasswordInput,
        help_text='<em>* Ваш пароль не должен быть простым,'
                  ' содержать только цифры и '
                  'иметь длинну не менее 8-ми символов</em>'
    )
    password2 = forms.CharField(
        min_length=8,
        label="Повторите пароль", widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'password1', 'password2')


class UserProfileForm(StyleFormsMixin, UserChangeForm):
    avatar = forms.ImageField(
        label='Аватар',
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'avatar', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()
