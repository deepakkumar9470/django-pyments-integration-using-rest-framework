import os
import environ
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth import authenticate , login as auth_login
from .models import Transaction
from .paytm import generate_checksum, verify_checksum


from .models import Transaction
from .serializers import TransactionSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import Checksum


env = environ.Env()
environ.Env.read_env()


paytm_merchant_id = os.environ.get('PAYTM_MERCHANT_ID')
paytm_secret_key = os.environ.get('PAYTM_SECRET_KEY')
paytm_website = os.environ.get('PAYTM_WEBSITE')
paytm_channle_id = os.environ.get('PAYTM_CHANNEL_ID')
paytm_industry_type_id = os.environ.get('PAYTM_INDUSTRY_TYPE_ID')



#initializing payment here
@api_view(['POST'])
def initiate_payment(request):

    amount = request.data['amount']
    name = request.data['name']
    email = request.data['email']

    paytm_order = Transaction.objects.create(product_name=name,order_amount=amount,user_email=email,)

    serializer = TransactionSerializer(paytm_order)

    # we have to send the param_dict to the frontend
    # these credentials will be passed to paytm order processor to verify the business account
    param_dict = {
        'MID': env('MERCHANTID'),
        'ORDER_ID': str(order.id),
        'TXN_AMOUNT': str(amount),
        'CUST_ID': email,
        'INDUSTRY_TYPE_ID': 'Retail',
        'WEBSITE': 'WEBSTAGING',
        'CHANNEL_ID': 'WEB',
        'CALLBACK_URL': 'http://127.0.0.1:8000/success/',
        # this is the url of handlepayment function, paytm will send a POST request to the fuction associated with this CALLBACK_URL
    }


    # create new checksum (unique hashed string) using our merchant key with every paytm payment
    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, env('PAYTM_SECRET_KEY'))
    # send the dictionary with all the credentials to the frontend
    return Response({'param_dict': param_dict})

    
    


# Callback view after all transaction ok

@api_view(['POST'])              
def payment_handle(request):

    checksum = ""

    # this post request from paytm
    form = request.POST

    
    response_dict = {}
    order = None 

    for i in form.keys():
        response_dict[i] = form[i]

        if i == 'CHECKSUMHASH':
            checksum = form[i]

        if i == 'ORDERID':
            # we will get an order with id==ORDERID to turn 
            # isPaid=True when payment is successful

            order = Transaction.objects.get(id = form[i]) 

    verify = Checksum.verify_checksum(response_dict, env('PAYTM_SECRET_KEY'), checksum)  

    if verify:
        # response code 01 shows transaction is successful
        if response_dict['RESPCODE'] == '01':

            print('order successful')
            # after successfull payment we will make isPaid=True and will save the order
            order.isPaid = True
            order.save()
            # we will render a template to display the payment status
            return render(request, 'payment.html', {'response': response_dict})

        else:
            print('order was not successful because' + response_dict['RESPMSG'])
            return render(request, 'payment.html', {'response': response_dict})    



    