from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from . import views
from .views import *

router = DefaultRouter()
router.register(r'product_details', ProductDetailViewSet)
router.register(r'product_images', ProductImageViewSet)
router.register(r'product_categories', ProductCategoryViewSet)
router.register(r'proteins', ProductProteinViewSet, basename='proteins')
router.register(r'creatine', ProductCreatineViewSet, basename='creatine')
router.register(r'gainer', ProductGainerViewSet, basename='gainer')
router.register(r'sport_bars', ProductSportBarsViewSet, basename='sport_bars')
router.register(r'products', ProductViewSet)
router.register(r'proteins_brands', ProductProteinBrandViewSet, basename='proteins_brands')
router.register(r'creatine_brands', ProductCreatineBrandViewSet, basename='creatine_brands')
router.register(r'gainer_brands', ProductGainerBrandViewSet, basename='gainer_brands')
router.register(r'sport_bars_brands', ProductSportBarsBrandViewSet, basename='sport_bars_brands')
router.register(r'baskets', BasketViewSet)
router.register(r'product_quantities', ProductQuantityViewSet)
router.register(r'forms', FormViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order_items', OrderItemViewSet)
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('protein_catalog/', views.protein_catalog, name='protein_catalog'),
    path('creatine_catalog/', views.creatine_catalog, name='creatine_catalog'),
    path('gainer_catalog/', views.gainer_catalog, name='gainer_catalog'),
    path('sport_bars_catalog/', views.sport_bars_catalog, name='sport_bars_catalog'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('check_stock/', views.check_stock, name='check_stock'),
    path('order/', views.order, name='order'),
    path('order_success/', views.order_success, name='order_success'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update_cart_quantity/<int:product_id>/<str:action>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('', views.main, name='main'),

    path('products/', product_create, name='product-create'),
    path('product/<int:id>/', ProductIDViewSet.as_view(), name='product-id'),
    path('proteins/', product_create_protein, name='product-create_protein'),
    path('creatines/', product_create_creatine, name='product-create_creatine'),
    path('gainers/', product_create_gainer, name='product-create_gainer'),
    path('sport_bars/', product_create_sport_bar, name='product-create_sport_bar'),
    path('proteins_brands/', product_create_protein_brands, name='product-create_protein_brands'),
    path('creatines_brands/', product_create_creatine_brands, name='product-create_creatine_brands'),
    path('gainers_brands/', product_create_gainer_brands, name='product-create_gainer_brands'),
    path('sport_bars_brands/', product_create_sport_bars_brands, name='product-create_sport_bar_brands'),
    path('product-details/', product_detail_create, name='product-detail-create'),
    path('product-images/', product_image_create, name='product-image-create'),
    path('product-categories/', product_category_create, name='product-category-create'),
    path('baskets/', basket_create, name='basket-create'),
    path('product-quantities/', product_quantity_create, name='product-quantity-create'),
    path('forms/', form_create, name='form-create'),
    path('orders/', order_create, name='order-create'),
    path('order-items/', order_item_create, name='order-item-create'),
    path('payments/', payment_create, name='payment-create'),
    path('api/', include(router.urls)),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
