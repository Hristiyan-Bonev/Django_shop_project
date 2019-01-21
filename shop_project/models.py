import os
from django.db import models
from django.contrib.auth.models import  AbstractUser
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _


class CustomUser(AbstractUser):
    first_name = models.CharField(_('first name'), max_length=30)
    email = models.EmailField(_('email address'), max_length=150, unique=True)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    delivery_address = models.CharField(max_length=50)

    def __str__(self):
        return self.username


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    category = models.ManyToManyField(Category)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.name

    def get_item_image(self, width=150, height=150):
        return mark_safe('<img src="{}" width="{}" height="{}" />'.format(self.image.url, width, height))
        #TODO : Add default image

    def get_item_thumbnail(self, width=75, height=75):
        return mark_safe('<img src="{}" width="{}" height="{}" />'.format(self.image.url, width, height))

    get_item_image.short_description = 'Image preview'


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    date_of_issue = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField('shop_project.CustomUser', on_delete=models.CASCADE)
    delivery_address = models.CharField(max_length=100)
    order_items = models.ManyToManyField(Item)
    total_price = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return 'Order #{}'.format(self.order_id)