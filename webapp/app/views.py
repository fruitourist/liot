from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from app.models import Service
from django.core import serializers

import requests

# from local dir
from ownsecrets import BOT_TOKEN, PROVIDER_TOKEN
from app import data


def make_order(request):

	services = Service.objects.all()
	services_json = serializers.serialize('json', services)

	return render(request,
		'make_order.html',
		context={
			'init_message_id': request.GET['init_message_id'],
			'services': services, 'services_json': services_json
		}
	)


def create_invoice_link(request):
	
	response = requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/createInvoiceLink',
		{'title': "Запись",
		 'description': request.GET['description'],
		 'payload': request.GET['payload'],
		 'provider_token': PROVIDER_TOKEN,
		 'currency': 'RUB',
		 'prices': request.GET['prices'],
		 'photo_url': 'https://user-images.githubusercontent.com/70770455/195734898-ac0a1171-be48-4773-b382-7f6430df9744.png',
		 'need_name': True,
		 'need_phone_number': True,
		 'need_shipping_address': True}
	)

	return HttpResponse(response.text)


def get_free_dates(request):

	free_dates = data.get_free_dates()

	return JsonResponse({
		'free_dates': free_dates
	})


def make_appointment(request):

	data.make_appointment(request.GET['user_id'], list(request.GET['services_ids']), request.GET['date_isoformat'], request.GET['time_isoformat'])

	return HttpResponse('')


def get_active_appointments(request):

	return JsonResponse({
		'active_appointments': data.get_active_appointments(request.GET['user_id'])
	})