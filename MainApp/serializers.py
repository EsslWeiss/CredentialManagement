from rest_framework.serializers import ModelSerializer
from .models import Customer


class CustomerSerializer(ModelSerializer):

    class Meta:
        model = Customer
        fields = ('pk', 'first_name', 'last_name', 'email', 'phone', 'address', 'description')

