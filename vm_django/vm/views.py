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


def addquery(request):
    if not request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = QueryForm(request.POST)
            if form.is_valid():
                try:
                    if form.cleaned_data['choice_field'] == 'vc2-1c-1gb':
                        vultr_api(plan='vc2-1c-1gb', name_vm=form.cleaned_data['name_vm'])
                        form.cleaned_data.pop('choice_field')
                        QueryVM.objects.create(user=request.user, ram=1, cpu_cores=1, ssd=25, **form.cleaned_data)

                    elif form.cleaned_data['choice_field'] == 'vc2-1c-2gb':
                        vultr_api(plan='vc2-1c-2gb', name_vm=form.cleaned_data['name_vm'])
                        form.cleaned_data.pop('choice_field')
                        QueryVM.objects.create(user=request.user, ram=2, cpu_cores=1, ssd=55, **form.cleaned_data)

                    elif form.cleaned_data['choice_field'] == 'vc2-2c-4gb':
                        vultr_api(plan='vc2-2c-4gb', name_vm=form.cleaned_data['name_vm'])
                        form.cleaned_data.pop('choice_field')
                        QueryVM.objects.create(user=request.user, ram=4, cpu_cores=2, ssd=80, **form.cleaned_data)

                    elif form.cleaned_data['choice_field'] == 'vhf-2c-4gb':
                        vultr_api(plan='vhf-2c-4gb', name_vm=form.cleaned_data['name_vm'])
                        form.cleaned_data.pop('choice_field')
                        QueryVM.objects.create(user=request.user, ram=4, cpu_cores=2, ssd=128, **form.cleaned_data)

                    elif form.cleaned_data['choice_field'] == 'vdc-2c-8gb':
                        vultr_api(plan='vdc-2c-8gb', name_vm=form.cleaned_data['name_vm'])
                        form.cleaned_data.pop('choice_field')
                        QueryVM.objects.create(user=request.user, ram=8, cpu_cores=2, ssd=110, **form.cleaned_data)

                    elif form.cleaned_data['choice_field'] == 'vc2-4c-8gb':
                        vultr_api(plan='vc2-4c-8gb', name_vm=form.cleaned_data['name_vm'])
                        form.cleaned_data.pop('choice_field')
                        QueryVM.objects.create(user=request.user, ram=8, cpu_cores=4, ssd=160, **form.cleaned_data)
                    addr = get_ip_address(plan='vc2-1c-1gb', name_vm=form.cleaned_data['name_vm'])
                    return render(request, 'vm/result.html', {'address': addr})
                except:
                    form.add_error(None, 'Error')
        else:
            form = QueryForm()
        return render(request, 'vm/form.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('login')
