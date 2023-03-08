from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import redirect, render, get_object_or_404
from .forms import AddBDayForm
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count
from django.views.generic import TemplateView
from datetime import datetime, timedelta
from django.db.models.functions import ExtractDay, ExtractMonth
from django.db.models import Q
from django.views.generic import ListView
from django.views import View
from datetime import date, timedelta
from django.db.models.functions import ExtractYear
from django.db.models import Q
from happy_bday.settings import TIME_ZONE
import calendar

from .utils import *
from .forms import *
from .models import BDays


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


class BDayList(LoginRequiredMixin, DataMixin, ListView):
    model = BDays  # Модель список екземплярів якої будемо подавати
    template_name = 'happy_site/bdays.html'  # Адреса шаблону, куди подавати
    context_object_name = 'b_days'  # Ім'я з яким викликається в шаблоні index.html

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # Передаємо вже сформований контекст
        c_def = self.get_user_context(title="Happy B-days!")

        context = {**context, **c_def}

        # get months with birthdays
        months = self.model.objects.filter(user=self.request.user).\
            order_by('date__month').values('date__month').distinct()
        # print(months)
        # for month in months:
        #     month['date__month'] = calendar.month_name[month['date__month']]
        #     print(month['date__month'])


        ###
        # for month in months:
        #     month['num_bdays'] = self.model.objects.filter(
        #         user=self.request.user,
        #         date__month=month['date__month']
        #     ).aggregate(num_bdays=Count('id'))['num_bdays']
        ###

        context['months'] = months

        return context

    def get_queryset(self):
        if month := self.request.GET.get('month'):
            bdays = self.model.objects.filter(user=self.request.user, date__month=month).order_by('date__day', 'title')
        else:
            bdays = self.model.objects.filter(user=self.request.user).order_by('date__month', 'date__day', 'title')

        # Add age information to each BDays instance
        for bday in bdays:
            bday.age = bday.get_age()

        return bdays


class NextBDay(TemplateView):
    template_name = 'happy_site/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Отримуємо сьогоднішню дату
            today = datetime.now()

            # Знаходимо наступний день народження
            next_birthday = BDays.objects.filter(
                Q(date__month=today.month, date__day__gte=today.day) | Q(date__month=today.month + 1,
                                                                         date__day__lte=today.day),
                user=self.request.user
            ).annotate(
                days_until_birthday=ExtractDay('date') - today.day + ExtractDay(
                    today.replace(year=today.year + 1, month=1, day=1))
            ).order_by('days_until_birthday').first()

            # Знаходимо сьогоднішній день народження
            today_birthday = BDays.objects.filter(
                date__month=today.month,
                date__day=today.day,
                user=self.request.user
            ).first()

            context['today_birthday'] = today_birthday

            context['next_birthday'] = next_birthday

            context['title'] = 'Birthday'

        return context


def sing_out(request):
    logout(request)
    return redirect('home')


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


class AddReminder(LoginRequiredMixin, CreateView):
    model = Reminder
    form_class = ReminderForm
    success_url = reverse_lazy('b_days')
    template_name = 'happy_site/add_reminder.html'

    def form_valid(self, form):
        bday = BDays.objects.get(pk=self.kwargs['bd_id'])
        form.instance.bday = bday
        form.instance.user = self.request.user

        form.instance.date_time = datetime.combine(
            form.instance.bday.date,
            form.cleaned_data['time_of_day']
        ).replace(year=datetime.now().year) - timedelta(days=form.cleaned_data['days_before'])
        print(timedelta(days=form.cleaned_data['days_before']))

        return super().form_valid(form)


def get_reminders_by_birthday(birthday):
    return Reminder.objects.filter(bday=birthday)



def edit_reminder(request, reminder_id):
    current_reminder = get_object_or_404(Reminder, pk=reminder_id)
    if request.method == 'POST':
        form = UpdateReminderForm(request.POST, instance=current_reminder)
        if form.is_valid():
            form.save()
            return redirect('b_days')
    else:
        form = UpdateReminderForm(instance=current_reminder)
    return render(request, 'happy_site/edit_reminder.html', {'form': form})


def del_reminder(request, reminder_id):
    current_reminder = Reminder.objects.filter(id=reminder_id)
    current_reminder.delete()
    return redirect('b_days')
