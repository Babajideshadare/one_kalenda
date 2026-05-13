from django.shortcuts import render, redirect
from .models import CalendarEntry


def home(request):
    """
    Home page: show layout and a row of tabs for CalendarEntry objects.
    The active tab can be chosen via ?entry_id=...; otherwise first entry.
    """
    entries = CalendarEntry.objects.all().order_by('order', 'id')
    active_entry = entries.first() if entries else None

    entry_id = request.GET.get('entry_id')
    if entry_id and entries.exists():
        try:
            active_entry = entries.get(id=entry_id)
        except CalendarEntry.DoesNotExist:
            pass

    context = {
        'entries': entries,
        'active_entry': active_entry,
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

    # Do not create more than MAX_ENTRIES
    if count >= MAX_ENTRIES:
        return redirect('home')

    # Default name: 'Tab N' where N = total entries + 1
    next_number = count + 1
    default_name = f"Tab {next_number}"

    new_entry = CalendarEntry.objects.create(
        name=default_name,
        order=count,   # append at the end
        user=None,     # will use real user when we add auth
    )

    # Redirect back to home and mark this new entry as active via query param
    return redirect(f"/?entry_id={new_entry.id}")