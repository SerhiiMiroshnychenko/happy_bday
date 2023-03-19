"""КЛАСИ ТА ФУНКЦІЇ ВІДОБРАЖЕННЯ"""

# Базові імпорти
from datetime import datetime, timedelta

# Імпорти Django
from django.urls import reverse_lazy
from django.db.models import QuerySet
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.core.handlers.wsgi import WSGIRequest
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import DetailView, CreateView, TemplateView, ListView

# Імпорти додатка HappyBot
from happy_bot.core.keyboards.inline import month_names
from happy_bot.core.handlers.reminders_and_birthdays import get_next_day_month

# Внутрішні імпорти
from happy_site.models import BDays, Reminder
from happy_site.utils import DataMixin
from happy_site.site_exceptions import SiteException
from happy_site.signals import update_reminders_for_signal
from happy_site.forms import RegisterUserForm, LoginUserForm, \
    AddBDayForm, UpdateBDayForm, ReminderForm, UpdateReminderForm


# Views of HappySite.
class RegisterUser(DataMixin, CreateView):
    """
    Клас-відображення для реєстрації користувачів
    """
    form_class = RegisterUserForm
    template_name = 'happy_site/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        """
        The get_context_data function is a method of the generic class-based view.
        Its purpose is to add additional context data to the template that will be rendered.
        The get_context_data function takes in an optional object list and keyword arguments,
        and returns a dictionary of context data.

        :param self: Represent the instance of the object
        :param : Unpack a list or tuple
        :param object_list: Pass a list of objects to the template
        :param kwargs: Pass keyword, variable-length argument list to a function
        :return: A dictionary of context
        """
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Реєстрація")
        return dict(list(context.items()) + list(c_def.items()))


class LoginUser(DataMixin, LoginView):
    """
    Клас-відображення для авторизації користувачів
    """
    form_class = LoginUserForm
    template_name = 'happy_site/login.html'

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        """
        The get_context_data function is a method of the generic class-based view.
        Its purpose is to add additional context data to the template that will be rendered.
        The get_context_data function takes in an optional object list and keyword arguments,
        and returns a dictionary of context data.

        :param self: Represent the instance of the object itself
        :param : Unpack the list into the function arguments
        :param object_list: Pass a list of objects to the template
        :param kwargs: Pass keyword, variable-length argument list to a function
        :return: A dictionary of context
        """
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизація")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        """
        The get_success_url function is used to redirect the user after a successful form submission.
        The default implementation will return the value of success_url, if it's set, or else will call
        reverse() on success_url_name (which should be a named URL pattern). If neither are set, then it'll
        raise ImproperlyConfigured.

        :param self: Refer to the object itself
        :return: A url that will be used to redirect the user after a successful form submission
        """
        return reverse_lazy('home')


def sing_out(request: WSGIRequest) -> HttpResponseRedirect:
    """
    The sing_out function logs the user out of their account and redirects them to the home page.

    :param request: WSGIRequest: Pass the request object to the view
    :return: The home page: HttpResponseRedirect
    """
    logout(request)
    return redirect('home')


class AddBDay(LoginRequiredMixin, DataMixin, CreateView):
    """
    Клас-відображення для додавання допису про день народження
    """
    form_class = AddBDayForm
    template_name = 'happy_site/add_bday.html'
    success_url = reverse_lazy('b_days')  # Маршрут, куди ми перейдемо після додавання статті

    # Функція reverse_lazy - будує маршрут коли він буде потрібен, а не наперед
    # Це запобігає помилці, коли маршрут намагається побудуватися, коли django
    # Ще його не побудував

    def form_valid(self: "AddBDay", form: AddBDayForm) -> HttpResponseRedirect:
        """
        The form_valid function is called when a valid form has been submitted.
        It should return an HttpResponse object, which could be the same response
        returned by get_success_url(). The default implementation calls form.save(),
        which will either create a new instance using the ModelForm’s save() method,
        or update an existing model instance if it was bound to an existing object
        (i.e., if the view was passed an object pk via its urlconf).

        :param self: AddBDay: Specify the type of the first parameter, which is self
        :param form: AddBDayForm: Pass the form to the parent class
        :return: HttpResponseRedirect
        """
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        The get_context_data function is used to add extra context variables to the template.
        The get_context_data function takes a single parameter, context, which is a dictionary
        of all the variables that will be available in your template.
        You can add new key-value pairs to this dictionary,
        and they will be accessible in your templates.

        :param self: Represent the instance of the object
        :param : Unpack a list or tuple
        :param object_list: Pass the list of objects to the template
        :param kwargs: Pass keyword, variable-length argument list to a function
        :return: A dictionary of context data
        """
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Додавання дня народження")
        return dict(list(context.items()) + list(c_def.items()))


