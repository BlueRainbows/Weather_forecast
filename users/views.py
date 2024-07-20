from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views, get_user_model
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from users.forms import UserProfileForm, UserRegisterForm, UserLoginForm
from users.models import User
from users.services import get_verification


class RegisterView(generic.CreateView):
    """
    Контроллер для регистрации пользователя.
    Модель User, форма UserRegisterForm.
    При регистрации предусмотрена верификация.
    """
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:verification')

    def form_valid(self, form):
        """
        При успешном создании пользователя формирует токен,
        добавляет токен в базу данных и формирует сообщение для отправки на почту.
        """
        user = form.save(commit=False)
        get_verification(self.request, user)
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, generic.DetailView):
    """
    Контроллер профиля пользователя.
    Модель User.
    """
    model = User
    template_name = 'users/profile.html'

    def get_object(self, queryset=None):
        """
        Метод возвращающий текущего пользователя
        """
        return self.request.user


class UserLoginView(views.LoginView):
    """
    Контроллер для авторизации пользователя.
    """
    model = User
    form_class = UserLoginForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('main:index')


class ChangeProfileView(LoginRequiredMixin, generic.UpdateView):
    """
    Контроллер для изменения профиля пользователя.
    Модель User, форма UserRegisterForm.
    При успешном изменении переходит на себя.
    """
    model = User
    form_class = UserProfileForm
    template_name = 'users/change_profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        """
        Метод возвращающий текущего пользователя
        """
        return self.request.user


class UserDeleteView(LoginRequiredMixin, generic.DeleteView):
    """
    Контроллер для удаления пользователя.
    """
    model = User
    success_url = reverse_lazy('main:index')

    def get_object(self, queryset=None):
        """
        Метод возвращающий текущего пользователя
        """
        return self.request.user


class VerificationView(generic.TemplateView):
    """
    Контроллер перенаправляющий на уведомление о верификации через почту.
    """
    template_name = 'users/verification.html'


def activate(request, token):
    """
    Функция принимает токен, сверяет его с токенами по базе данных.
    При успешном нахождении пользователя активирует его, перенаправляет на уведомление о успешной верификации.
    Если токен не найден или ссылка повреждена перенаправляет на уведомление о ошибке.
    """
    try:
        user = User.objects.filter(token=token)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None
    if user is not None:
        user.update(is_active=True)
        return redirect(reverse('users:success_activate'))
    else:
        return redirect(reverse('users:error_activate'))


class UserPasswordResetView(views.PasswordResetView):
    """
    Контроллер для востановления пароля.
    Принимает почту пользователя.
    Формирует сообщение в шаблоне для отправки на почту в 'users/password_reset_email.html'.
    Переходит на уведомление о отправке сообщения на почту.
    """
    template_name = 'users/password_reset_form.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')


class UserPasswordResetDoneView(views.PasswordResetDoneView):
    """
    Контроллер перенаправляющий на уведомление о отправке сообщения на почту для изменении пароля.
    """
    template_name = 'users/password_reset_done.html'


class UserPasswordResetConfirmView(views.PasswordResetConfirmView):
    """
    Контроллер для востановления пароля.
    Принимает почту для востановления пароля, переопределяет новый пароль.
    Переходит на уведомление о успешной смена пароля.
    """
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')


class UserPasswordResetCompleteView(views.PasswordResetCompleteView):
    """
    Контроллер перенаправляющий на уведомление о успешном изменении пароля.
    """
    template_name = 'users/password_reset_complete.html'
