import os
import stripe
import environ
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Producst
from .serializers import ProductSerializer



# Initializing environment here
env = environ.Env()
environ.Env.read_env()

stripe_publishable_key = os.environ.get('STRIPE_PUBLISHABLE_KEY')
stripe_secret_key = os.environ.get('STRIPE_SECRET_KEY')


# Home page
# class Home(TemplateView):
#     template_name = 'index.html'
#     def get_context_data(self, **kwargs): # new
#         context = super().get_context_data(**kwargs)
#         context['key'] = settings.STRIPE_PUBLISHABLE_KEY
#         return context


# # For creating stripe checkout and sent to frontend
# def charge(request): # new
#     if request.method == 'POST':
#         charge = stripe.Charge.create(
#             amount=500,
#             currency='inr',
#             description='Django Stripe',
#             source=request.POST['stripeToken']
#         )
#         return render(request, 'success.html')




# creating stripe checkout here

@api_view(['POST'])
def Payment(request):

    #Get and post fro frontend side
    email = request.get['email']
    amount = request.get['amount']
    description = request.get['description']

    # creating order 
    
    order = Producst(email=email, amount=amount, description=description)
    order.save()

    session = stripe.checkout.Session.create(client_reference_id=request.user.id if request.user.is_authenticated else None,
              payment_method_types=['card'], line_items=[{
                'price_data': {
                    'currency': 'INR',
                    'product_data': {
                    'name': 'Django Stripe first payment',
                    },
                    'unit_amount': 10000,
                },
                'quantity': 1,
                }],
                 metadata={ "order_id":order.id},
                 mode='payment',
                 success_url='http://127.0.0.1:8000' + '/success.html',
                 cancel_url='http://127.0.0.1:8000' + '/cancel.html',
    ) 
    return Response({'id': session.id})







# For successful payment page
@api_view(['GET'])
def success(request):
    return render(request, 'success.html')



# For cancel payment page
@api_view(['GET'])
def cancel(request):
    return render(request, 'cancel.html')