from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from .models import Producst



class ProductSerializer(serializers.ModelSerializer):
    order_date = serializers.DateTimeField(format="%d %B %Y %I:%M %p")

    class Meta:
        model = Producst
        fields = "__all__"
        
