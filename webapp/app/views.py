from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

import requests
import json

# from local dir
from ownsecrets import BOT_TOKEN, PROVIDER_TOKEN
from app import data


def make_order(request):

    init_message_id = request.GET['init_message_id']

    services, services_json = data.get_services_with_json()

    return render(request,
        'make_order.html',
        context={
            'init_message_id': init_message_id,
            'services': services, 'services_json': services_json
        }
    )


def get_free_dates(request):

    free_dates = data.get_free_dates()

    return JsonResponse({
        'free_dates': free_dates
    })


def get_active_appointments(request):

    user_id = request.GET['user_id']

    return JsonResponse({
        'active_appointments': data.get_active_appointments(int(user_id))
    })


def create_invoice_link(request):

    description = request.GET['description']
    payload = request.GET['payload']
    prices = request.GET['prices']
    
    response = requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/createInvoiceLink', {
        'title': "Запись",
        'description': description,
        'payload': payload,
        'provider_token': PROVIDER_TOKEN,
        'currency': 'RUB',
        'prices': prices,
        'photo_url': 'https://user-images.githubusercontent.com/70770455/195734898-ac0a1171-be48-4773-b382-7f6430df9744.png',
        'need_name': True,
        'need_phone_number': True
        }
    )

    return HttpResponse(response.text)


def make_appointment(request):

    user_id = request.GET['user_id']
    services_ids = request.GET['services_ids']
    date_isoformat = request.GET['date_isoformat']
    time_isoformat = request.GET['time_isoformat']

    data.make_appointment(int(user_id), json.loads(services_ids), date_isoformat, time_isoformat)

    return HttpResponse('')
