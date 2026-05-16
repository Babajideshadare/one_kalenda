from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Extra user info, currently just the profile image.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'Profile for {self.user.username}'


class CalendarEntry(models.Model):
    """
    One calendar entry / habit (tab + sidebar entry).
    """
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='calendar_entries',
    )
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)  # tab order
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.name


class CalendarDay(models.Model):
    """
    One day for a given CalendarEntry with notes and a simple status.
    At most one CalendarDay per (entry, date).
    """
    entry = models.ForeignKey(
        CalendarEntry,
        on_delete=models.CASCADE,
        related_name='days',
    )
    date = models.DateField()
    notes = models.TextField(blank=True)
    status = models.CharField(
        max_length=10,
        choices=[
            ('none', 'No status'),
            ('done', 'Completed'),
            ('cancel', 'Cancelled'),
        ],
        default='none',
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('entry', 'date')
        ordering = ['-date']

    def __str__(self):
        return f'{self.entry.name} on {self.date} ({self.status})'