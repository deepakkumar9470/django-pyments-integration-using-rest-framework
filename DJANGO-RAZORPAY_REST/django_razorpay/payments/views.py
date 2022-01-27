import json
import os
import razorpay
import environ
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .serializers import OrderSerializer
from .models import Order
# Create your views here.


# @csrf_exempt
# def payment(request):
#     # For now we can use only simple data but if data post from frontend so we will 
#     # have to make post request of order
#     razor_client = razorpay.Client(auth =(settings.RAZOR_KEY_ID , settings.RAZOR_SECRET_KEY )) 
#     currency = 'INR'
#     amount = 60000  # Rs 600/-
#     response  = razor_client.order.create({'amount' : amount,'currency' :currency, 'payment_capture' :'1'})
#     print (response)
#     context = {'response' : response}

#     #*** In same ways we can do this also ****
#     #razorpay_order_id = response ['id']
#     # callback_url = 'payment/'

#     # for passing these details to client(forntend)
#     # context = {}
#     # context['razorpay_order_id'] = razorpay_order_id
#     # context['razorpay_key_id'] = settings.RAZOR_KEY_ID
#     # context['razorpay_amount'] = amount
#     # context['razorpay_currency'] = currency
#     # context['callback_url'] = callback_url

#     return render(request, 'payment.html',  context)

env = environ.Env()
environ.Env.read_env()

@api_view(['POST'])
def payment(request):

    amount = request.get['amount']
    name = request.get['name']

    razorpay_client = razorpay.Client(auth=(env('RAZOR_KEY_ID'), env('RAZOR_SECRET_KEY')))

    payment = razorpay_client.order.create({"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"})

    order = Order.objects.create(order_product=name, order_amount=amount,order_payment_id=payment['id'])

    serializer = OrderSerializer(order)

    data = {
        "payment": payment,
        "order": serializer.data
    }


    return Response('Order details :',data)




# For payments

@api_view(['POST'])
def success(request):
    # request.data is coming from frontend
    res = json.loads(request.data["response"])
    ord_id = ""
    raz_pay_id = ""
    raz_signature = ""

     # res.keys() will give us list of keys in res
    for key in res.keys():
        if key == 'razorpay_order_id':
            ord_id = res[key]
        elif key == 'razorpay_payment_id':
            raz_pay_id = res[key]
        elif key == 'razorpay_signature':
            raz_signature = res[key]
    return Response('Payment Successful')

    order = Order.objects.get(order_payment_id=ord_id)

    data = {
        'razorpay_order_id': ord_id,
        'razorpay_payment_id': raz_pay_id,
        'razorpay_signature': raz_signature
    }

    razorpay_client = razorpay.Client(auth=(env('RAZOR_KEY_ID'), env('RAZOR_SECRET_KEY')))

    check = razorpay_client.utility.verify_payment_signature(data)


    if check is not None:
        print("Redirect to error url or error page")
        return Response({'error': 'Something went wrong'})

    # if payment is successful that means check is None then we will turn isPaid=True
    order.isPaid = True
    order.save()

    res_data = {
        'message': 'Payment successfully received!'
    }

    return Response(res_data)





