import os
import base64
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Tenant, RentPayment


def home(request):
    tenants = Tenant.objects.all()
    return render(request, 'payments/home.html', {'tenants': tenants})


def get_mpesa_token():
    key = os.environ.get('')
    secret = os.environ.get('MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjEwNjI4MDkyNDA4')
    if not key or not secret:
        raise RuntimeError('MPESA credentials missing')
    auth = base64.b64encode(f"{key}:{secret}".encode()).decode()
    url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    resp = requests.get(url, headers={'Authorization': f'Basic {auth}'})
    resp.raise_for_status()
    return resp.json()['access_token']


def start_payment(request):
    if request.method == 'POST':
        tenant_id = request.POST.get('tenant')
        amount = request.POST.get('amount')
        tenant = Tenant.objects.get(pk=tenant_id)
        token = get_mpesa_token()
        shortcode = os.environ.get('174379')
        passkey = os.environ.get('GZA6SLZtAG99AF5CjIxeygrKF1trHgAO4SBLXnDgh1gAAJFF')
        callback = request.build_absolute_uri('/mpesa-callback/')
        import datetime
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode(f"{shortcode}{passkey}{timestamp}".encode()).decode()
        payload = {
            "BusinessShortCode": 174379,
            "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjEwNjI4MDkyNDA4", 
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": "254740676371",
            "PartyB": shortcode,
            "PhoneNumber": 254740676371,
            "CallBackURL": os.environ.get('MPESA_CALLBACK_URL'),
            "AccountReference": f"rent-{tenant.id}",
            "TransactionDesc": "Rent payment"
        }
        resp = requests.post(
            'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest',
            json=payload,
            headers={'Authorization': f'Bearer {token}'}
        )
        data = resp.json()
        payment = RentPayment.objects.create(
            tenant=tenant,
            amount=amount,
            mpesa_checkout_request_id=data.get('CheckoutRequestID', '')
        )
        return JsonResponse(data)
    return HttpResponse(status=405)


@csrf_exempt
def mpesa_callback(request):
    # Safaricom will POST payment result here
    # For simplicity just mark payment paid if successful
    data = request.body.decode('utf-8')
    # In real usage parse JSON and find CheckoutRequestID and result code
    # Here we'll print and return 200
    print('MPESA CALLBACK', data)
    return HttpResponse('OK')
