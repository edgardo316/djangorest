from django.contrib.auth import models
from django.db.models import fields
from rest_framework import serializers
from core.models import Tag_Brand, Deals, store

class TagBrandSerializar(serializers.ModelSerializer):
    #serializador para objeto de tag_brand
    class Meta:
        models=Tag_Brand
        fields=('id', 'name', 'logo')
        read_only_Fields = ('id',)

class DealsSerializar(serializers.ModelSerializer):
    #serializador para objeto de tag_brand
    class Meta:
            models=Deals
            fields=('id', 'name', 'price')
            read_only_Fields = ('id',)

'''class StoreSerializar(serializers.ModelSerializer):
    #cerializa tienda
    Tag_Brand = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset = Deals.object.all()
    )
    Tag_Brand = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset = Tag_Brand.object.all()
    )

    class Meta:
        models = store
        fields = (
            'id','identifier', 'name', 'addres',
        )
        read_only_fields = ('id',)'''