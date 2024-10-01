from django.db import models
from .validators import validate_image_size
from django.utils.text import slugify


class ProductDetail(models.Model):
    description = models.TextField(verbose_name="Полное описание")
    compound = models.TextField(verbose_name="Состав")
    expiration_date = models.SmallIntegerField(verbose_name="Срок годности (мес.)")
    number_of_servings = models.IntegerField(null=True, blank=True, verbose_name="Количество порций")
    serving_weight = models.IntegerField(null=True, blank=True, verbose_name="Вес порции (г.)")

    class Meta:
        verbose_name = "Деталь продукта"
        verbose_name_plural = "Детали продуктов"

    def __str__(self):
        return self.description


def user_directory_path(instance, filename):
    title = instance.title
    slug = slugify(title)
    return 'products/{0}/{1}.png'.format(slug, filename)


class ProductImage(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    image = models.ImageField(upload_to=user_directory_path, max_length=255, validators=[validate_image_size], verbose_name="Изображение")

    class Meta:
        verbose_name = "Изображение продукта"
        verbose_name_plural = "Изображения продуктов"

    def __str__(self):
        return self.title


class ProductCategory(models.Model):
    category = models.CharField(max_length=255, verbose_name='Категория')

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f'{self.category}'


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    brand = models.CharField(max_length=255, null=True, blank=True, verbose_name="Бренд")
    quantity = models.IntegerField(verbose_name="Количество (шт.)")
    short_description = models.CharField(max_length=255, verbose_name='Короткое описание')
    price = models.PositiveIntegerField(verbose_name='Цена')
    weight_o = models.PositiveIntegerField(verbose_name='Вес (г.)')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='Категория')
    images = models.ManyToManyField(ProductImage, verbose_name="Изображения")
    product_detail = models.ForeignKey(ProductDetail, on_delete=models.CASCADE, verbose_name="Деталь продукта", related_name='products')

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.title


class Basket(models.Model):
    products = models.BigIntegerField(null=True, blank=True, verbose_name="Продукты")
    total_price = models.BigIntegerField(verbose_name="Общая цена")

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return str(self.id)


class ProductQuantity(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Вес продукта")
    quantity = models.SmallIntegerField(verbose_name="Количество")

    class Meta:
        verbose_name = "Количество продукта"
        verbose_name_plural = "Количество продуктов"

    def __str__(self):
        return f'{self.product.title} - {self.quantity}'


class Form(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    email = models.CharField(max_length=255, verbose_name="Электронная почта")
    phone_number = models.CharField(max_length=255, verbose_name="Номер телефона")
    city = models.CharField(max_length=255, verbose_name="Город")
    street = models.CharField(max_length=255, verbose_name="Улица")
    house = models.CharField(max_length=255, verbose_name="Дом")
    comment = models.TextField(null=True, blank=True, verbose_name="Комментарий")

    class Meta:
        verbose_name = "Форма"
        verbose_name_plural = "Формы"

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(Form, on_delete=models.CASCADE, verbose_name="Пользователь")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая цена")
    payment_status = models.CharField(max_length=255, verbose_name="Статус оплаты")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f'Order {self.id} by {self.user}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    price = models.PositiveIntegerField(verbose_name="Цена")

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"

    def __str__(self):
        return f'{self.product.title} ({self.quantity})'


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    product_title = models.CharField(max_length=255, verbose_name="Название продукта")
    client_id = models.BigIntegerField(verbose_name="ID клиента")
    total_price = models.BigIntegerField(verbose_name="Общая цена")
    status = models.BigIntegerField(verbose_name="Статус")
    date = models.BigIntegerField(verbose_name="Дата")

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"

    def __str__(self):
        return str(self.id)
