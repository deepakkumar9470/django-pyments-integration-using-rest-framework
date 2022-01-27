

from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    order_date = serializers.DateTimeField(format="%d %B %Y %I:%M %p")

    class Meta:
        model = Transaction
        fields = "__all__"
      