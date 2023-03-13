import pytz
from django import template
from django.urls import reverse
from django.utils.html import format_html
from ..views import get_reminders_by_birthday
from happy_bday.settings import TIME_ZONE

register = template.Library()


@register.simple_tag
def reminders_for_birthday(birthday):
    if not (reminders := get_reminders_by_birthday(birthday).order_by('date_time')):
        return ''
    html = "<p style='font-weight: bold; color: steelblue; text-align: left;'>Пам'ятки:</p>"
    for reminder in reminders:
        url = reverse('edit_reminder', args=[reminder.id])

        html += f'<div style="margin: 10px; padding: 10px"><a class="btn btn-secondary" ' \
                f' href="{url}">{reminder.text} ' \
                f'{reminder.date_time.astimezone(tz=pytz.timezone(TIME_ZONE)).strftime("(%d.%m.%y) %H:%M")}</a>' \
                f'<a class="btn btn-secondary" style="background-color: #D8E8FC; color: rosybrown"' \
                f' href="/edit_reminder/{reminder.id}/delete" ' \
                f'onclick="return confirm(\'Ви впевнені, що хочете видалити це нагадування?\')"' \
                f'onmouseover="this.style.backgroundColor=\'rosybrown\'; this.style.color=\'white\'"  ' \
                f'onmouseout="this.style.backgroundColor=\'#D8E8FC\'; this.style.color=\'rosybrown\'">X</a></div>'
    return format_html(html)
