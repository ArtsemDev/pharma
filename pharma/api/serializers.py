from rest_framework.serializers import ModelSerializer, Serializer, HyperlinkedModelSerializer
from rest_framework.fields import CharField, IntegerField

from shop.models import Category, Product


class CategorySerializer(ModelSerializer):
    slug = CharField(required=False)

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class ProductHyperLinkedModelSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'category', 'descr')


class CalculatorSerializer(Serializer):

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    height = IntegerField(min_value=1)
    width = IntegerField(min_value=1)
