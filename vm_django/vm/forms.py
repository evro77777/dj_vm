from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import *
from django.core.exceptions import ValidationError
import re


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'input100','placeholder':'username'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'input100','placeholder':'password'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'input100', 'placeholder':'confirm password'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'input100', 'placeholder':'username'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'input100', 'placeholder':'password'}))


class QueryForm(forms.ModelForm):
    class Meta:
        model = QueryVM
        fields = ['pool', 'subdivision', 'name_vm']
    plans = (
        ('vc2-1c-1gb', 'Cores - 1, RAM - 1GB, Disk - 25GB'),
        ('vc2-1c-2gb', 'Cores - 1, RAM - 2GB, Disk - 55GB'),
        ('vc2-2c-4gb', 'Cores - 2, RAM - 4GB, Disk - 80GB'),
        ('vhf-2c-4gb', 'Cores - 2, RAM - 4GB, Disk - 128GB'),
        ('vdc-2c-8gb', 'Cores - 2, RAM - 8GB, Disk - 110GB'),
        ('vc2-4c-8gb', 'Cores - 4, RAM - 8GB, Disk - 160GB'),


    )
    choice_field = forms.ChoiceField(widget=forms.RadioSelect,
                                     choices= plans)
    pool = forms.ChoiceField(widget=forms.Select(attrs={'class': 'input100 input-select'}),
                             choices=(('Тестовый', 'Тестовый'),
                                      ('Рабочий', 'Рабочий')))
    subdivision = forms.ChoiceField(widget=forms.Select(attrs={'class': 'input-select input100 '}),
                                    choices=(('Отдел продаж', 'Отдел продаж'),
                                             ('Отдел тестирования', 'Отдел тестирования')))
    name_vm = forms.CharField(widget=forms.TextInput(attrs={'class':'input-select ','placeholder':'XXX-XXX'}))

    def clean_name_vm(self):
        name_vm = self.cleaned_data['name_vm']
        search = re.match(r'^[A-Za-z]{3}-[A-Za-z]{3}', name_vm)
        if not search:
            raise ValidationError('Имя не соответствует шаблону ХХХ-ХХХ')
        return name_vm