def edit_bd(request: WSGIRequest, bd_id: int) -> HttpResponse:
    """
    The edit_bd function is used to edit a birthday.
    It takes in the request and the id of the birthday to be edited,
    and returns an HttpResponse object. It first gets the current bday from
    the database using get_object_or_404, then checks if it's a POST request.
    If so, it creates an UpdateBDayForm with the POST data and instance set as
    current_bd (which is what we're editing). If that form is valid, we save it
    and redirect to bday view for that particular birthday.

    :param request: WSGIRequest: Get the request that was sent to the server
    :param bd_id: int: Find the birthday that is being edited
    :return: A render function that renders the edit_bday
    """
    current_bd = get_object_or_404(BDays, pk=bd_id)
    if request.method == 'POST':
        form = UpdateBDayForm(request.POST, instance=current_bd)
        if form.is_valid():
            form.save()
            return redirect('bday', bday_pk=current_bd.pk)
    else:
        form = UpdateBDayForm(instance=current_bd)
    return render(request, 'happy_site/edit_bday.html', {'form': form})


def delete_bd(request: WSGIRequest, bd_id: int) -> HttpResponseRedirect:
    """
    The delete_bd function takes a request and an id of a birthday object,
        then deletes the birthday object from the database.

    :param request: WSGIRequest: Get the request object
    :param bd_id: int: Specify the id of the object to be deleted
    :return: The redirect function, which returns an HttpResponseRedirect object
    """
    topic = BDays.objects.filter(id=bd_id)
    topic.delete()
    if request:
        print(request)
    return redirect('b_days')


@method_decorator(login_required, name='dispatch')
class ShowBDay(DetailView):
    """
    Клас-відображення для окремого дня народження
    """
    model = BDays
    template_name = 'happy_site/bday.html'
    context_object_name = 'bday'

    # Returns the object the view is displaying.
    def get_object(self: "ShowBDay", queryset=None) -> BDays:
        """
        The get_object function is a helper function that returns the object
        the view will be operating on. It takes an optional queryset argument,
        which should be used if you need to provide custom queryset filtering.
        By default, this function uses get_object_or_404() to return the object -
        if it can’t find an object that matches your query it will raise Http404.

        :param self: ShowBDay: Access the current instance of the class
        :param queryset: Specify the queryset that should be used for looking up the object
        :return: BDays: the view is displaying
        """
        return get_object_or_404(
            BDays, pk=self.kwargs['bday_pk'], user=self.request.user
        )


class BDayList(LoginRequiredMixin, DataMixin, ListView):
    """
    Клас-відображення для набору днів народження
    """
    model = BDays  # Модель список екземплярів якої будемо подавати
    template_name = 'happy_site/bdays.html'  # Адреса шаблону, куди подавати
    context_object_name = 'b_days'  # Ім'я з яким викликається в шаблоні index.html

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        """
        The get_context_data function is a method that returns the context data for the template.
        The context data is a dictionary of key-value pairs, where each key represents a variable name
        in the template and each value represents its corresponding value. The get_context_data
        function takes an optional object_list parameter, which defaults to self.object_list if not provided.

        :param self: Represent the instance of the object itself
        :param : Unpack the list of arguments
        :param object_list: Pass the list of objects to display in the template
        :param kwargs: Pass keyword, variable-length argument list
        :return: A dictionary of context variables
        """
        context = super().get_context_data(**kwargs)  # Передаємо вже сформований контекст
        c_def = self.get_user_context(title="Happy B-days!")
        context = {**context, **c_def}

        # get months with birthdays
        months = self.model.objects.filter(user=self.request.user). \
            order_by('date__month').values('date__month').distinct()
        for month in months:
            month["name__month"] = month_names[month["date__month"]]
        context['months'] = months
        return context

    def get_queryset(self: "BDayList") -> QuerySet:
        """
        The get_queryset function is used to filter the queryset of BDay objects
            that are returned by the ListView. The default behavior is to return all
            instances of a model, but we want only those belonging to the current user.

        :param self: BDayList: Specify the type of self
        :return: A queryset object
        """
        if month := self.request.GET.get('month'):
            bdays = self.model.objects.filter(user=self.request.user, date__month=month).order_by('date__day', 'title')
        else:
            bdays = self.model.objects.filter(user=self.request.user).order_by('date__month', 'date__day', 'title')

        # Add age information to each BDays instance
        for bday in bdays:
            bday.age = bday.get_age()
            if bday.photo:
                print('PHOTO->', bday.photo.path)
        return bdays


