import calendar
from datetime import date, datetime

from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import CalendarEntry, CalendarDay, UserProfile, PublicComment
from .forms import RegisterForm, EditProfileForm, PublicCommentForm


@login_required
def home(request):
    """
    Home page: layout + sidebar + tabs.
    """
    # Only this user's entries
    entries = CalendarEntry.objects.filter(user=request.user).order_by('order', 'id')
    active_entry = entries.first() if entries else None

    # 1) Determine active entry
    entry_id = request.GET.get('entry_id') or request.POST.get('entry_id')
    if entry_id and entries.exists():
        try:
            active_entry = entries.get(id=entry_id)
        except CalendarEntry.DoesNotExist:
            active_entry = entries.first() if entries else None

    # Use local date in your configured TIME_ZONE
    today = timezone.localdate()

    # 2) Determine selected date
    selected_date = today
    date_str = request.GET.get('date')
    if date_str:
        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = today

    day_obj = None

    # 3) Handle POST actions (click day / save notes)
    if active_entry and request.method == 'POST':
        action = request.POST.get('action')

        if action == 'click_day':
            clicked_str = request.POST.get('date')
            try:
                clicked_date = datetime.strptime(clicked_str, '%Y-%m-%d').date()
            except (TypeError, ValueError):
                clicked_date = selected_date

            if clicked_date != selected_date:
                return redirect(f"/?entry_id={active_entry.id}&date={clicked_date.isoformat()}")

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

        if 'notes' in request.POST:
            target_str = request.POST.get('date')
            try:
                target_date = datetime.strptime(target_str, '%Y-%m-%d').date()
            except (TypeError, ValueError):
                target_date = selected_date

            day_obj, _created = CalendarDay.objects.get_or_create(
                entry=active_entry,
                date=target_date,
            )
            day_obj.notes = request.POST.get('notes', '')
            day_obj.save()

            return redirect(f"/?entry_id={active_entry.id}&date={target_date.isoformat()}")

    # 4) Prev/next month dates
    first_of_month = selected_date.replace(day=1)

    if first_of_month.month == 1:
        prev_month_year = first_of_month.year - 1
        prev_month = 12
    else:
        prev_month_year = first_of_month.year
        prev_month = first_of_month.month - 1
    prev_month_date = date(prev_month_year, prev_month, 1)

    if first_of_month.month == 12:
        next_month_year = first_of_month.year + 1
        next_month = 1
    else:
        next_month_year = first_of_month.year
        next_month = first_of_month.month + 1
    next_month_date = date(next_month_year, next_month, 1)

    # 5) Calendar weeks + classes
    display_year = selected_date.year
    display_month = selected_date.month
    cal = calendar.Calendar(firstweekday=6)
    weeks_raw = cal.monthdatescalendar(display_year, display_month)
    month_label = selected_date.strftime('%B %Y').upper()

    weeks = []
    if active_entry:
        visible_dates = {d for w in weeks_raw for d in w}
        days_qs = CalendarDay.objects.filter(entry=active_entry, date__in=visible_dates)
        status_map = {d.date: d.status for d in days_qs}
    else:
        status_map = {}

    today = timezone.localdate()
    for w in weeks_raw:
        row = []
        for d in w:
            classes = ['day']
            if d.month != display_month:
                classes.append('muted')
            elif d == selected_date:
                classes.append('selected')
            elif d == today:
                classes.append('today')
            status = status_map.get(d, 'none')
            if status == 'done':
                classes.append('day-done')
            elif status == 'cancel':
                classes.append('day-cancel')
            row.append({'date': d, 'classes': ' '.join(classes)})
        weeks.append(row)

    if active_entry and day_obj is None:
        day_obj = CalendarDay.objects.filter(entry=active_entry, date=selected_date).first()

    context = {
        'entries': entries,
        'active_entry': active_entry,
        'selected_date': selected_date,
        'today': today,
        'day': day_obj,
        'display_year': display_year,
        'display_month': display_month,
        'weeks': weeks,
        'month_label': month_label,
        'prev_month_date': prev_month_date,
        'next_month_date': next_month_date,
    }
    return render(request, 'habits/home.html', context)


@login_required
def create_calendar_entry(request):
    MAX_ENTRIES = 10
    entries = CalendarEntry.objects.filter(user=request.user).order_by('order', 'id')
    count = entries.count()

    if count >= MAX_ENTRIES:
        return redirect('home')

    next_number = count + 1
    default_name = f"Tab {next_number}"

    new_entry = CalendarEntry.objects.create(
        name=default_name,
        order=count,
        user=request.user,
    )

    return redirect(f"/?entry_id={new_entry.id}")


