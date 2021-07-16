from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse

User = get_user_model()

def get_product_url(obj,viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model':ct_model, 'slug': obj.slug})
    

class LatestProductsManager:

    @staticmethod
    def get_products_for_main_page(*args,**kwargs):
        products = []
        ct_models = ContentType.objects.filter(model_in=args)
        for ct_model in ct_models:
            model_products= ct_model.model_class().base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        return products


class LatestProducts:
    objects = LatestProductsManager()

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя категории ")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name="Имя продукта")
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Фото продукта')
    description = models.TextField(verbose_name="Описание", null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return self.title


class SmartPhone(Product):
    diagonal = models.CharField(max_length=255, verbose_name="Диагональ")
    display = models.CharField(max_length=255, verbose_name="Тип дисплея")
    matrix_type = models.CharField(max_length=255, verbose_name="Тип матрицы")
    screen_resolution = models.CharField(max_length=255, verbose_name="Розрешение екрана")
    ram = models.CharField(max_length=255, verbose_name="Оперативная память")
    memory = models.CharField(max_length=255, verbose_name="Встроеная память")
    cpu = models.CharField(max_length=255, verbose_name="Процесор")
    front_cam = models.CharField(max_length=255, verbose_name="Фронтальная камера")
    main_cam = models.CharField(max_length=255, verbose_name="Основная камера")
    battery_capacity = models.CharField(max_length=255, verbose_name="Емкость акамулятора")
    number_of_SIM = models.CharField(max_length=255, verbose_name="Количесно сим-карт")
    protection = models.CharField(max_length=255, verbose_name="Тип защити", null=True, blank=True)
    OS = models.CharField(max_length=255, verbose_name="Тип операционной системы")
    NFC = models.BooleanField(verbose_name='NFC')

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')

class SmartWatch(Product):
    diagonal = models.CharField(max_length=255, verbose_name="Диагональ")
    display = models.CharField(max_length=255, verbose_name="Тип дисплея")
    matrix_type = models.CharField(max_length=255, verbose_name="Тип матрицы")
    battery_capacity = models.CharField(max_length=255, verbose_name="Емкость акамулятора")
    protection = models.CharField(max_length=255, verbose_name="Тип защити", null=True, blank=True)

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Accessory(Product):
    pass

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class SmartHouse(Product):
    pass

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)
    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', "object_id")
    qty = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return "Продукт {}".format(self.product.title)


class Cart(models.Model):
    owner = models.ForeignKey('Customer', verbose_name="Владелец", on_delete=models.CASCADE)
    product = models.ManyToManyField(CartProduct, blank=True, related_name='related_card')
    total_products = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, verbose_name='Номер телефона')
    adress = models.CharField(max_length=255, verbose_name='Адрес')
    email = models.EmailField()

    def __str__(self):
        return "Покупатель: {} {}".format(self.user.first_name, self.user.last_name)
