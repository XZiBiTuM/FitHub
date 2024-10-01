from django.contrib import admin
from .models import *
from django.db import transaction


@admin.register(ProductDetail)
class ProductDetailAdmin(admin.ModelAdmin):
    list_display = ('description', 'compound', 'expiration_date', 'number_of_servings', 'serving_weight')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'image')


@admin.action(description='Копировать выбранные продукты')
def copy_products(modeladmin, request, queryset):
    for obj in queryset:
        with transaction.atomic():
            if obj.product_detail:
                original_product_detail = obj.product_detail
                original_product_detail.pk = None
                original_product_detail.save()
                new_product_detail = original_product_detail
            else:
                new_product_detail = None

            new_images = []
            for image in obj.images.all():
                new_image = ProductImage.objects.get(pk=image.pk)
                new_image.pk = None
                new_image.save()
                new_images.append(new_image)

            obj.pk = None
            obj.product_detail = new_product_detail
            obj.save()

            for image in new_images:
                obj.images.add(image)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'price', 'weight_o', 'category', 'product_detail')
    filter_horizontal = ('images',)
    actions = [copy_products]


admin.site.register(Product, ProductAdmin)


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('category',)


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('id', 'products', 'total_price')


@admin.register(ProductQuantity)
class ProductQuantityAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'payment_status', 'date')
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_title', 'client_id', 'total_price', 'status', 'date')


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'city', 'street', 'house', 'comment')
