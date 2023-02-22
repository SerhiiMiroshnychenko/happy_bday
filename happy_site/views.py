from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import redirect, render, get_object_or_404
from .forms import AddBDayForm
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .models import BDays

menu = [{'title': "Про сайт", 'url_name': 'home'},
        {'title': "Додати день народження", 'url_name': 'add_bday'},
        {'title': "Дні народження", 'url_name': 'b_days'},
        ]


# Create your views here.
def index(request):
    return render(request, 'happy_site/index.html', {'title': 'Happy B-Days!', 'menu': menu})


class AddBDay(CreateView):
    form_class = AddBDayForm
    template_name = 'happy_site/add_bday.html'
    success_url = reverse_lazy('b_days')  # Маршрут, куди ми перейдемо після додавання статті
    # Функція reverse_lazy - будує маршрут коли він буде потрібен, а не наперед
    # Це запобігає помилці, коли маршрут намагається побудуватися, коли django
    # Ще його не побудував

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Додавання статті'
        context['menu'] = menu
        return context


class BDayList(ListView):
    model = BDays  # Модель список екземплярів якої будемо подавати
    template_name = 'happy_site/bdays.html'  # Адреса шаблону, куди подавати
    context_object_name = 'b_days'  # Ім'я з яким викликається в шаблоні index.html

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # Передаємо вже сформований контекст
        context['menu'] = menu
        context['title'] = 'Головна сторінка'
        return context

    def get_queryset(self):
        return BDays.objects.all()
