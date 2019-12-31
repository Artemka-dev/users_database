from django import forms
from .models import *

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):

	class Meta:
		model = UserObj
		fields = ['name', "phone_number", "email", "address", "description"]

		widgets = {
			'name':forms.TextInput(attrs={"placeholder": "Имя"}),
			'phone_number': forms.TextInput(attrs={"placeholder": "Номер телеофна"}),
			'email': forms.TextInput(attrs={"placeholder": "Почта"}),
			'address': forms.TextInput(attrs={"placeholder": "Место проживания"}),
			'description': forms.Textarea()
		}

		labels = {
			'name': _("Имя пользователя"),
			'phone_number': _("Номер телефона *"),
			"email": _("Почта *"),
			"address": _("Место проживания *"),
			"description": _("Краткое описание *")
		}

class ChangeForm(UserChangeForm):

	class Meta:
		model = User
		fields = ['username', "email", "first_name", 'last_name']

		labels = {
			'username': _('Имя пользователя'),
			'email': _('Почта *'),
			'first_name': _('Ваше имя *'),
			'last_name': _('Ваша фамилия *'),
		}
