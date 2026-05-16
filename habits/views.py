import calendar
from datetime import date, datetime

from django.shortcuts import render, redirect, get_object_or_404
from .models import CalendarEntry, CalendarDay


def home(request):
    """
    Home page: layout + sidebar + tabs.
    Calendar:
      - Shows real month for selected_date.
      - Clicking a day:
        * selects that date
        * cycles its status: none -> done -> cancel -> none.
    Daily notes:
      - Saved per (entry, selected_date).
    """
    entries = CalendarEntry.objects.all().order_by('order', 'id')
    active_entry = entries.first() if entries else None

    # 1) Determine active entry
    entry_id = request.GET.get('entry_id') or request.POST.get('entry_id')
    if entry_id and entries.exists():
        try:
            active_entry = entries.get(id=entry_id)
        except CalendarEntry.DoesNotExist:
            pass

    # 2) Determine selected date
    today = date.today()
    selected_date = today
    date_str = request.GET.get('date') or request.POST.get('date')
    if date_str:
        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = today

    day_obj = None

    # 3) Handle POST actions (click day / save notes)
    if active_entry and request.method == 'POST':
        action = request.POST.get('action')

        # Clicking a day cell: cycle status and select that date
        if action == 'click_day':
            # For click_day, we trust the posted date
            click_date_str = request.POST.get('date')
            try:
                selected_date = datetime.strptime(click_date_str, '%Y-%m-%d').date()
            except (TypeError, ValueError):
                selected_date = today

            day_obj, _created = CalendarDay.objects.get_or_create(
                entry=active_entry,
                date=selected_date,
            )
            if day_obj.status == 'none':
                day_obj.status = 'done'
            elif day_obj.status == 'done':
                day_obj.status = 'cancel'
            else:
                day_obj.status = 'none'
            day_obj.save()

            return redirect(f"/?entry_id={active_entry.id}&date={selected_date.isoformat()}")

        # Saving notes for selected_date
        if 'notes' in request.POST:
            notes = request.POST.get('notes', '')
            day_obj, _created = CalendarDay.objects.get_or_create(
                entry=active_entry,
                date=selected_date,
            )
            day_obj.notes = notes
            day_obj.save()

            return redirect(f"/?entry_id={active_entry.id}&date={selected_date.isoformat()}")

    # 4) Compute calendar weeks and attach status
    display_year = selected_date.year
    display_month = selected_date.month
    cal = calendar.Calendar(firstweekday=6)  # 6 = Sunday
    weeks_raw = cal.monthdatescalendar(display_year, display_month)
    month_label = selected_date.strftime('%B %Y').upper()

    # Build status map for visible dates
    weeks = []
    if active_entry:
        visible_dates = {d for w in weeks_raw for d in w}
        days_qs = CalendarDay.objects.filter(entry=active_entry, date__in=visible_dates)
        status_map = {d.date: d.status for d in days_qs}
    else:
        status_map = {}

    for w in weeks_raw:
        week = []
        for d in w:
            week.append({
                'date': d,
                'status': status_map.get(d, 'none'),
            })
        weeks.append(week)

    # 5) Day object for notes textarea (after potential POST redirects)
    if active_entry and day_obj is None:
        day_obj = CalendarDay.objects.filter(
            entry=active_entry,
            date=selected_date
        ).first()

    context = {
        'entries': entries,
        'active_entry': active_entry,
        'selected_date': selected_date,
        'today': today,
        'day': day_obj,  # used by notes textarea
        'display_year': display_year,
        'display_month': display_month,
        'weeks': weeks,  # list of weeks; each week is list of {'date', 'status'}
        'month_label': month_label,
    }
    return render(request, 'habits/home.html', context)


def create_calendar_entry(request):
    MAX_ENTRIES = 10
    entries = CalendarEntry.objects.all().order_by('order', 'id')
    count = entries.count()

    if count >= MAX_ENTRIES:
        return redirect('home')

    next_number = count + 1
    default_name = f"Tab {next_number}"

    new_entry = CalendarEntry.objects.create(
        name=default_name,
        order=count,
        user=None,
    )

    return redirect(f"/?entry_id={new_entry.id}")


def rename_calendar_entry(request, pk):
    entry = get_object_or_404(CalendarEntry, pk=pk)

    if request.method == 'POST':
        new_name = (request.POST.get('name') or '').strip()
        if new_name:
            entry.name = new_name[:100]
            entry.save()
        return redirect(f"/?entry_id={entry.id}")

    return render(request, 'habits/rename_entry.html', {'entry': entry})