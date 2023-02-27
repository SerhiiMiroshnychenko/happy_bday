from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import redirect, render, get_object_or_404
from .forms import AddBDayForm
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .models import BDays
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import *
from .forms import *


menu = [{'title': "Про сайт", 'url_name': 'home'},
        {'title': "Додати день народження", 'url_name': 'add_bday'},
        {'title': "Дні народження", 'url_name': 'b_days'},
        ]


# Create your views here.
def index(request):
    return render(request, 'happy_site/index.html', {'title': 'Happy B-Days!', 'menu': menu})


class AddBDay(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddBDayForm
    template_name = 'happy_site/add_bday.html'
    success_url = reverse_lazy('b_days')  # Маршрут, куди ми перейдемо після додавання статті
    # Функція reverse_lazy - будує маршрут коли він буде потрібен, а не наперед
    # Це запобігає помилці, коли маршрут намагається побудуватися, коли django
    # Ще його не побудував

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = 'Додавання дня народження'
        # context['menu'] = menu
        # return context
        c_def = self.get_user_context(title="Додавання дня народження")
        return dict(list(context.items()) + list(c_def.items()))


def edit_bd(request, bd_id):
    current_bd = get_object_or_404(BDays, pk=bd_id)
    if request.method == 'POST':
        form = UpdateBDayForm(request.POST, instance=current_bd)
        if form.is_valid():
            form.save()
            return redirect('b_days')
    else:
        form = UpdateBDayForm(instance=current_bd)
    return render(request, 'happy_site/edit_bday.html', {'form': form})


def delete_bd(request, bd_id):
    topic = BDays.objects.filter(id=bd_id)
    topic.delete()
    return redirect('b_days')


class BDayList(DataMixin, ListView):
    model = BDays  # Модель список екземплярів якої будемо подавати
    template_name = 'happy_site/bdays.html'  # Адреса шаблону, куди подавати
    context_object_name = 'b_days'  # Ім'я з яким викликається в шаблоні index.html

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # Передаємо вже сформований контекст
        # context['menu'] = menu
        # context['title'] = 'Happy B-days!'
        # return context
        c_def = self.get_user_context(title="Happy B-days!")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return BDays.objects.all()


def login(request):
    return HttpResponse('Вхід')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'happy_site/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Реєстрація")
        return dict(list(context.items()) + list(c_def.items()))


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'happy_site/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизація")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')



