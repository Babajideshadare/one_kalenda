from datetime import date

from django.shortcuts import render, redirect
from .models import CalendarEntry, CalendarDay


def home(request):
    """
    Home page: show layout, entries as tabs, and for an active entry
    show a calendar + Daily Notes for a single date (today for now).

    POST: save notes for the active entry + selected date.
    GET: display current notes.
    """
    entries = CalendarEntry.objects.all().order_by('order', 'id')
    active_entry = entries.first() if entries else None

    # Determine active entry id from GET or POST
    entry_id = request.GET.get('entry_id') or request.POST.get('entry_id')
    if entry_id and entries.exists():
        try:
            active_entry = entries.get(id=entry_id)
        except CalendarEntry.DoesNotExist:
            pass

    # For now, use today's date as the selected date
    selected_date = date.today()
    day = None

    if active_entry:
        # Handle saving notes (POST)
        if request.method == 'POST':
            notes = request.POST.get('notes', '')
            day, _created = CalendarDay.objects.get_or_create(
                entry=active_entry,
                date=selected_date,
            )
            day.notes = notes
            day.save()
            # Redirect to avoid form re-submission and keep active entry
            return redirect(f"/?entry_id={active_entry.id}")

        # On GET: fetch existing day if any
        day = CalendarDay.objects.filter(
            entry=active_entry,
            date=selected_date
        ).first()

    context = {
        'entries': entries,
        'active_entry': active_entry,
        'selected_date': selected_date,
        'day': day,
    }
    return render(request, 'habits/home.html', context)


def create_calendar_entry(request):
    """
    Create a new CalendarEntry (tab) with a default name like 'Tab 1', 'Tab 2', ...
    Limit to a maximum of 10 entries. After creation, redirect back to home and
    make the new entry active.
    """
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
        user=None,   # will be set when auth is added
    )

    return redirect(f"/?entry_id={new_entry.id}")