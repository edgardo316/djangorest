from user.serializers import UserSerializer, AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import generics, authentication, permissions

from rest_framework.settings import api_settings

class CreateUserView(generics.CreateAPIView):
    # crea un usuario en el sistema 
    serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
    #crea nuevo auth token para usuario 
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserVIew(generics.RetrieveDestroyAPIView):
    #manejar el usuario autenticado 
    serializer_class=UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes=(permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

