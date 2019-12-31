from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.views.generic import View

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.template.context_processors import csrf

from django.contrib import auth
from .models import UserObj
from .forms import UserForm, ChangeForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from django.core.mail import EmailMessage
# from ipware.ip import get_real_ip
from ipware import get_client_ip

# Create your views here.
class Home(LoginRequiredMixin, View):

	def get(self, request):
		active = "home"
		users = UserObj.objects.all()
		form = UserForm()

		return render(request, "login/home.html", context={"active": active, "users": users, "form": form})

	def post(self, request):
		active = "home"
		users = UserObj.objects.all()
		bound_form = UserForm(request.POST)

		if bound_form.is_valid():
			UserObj.objects.create(
				user = request.user,
				name = bound_form.cleaned_data['name'],
				phone_number = bound_form.cleaned_data['phone_number'],
				email = bound_form.cleaned_data['email'],
				address = bound_form.cleaned_data['address'],
				description = bound_form.cleaned_data['description']
			)
			return redirect("home_page")
		else:
			error = "Невозможно создать пользователя. Убедитесь, что форма заполнена правильно"
			return render(request, "login/home.html", context={"active": active, "users": users, "form": bound_form, "error": error})


class LoginUser(View):

	def get(self, request):
		if request.user.is_authenticated:
			return redirect("home_page")

		active = "login"
		return render(request, "login/login.html", context={"active": active})

	def post(self, request):
		dictionary = {}
		active = "login"

		dictionary.update(csrf(request))
		username = request.POST["username"]
		password = request.POST["password"]

		user = auth.authenticate(username = username, password = password)
		if user is not None:
			auth.login(request, user)

			try:
				client_ip, is_routable = get_client_ip(request)
				email = EmailMessage(
					subject="От администрации django",
					body=f"Был выполнен вход на ваш аккаунт - {client_ip}",
					from_email="artemka_pro@inbox.ru",
					to=[user.email],
					reply_to=[user.email, "artemka_pro@inbox.ru"]
				)
				sent = email.send(fail_silently=False)
			except Exception:
				return redirect("home_page")

			return redirect("home_page")
		else:
			error = "Пользователь не найден"
			return render(request, "login/login.html", context={"dictionary": dictionary, "active": active, "error": error})

class EditUser(LoginRequiredMixin, View):

	def get(self, request, user_id):
		user = get_object_or_404(UserObj, id = user_id)
		form = UserForm(instance = user)

		return render(request, "login/edit.html", context={"form": form, "user": user})

	def post(self, request, user_id):
		user = get_object_or_404(UserObj, id = user_id)
		bound_form = UserForm(request.POST, instance = user)

		if bound_form.is_valid():
			bound_form.save()
			return redirect("home_page")
		else:
			error = "Произошла ошибка в сохранении пользователя!"
			return render(request, "login/edit.html", context={"form": bound_form, "user": user})

class CreateAccount(LoginRequiredMixin, View):

	def get(self, request):
		form = UserCreationForm()
		active = "create_account"

		return render(request, "login/create_account.html", context={"form": form, "active": active})

	def post(self, request):
		bound_form = UserCreationForm(request.POST)
		active = "create_account"

		if bound_form.is_valid():
			bound_form.save()
			return redirect("logout")
		else:
			error = "Невозможно создать аккаунт!"
			return render(request, "login/create_account.html", context={"form": bound_form, "active": active})


class ProfilePage(LoginRequiredMixin, View):

	def get(self, request):
		active = "profile"
		form = ChangeForm(instance=request.user)

		return render(request, "login/profile.html", context={"active": active, "form": form})

	def post(self, request):
		bound_form = ChangeForm(request.POST, instance=request.user)

		if bound_form.is_valid():
			new_user = bound_form.save()
			return redirect('home_page')
		
		error = "Невозможно изменить профиль"
		return render(request, "login/profile.html", context={"active": "login", "form": bound_form, "error": error})


class ChangePassword(LoginRequiredMixin, View):

	def get(self, request):
		form = PasswordChangeForm(request.user)

		return render(request, "login/change_password.html", context={"form": form})

	def post(self, request):
		bound_form = PasswordChangeForm(request.user, request.POST)

		if bound_form.is_valid():
			user = bound_form.save()
			update_session_auth_hash(request, user)
			return redirect("logout")

		error = "Невозможно изменить пароль. Произошла ошибка"
		return render(request, "login/change_password.html", context={"form": bound_form, "error": error})

@login_required
def logout_func(request):
	auth.logout(request)
	return redirect("login")

@login_required
def delete_user(request, user_id):
	user = get_object_or_404(UserObj, id = user_id)
	user.delete()
	return redirect("home_page")

