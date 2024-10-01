from rest_framework import serializers
from .models import *


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetail
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    product_detail = ProductDetailSerializer()
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductSerializerProtein(serializers.ModelSerializer):
    product_detail = ProductDetailSerializer()
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductSerializerCreatine(serializers.ModelSerializer):
    product_detail = ProductDetailSerializer()
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductSerializerGainer(serializers.ModelSerializer):
    product_detail = ProductDetailSerializer()
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductSerializerSportBar(serializers.ModelSerializer):
    product_detail = ProductDetailSerializer()
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductProteinBrandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['brand']


class ProductCreatineBrandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['brand']


class ProductGainerBrandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['brand']


class ProductSportBarsBrandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['brand']


class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = '__all__'


class ProductQuantitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductQuantity
        fields = '__all__'


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = '__all__'


class OrderProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price']


class OrderItemSerializer(serializers.ModelSerializer):
    product = OrderProductsSerializer()

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    user = FormSerializer()
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'items', 'total_price', 'payment_status', 'date']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

