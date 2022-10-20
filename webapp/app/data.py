from app.models import Service, Appointment

import datetime
import json

from typing import List, Dict


def get_free_dates() -> Dict[datetime.date.isoformat, List[datetime.time.isoformat]]:

	free_dates = dict()

	today = datetime.date.today()
	for i in range(7):
		date_isoformat = (today + datetime.timedelta(days=i)).isoformat()
		free_times = get_free_times(date_isoformat)
		if len(free_times) != 0:
			free_dates[date_isoformat] = free_times


	return free_dates


def get_free_times(date_isoformat: datetime.date.isoformat) -> List[datetime.time.isoformat]:

	free_times = list()

	hour_start = 11
	if date_isoformat == datetime.date.today().isoformat():
		hour_now = datetime.datetime.now().hour
		hour_start = hour_now if hour_now < hour_end - 1 and hour_now >= hour_start else hour_end 

	hour_end = 21
	for h in range(hour_start, hour_end):
		time_isoformat = datetime.time(h).isoformat()
		if not Appointment.objects.filter(date=date_isoformat, time=time_isoformat).exists():
			free_times.append(time_isoformat)


	return free_times


def make_appointment(user_id: int,
	services_ids: List[int],
	date_isoformat: datetime.date.isoformat,
	time_isoformat: datetime.time.isoformat):

	appointment = Appointment.objects.create(user_id=user_id, services=services_ids, date=date_isoformat, time=time_isoformat)
	appointment.save()


def get_active_appointments(user_id: int):

	active_appointments = Appointment.objects.filter(user_id=user_id, date__gte=datetime.date.today().isoformat()).order_by('date', 'time')
	active_appointments = [
		{
			'services_titles': [
				Service.objects.get(pk=service_id).title
				for service_id in active_appointment.services
			],
			'date': active_appointment.date,
			'time': active_appointment.time
		}
		for active_appointment in active_appointments
	]

	return active_appointments