class NextBDay(TemplateView):
    """
    Клас для відображення найближчих днів народження
    """
    template_name = 'happy_site/index.html'

    def get_context_data(self, **kwargs) -> dict:
        """
        The get_context_data function is a method that
        Django calls when rendering the template.
        It allows you to add additional context variables to the template,
        which are then available in your templates.

        :param self: Represent the instance of the object itself
        :param kwargs: Pass a variable number of keyword arguments to a function
        :return: A dictionary of context data for the template to use
        """
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Отримуємо сьогоднішню дату
            today = datetime.now()

            # Знаходимо сьогоднішні дні народження
            today_birthdays = BDays.objects.filter(
                date__month=today.month,
                date__day=today.day,
                user=self.request.user
            ).order_by('date', 'title')

            # Знаходимо наступні дні народження
            birthdays = BDays.objects.filter(user=self.request.user). \
                order_by('date__month', 'date__day', 'title')
            next_day_month = get_next_day_month(today, birthdays)
            next_day, next_month = None, None
            try:
                next_day = next_day_month[0]
                next_month = next_day_month[1]
            except TypeError as error:
                print(error.__class__, error)
            if next_day and next_month:
                next_birthdays = BDays.objects.filter(
                    date__month=next_day_month[1],
                    date__day=next_day_month[0],
                    user=self.request.user
                ).order_by('date', 'title')
            else:
                next_birthdays = None

            context['today_birthdays'] = today_birthdays
            context['next_birthdays'] = next_birthdays

            context['title'] = 'Birthday'

        return context


class AddReminder(LoginRequiredMixin, CreateView):
    """
    Клас-відображення для додавання нагадування до дня народження
    """
    model = Reminder
    form_class = ReminderForm
    template_name = 'happy_site/add_reminder.html'

    def form_valid(self: "AddReminder", form: ReminderForm) -> HttpResponseRedirect:
        """
        The form_valid function is called when a valid form has been submitted.
        It should return an HttpResponseRedirect object to redirect the user to another page,
        or an empty HttpResponse object if rendering a template containing the submitted data.

        :param self: AddReminder: Specify the type of self
        :param form: ReminderForm: Get the form data from the user
        :return: HttpResponseRedirect
        """
        bday = BDays.objects.get(pk=self.kwargs['bd_id'])
        form.instance.bday = bday
        form.instance.user = self.request.user

        form.instance.date_time = datetime.combine(
            form.instance.bday.date,
            form.cleaned_data['time_of_day']
        ).replace(year=datetime.now().year) - timedelta(days=form.cleaned_data['days_before'])

        if form.instance.date_time.date() < datetime.now().date():
            form.instance.date_time = form.instance.date_time.replace(year=datetime.now().year + 1)
        return super().form_valid(form)

    def get_success_url(self):
        """
        The get_success_url function is used to redirect
        the user after a successful form submission.
        The default implementation will raise NotImplementedError
        if no success_url attribute is defined on the view.

        :param self: Access the current object
        :return: The url for the bday page
        """
        return reverse_lazy('bday', kwargs={'bday_pk': self.kwargs['bd_id']})


def get_reminders_by_birthday(birthday: BDays) -> QuerySet:
    """
    The get_reminders_by_birthday function returns a QuerySet
    of Reminder objects that are associated with the given birthday.

    :param birthday: BDays: Specify the type of parameter that is expected to be passed into the function
    :return: A QuerySet of all reminders associated with the given birthday
    """
    return Reminder.objects.filter(bday=birthday)


def edit_reminder(request: WSGIRequest, reminder_id: int) -> HttpResponse:
    """
    The edit_reminder function is used to edit a reminder.
        It takes in the request and the id of the reminder to be edited as parameters.
        The function first gets the current_reminder object from Reminder model using
        get_object_or_404 method, which returns an HttpResponseNotFound if no such object exists.

    :param request: WSGIRequest: Get the request that was sent to the server
    :param reminder_id: int: Get the reminder that is being edited
    :return: The HttpResponse object returned by the render function
    """
    current_reminder = get_object_or_404(Reminder, pk=reminder_id)
    if request.method == 'POST':
        form = UpdateReminderForm(request.POST, instance=current_reminder)
        if form.is_valid():
            form.save()

            return redirect('bday', bday_pk=current_reminder.bday.id)
    else:
        form = UpdateReminderForm(instance=current_reminder)

    return render(request, 'happy_site/edit_reminder.html', {'form': form})


def del_reminder(request: WSGIRequest, reminder_id: int) -> HttpResponseRedirect:
    """
    The del_reminder function deletes a reminder from the database.
        It takes in a request and an id of the reminder to be deleted,
        then it finds that specific reminder in the database and deletes it.
        After deleting, it redirects to bday page with birthday's id as parameter.

    :param request: WSGIRequest: Get the request object
    :param reminder_id: int: Get the id of the reminder
    :return: An HttpResponseRedirect object that redirects to the bday page
    """
    current_reminder = Reminder.objects.filter(id=reminder_id)
    bday_id = current_reminder.first().bday.id
    try:
        current_reminder.delete()
    except SiteException as error:
        print(error.__class__, error, 'in del_reminder')
    try:
        print(f'IN VIEW: {request}')
        update_reminders_for_signal()
    except SiteException as error:
        print(error.__class__, error, 'in del_reminder')

    return redirect('bday', bday_pk=bday_id)
