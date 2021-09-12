from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

class UserSerializer (serializers.ModelSerializer):
    #serializador para el objeto usuario 
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password':{'write_only': True, 'min_length': 5}}

    def create(self, validate_data):
        #retornar usuario clave encriptada
        return get_user_model().objects.create_user(**validate_data)
    
    def update(self,instance ,validated_data):
        #acualiza usuario 
        password= validated_data.pop('password', None)
        user=super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    #serializador para la autenticacion de usuario 
    email=serializers.CharField()
    password=serializers.CharField(
        style={'imput:type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        #validar y autenticar usuario 
        email=attrs.get('email')
        password= attrs.get('password')

        user=authenticate(
            request=self.context.get('request'),
            username=email,
            password= password
        )
        if not user:
            msg = _('Unable to authenticate with provided credetials')
            raise serializers.ValidationError(msg='authorization')

            attrs['user'] = user
            return attrs

