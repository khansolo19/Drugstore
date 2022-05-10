from django.db import models
from django.urls import reverse

from account.models import MyUser


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ('name', )
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        
        return reverse('drugstore:product_list_by_category',
                       args=[self.slug, ])


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveSmallIntegerField(default=0)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name', )
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        
        return reverse('drugstore:product_details',
                       args=[self.slug, ])

    def save(self):
        self.slug = self.name.lower().replace(" ", '-')
        return super().save()


class Comment(models.Model):
    class Meta:
        db_table = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    user = models.ForeignKey('account.MyUser', related_name='comment', on_delete=models.CASCADE, blank=True)
    product = models.ForeignKey(Product, related_name='comment', on_delete=models.CASCADE, blank=True)
    text = models.TextField('Enter comment:', max_length=500)
    create_at = models.DateTimeField(auto_now_add=True)
    moder = models.BooleanField(default=False)

class Like(models.Model):
    user = models.ForeignKey(MyUser, related_name='likes', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='likes', on_delete=models.CASCADE)


    def str(self):
        return f'{self.user}:{self.product.name}'
