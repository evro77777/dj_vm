from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from .forms import *
from .models import *
from .utils import *
import re

def index(request):
    context = {
        'title': 'Главная страница'
    }
    return render(request, 'vm/index.html', context=context)


def query_vm(request):
    return HttpResponse('запрос vm')


def pageNotFound(request, exception):
    return HttpResponseNotFound('Страница не найдена')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'vm/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('form')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'vm/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context

    def get_success_url(self):
        return reverse_lazy('form')

def create_form(request):
    form = QueryForm(request.POST)
    if form.is_valid():
        params = {
                'vc2-1c-1gb':(1, 1, 25),
                'vc2-1c-2gb':(2,1, 55),
                'vc2-2c-4gb': (4, 2, 80),
                'vhf-2c-4gb': (4, 2, 128),
                'vdc-2c-8gb': (8, 2, 110),
                'vc2-4c-8gb': (8, 4, 160)

            }
        key = form.cleaned_data['choice_field']
        ram, cpu_cores, ssd = params.get(key)
        try:
            vultr_api(plan=key, name_vm=form.cleaned_data['name_vm'])
            addr = get_ip_address(plan=key, name_vm=form.cleaned_data['name_vm'])
            form.cleaned_data.pop('choice_field')
            QueryVM.objects.create(user=request.user, ram=ram, cpu_cores=cpu_cores, ssd=ssd, **form.cleaned_data)
            return addr
        except:
            form.add_error(None, 'Error')

        return form

def addquery(request):
    if request.user.is_authenticated:
        result = create_form(request) if request.method == 'POST' else QueryForm()
    else: 
        return redirect('home')

    if re.match(r'([0-9]{1,3}[\.]){3}[0-9]{1,3}', str(result)):
        return render(request, 'vm/result.html', {'address': result})

    return render(request, 'vm/form.html', {'form': result})







def logout_user(request):
    logout(request)
    return redirect('login')
