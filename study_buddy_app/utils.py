from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Event

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	def formatday(self, day, events):
		events_per_day = events.filter(start_time__day=day)
		d = ''
		for event in events_per_day:
			new_start_time = event.start_time+timedelta(hours=-5) + timedelta(minutes=4)
			new_end_time = event.end_time+timedelta(hours=-5) + timedelta(minutes=4)
			d += f'<li><div class="fw-bold">{event.title}</div>{new_start_time.strftime("%I:%M %p")}-{new_end_time.strftime("%I:%M %p")}</li>'

		if day != 0:
			return f"<td><span class='date'>{day}</span><ul>{d} </div></li></ul>"
		return '<td></td>'

	# formats a week as a tr 
	def formatweek(self, theweek, events):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events)
		return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, user, withyear=True):
		events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month, users__username=user.username)

		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, events)}\n'
		return cal