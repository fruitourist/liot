from django.http import HttpResponse
from django.shortcuts import render

import requests

# from local dir
from ownsecrets import BOT_TOKEN, PROVIDER_TOKEN


def make_order(request):
	return render(request,
		'app/make_order.html',
		context={'init_message_id': request.GET['init_message_id']}
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