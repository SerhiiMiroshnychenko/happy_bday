from django import template
from django.urls import reverse
from django.utils.html import format_html
from ..views import get_reminders_by_birthday

register = template.Library()


@register.simple_tag
def reminders_for_birthday(birthday):
    if not (reminders := get_reminders_by_birthday(birthday)):
        return ''
    html = ''
    for reminder in reminders:
        url = reverse('edit_reminder', args=[reminder.id])

        html += f'<a class="btn btn-secondary"' \
                f' href="{url}">{reminder.text} ' \
                f'{reminder.date_time.strftime("(%d.%m) %H:%M")}</a>' \
                f'<a class="btn btn-secondary" style="background-color: lightgray; color: rosybrown"' \
                f' href="/edit_reminder/{reminder.id}/delete" ' \
                f'onclick="return confirm(\'Ви впевнені, що хочете видалити це нагадування?\')">X</a><br />'
    return format_html(html)
