# Rest Imports
from rest_framework import serializers

# Django Imports
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext_lazy

# Local Imports
from .models import ServiceOrder


User = get_user_model()


class LoginSerializers(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(
        label=ugettext_lazy("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        max_length=128,
        write_only=True
    )

    def validate(self, data):
        username = data.get('email')
        password = data.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data


class ServiceOrderSerializer(serializers.Serializer):
    
    class Meta:
        model = ServiceOrder
        fields = ('__all__')