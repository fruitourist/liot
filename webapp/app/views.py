from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

import requests
import json

# from local dir
from ownsecrets import BOT_TOKEN, PROVIDER_TOKEN
from security import is_valid_data
from app import data


def make_order(request):

    init_message_id = request.GET['init_message_id']
    
    if init_message_id == None:
        return HttpResponse("Bad Request", status=400)


    services, services_json = data.get_services_with_json()

    return render(request,
        'make_order.html',
        context={
            'init_message_id': int(init_message_id),
            'services': services, 'services_json': services_json
        }
    )


def get_free_dates(request):

    free_dates = data.get_free_dates()

    return JsonResponse({
        'free_dates': free_dates
    })


def get_active_appointments(request):

    bot_token = request.GET['bot_token']
    
    if bot_token != BOT_TOKEN:
        return HttpResponse("Forbidden", status=403)


    user_id = request.GET['user_id']

    if user_id == None:
        return HttpResponse("Bad Request", status=400)


    return JsonResponse({
        'active_appointments': data.get_active_appointments(int(user_id))
    })


def create_invoice_link(request):

    init_data_hash = request.GET['initDataHash']
    data_check_string = request.GET['dataCheckString']
    
    if not is_valid_data(init_data_hash, data_check_string):
        return HttpResponse("Unauthorized", status=401)


    description = request.GET['description']
    payload = request.GET['payload']
    prices = request.GET['prices']

    if description == None or payload == None or prices == None:
        return HttpResponse("Bad Request", status=400)

    
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

    bot_token = request.GET['bot_token']
    
    if bot_token != BOT_TOKEN:
        return HttpResponse("Forbidden", status=403)


    user_id = int(request.GET['user_id'])
    services_ids = json.loads(request.GET['services_ids'])
    date_isoformat = request.GET['date_isoformat']
    time_isoformat = request.GET['time_isoformat']

    if user_id == None or services_ids == None or date_isoformat == None or time_isoformat == None:
        return HttpResponse("Bad Request", status=400)


    data.make_appointment(user_id, services_ids, date_isoformat, time_isoformat)

    return HttpResponse("OK", status=200)
