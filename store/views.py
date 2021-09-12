from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from core.models import Tag_Brand, Deals, store
from store import serializer

class BaseStoreAttrs(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    #views base 
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        #retorna objetos para el usuario autenticado 
        return self.queryset.filter(user=self.request.user).order_by('mane')
    
    def perform(self, serializer):
        #crea un brand
        serializer.save(user=self.request.user)



class TagViewSet(BaseStoreAttrs):
    #manejar los tag en base de datos 
    queryset= Tag_Brand.objects.all()
    serializer_class = serializer.TagBrandSerializar

    
        
class DealsViewSet(BaseStoreAttrs):
    #manejar deals base de datos 
    queryset= Deals.objects.all()
    serializer_class = serializer.DealsSerializar

    
'''class StoreViewSet(viewsets.ModelViewSet):
    #maneja base datos tiendas 
    serializer_class = serializer.StoreSerializar
    queryset = store.objects.all()
    authentication_classes= (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        #retorna objetos para el tienda autenticado 
        return self.queryset.filter(user=self.request.user)'''    