@login_required
def rename_calendar_entry(request, pk):
    entry = get_object_or_404(CalendarEntry, pk=pk, user=request.user)

    if request.method == 'POST':
        new_name = (request.POST.get('name') or '').strip()
        if new_name:
            entry.name = new_name[:100]
            entry.save()
        return redirect(f"/?entry_id={entry.id}")

    return render(request, 'habits/rename_entry.html', {'entry': entry})


@login_required
def delete_calendar_entry(request, pk):
    entry = get_object_or_404(CalendarEntry, pk=pk, user=request.user)

    if request.method == 'POST':
        entry.delete()
        return redirect('home')

    return render(request, 'habits/delete_entry.html', {'entry': entry})


@login_required
def public_comments(request):
    """
    Shared public comments page visible to all logged-in users.
    """
    entries = CalendarEntry.objects.filter(user=request.user).order_by('order', 'id')
    active_entry = entries.first() if entries else None

    if request.method == 'POST':
        form = PublicCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            return redirect('public_comments')
    else:
        form = PublicCommentForm()

    comments = PublicComment.objects.select_related('user').all()[:100]

    context = {
        'entries': entries,
        'active_entry': active_entry,
        'form': form,
        'comments': comments,
    }
    return render(request, 'habits/public_comments.html', context)


@login_required
def pin_public_comment(request, pk):
    """
    Pin or unpin a public comment.

    - If action=pin and fewer than 5 comments are pinned, pin it.
    - If action=unpin, unpin it.
    - Limit: max 5 pinned comments in total.
    """
    comment = get_object_or_404(PublicComment, pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'pin':
            if not comment.is_pinned:
                pinned_count = PublicComment.objects.filter(is_pinned=True).count()
                if pinned_count >= 5:
                    messages.error(request, "You can only pin up to 5 comments.")
                else:
                    comment.is_pinned = True
                    comment.pinned_at = timezone.now()
                    comment.save()
        elif action == 'unpin':
            if comment.is_pinned:
                comment.is_pinned = False
                comment.pinned_at = None
                comment.save()

    return redirect('public_comments')


@login_required
def edit_public_comment(request, pk):
    """
    Edit a public comment. Only the author can edit.
    """
    comment = get_object_or_404(PublicComment, pk=pk, user=request.user)

    entries = CalendarEntry.objects.filter(user=request.user).order_by('order', 'id')
    active_entry = entries.first() if entries else None

    if request.method == 'POST':
        form = PublicCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('public_comments')
    else:
        form = PublicCommentForm(instance=comment)

    context = {
        'entries': entries,
        'active_entry': active_entry,
        'form': form,
        'comment': comment,
    }
    return render(request, 'habits/edit_comment.html', context)


@login_required
def delete_public_comment(request, pk):
    """
    Delete a public comment. Only the author can delete.
    """
    comment = get_object_or_404(PublicComment, pk=pk, user=request.user)

    entries = CalendarEntry.objects.filter(user=request.user).order_by('order', 'id')
    active_entry = entries.first() if entries else None

    if request.method == 'POST':
        comment.delete()
        return redirect('public_comments')

    context = {
        'entries': entries,
        'active_entry': active_entry,
        'comment': comment,
    }
    return render(request, 'habits/delete_comment.html', context)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})


def logout_view(request):
    auth_logout(request)
    return redirect('login')


@login_required
def profile(request):
    entries = CalendarEntry.objects.filter(user=request.user).order_by('order', 'id')
    active_entry = entries.first() if entries else None

    avatar_url = None
    try:
        profile_obj = request.user.profile
        if profile_obj.avatar:
            avatar_url = profile_obj.avatar.url
    except UserProfile.DoesNotExist:
        pass

    context = {
        'entries': entries,
        'active_entry': active_entry,
        'avatar_url': avatar_url,
    }
    return render(request, 'habits/profile.html', context)


@login_required
def edit_profile(request):
    entries = CalendarEntry.objects.filter(user=request.user).order_by('order', 'id')
    active_entry = entries.first() if entries else None

    avatar_url = None
    try:
        profile_obj = request.user.profile
        if profile_obj.avatar:
            avatar_url = profile_obj.avatar.url
    except UserProfile.DoesNotExist:
        pass

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            user = form.save()
            if form.cleaned_data.get('new_password1'):
                update_session_auth_hash(request, user)
            return redirect('profile')
    else:
        form = EditProfileForm(user=request.user)

    context = {
        'entries': entries,
        'active_entry': active_entry,
        'form': form,
        'avatar_url': avatar_url,
    }
    return render(request, 'habits/edit_profile.html', context)