from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.template.defaultfilters import slugify

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, blank=False)
    #Changes by Gayathri Dated: 16/11/2022
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
    #Changes by Gayathri Dated: 16/11/2022
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return str(self.id)

    #Changes by Tongmei Dated: 17/11/2022
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    #Changes by Gayathri Dated: 17/11/2022
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
 

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    #Changes by Gayathri Dated: 17/11/2022
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total



class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address 

#Changes by Tongmei Dated: 24/11/2022
class Category(models.Model):
    category_title = models.CharField(max_length=200)
    category_image = models.ImageField(upload_to="category")
    category_slug = models.SlugField(max_length=200, default=1)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_title 

    @property
    def imageURL(self):
        try:
            url = self.category_image.url
        except:
            url = ''
        
        return url

    @property    
    def get_photo_url(self):
        if self.category_image and hasattr(self.category_image, 'url'):
            return self.category_image.url
        else:
            return "/static/images/category/TV.png"

class Subcategory(models.Model):
    subcategory_title = models.CharField(max_length=200)
    subcategory_category = models.ForeignKey(
        Category, default=1, verbose_name="Category", on_delete=models.SET_DEFAULT)

    class Meta:
        verbose_name_plural = "Subcategories"

    def __str__(self):
        return self.subcategory_title

class ProductNew(models.Model):

    product_title = models.CharField(max_length=200)
    product_image = models.ImageField(null=True, blank=True)
    product_base_price = models.DecimalField(max_digits=12, decimal_places=2)
    product_description = models.TextField()
    product_slug = models.SlugField(max_length=200, default=1)
    product_subcategory = models.ForeignKey(
    Subcategory, default=1, verbose_name="Subcategories", on_delete=models.SET_DEFAULT)
    product_available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.product_title

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        
        return url