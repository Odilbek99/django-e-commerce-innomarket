from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.contrib.auth.models import User


# Create your models here.
class Slider(models.Model):
    DISCOUNT_DEAL = (
        ('HOT DEALS','HOT DEALS'),
        ('New Arraivels','New Arraivels'),
    )

    image = models.ImageField(upload_to='slider_imgs')
    discount_deal = models.CharField(choices=DISCOUNT_DEAL, max_length=200)
    sale = models.IntegerField()
    brand_name = models.CharField(max_length=200)
    discount = models.IntegerField()
    link = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.brand_name

class BannerArea(models.Model):

    image = models.ImageField(upload_to='banner_imgs')
    discount_deal = models.CharField(max_length=255)  
    quote = models.CharField(max_length=255)  
    discount = models.IntegerField()
    link = models.CharField(max_length=255, null=True)
    
    def __str__(self) -> str:
        return self.quote

class MainCategoty(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

class Category(models.Model):
    main_category = models.ForeignKey(MainCategoty, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    
    def __str__(self) -> str:
        return self.name + ' -- ' + self.main_category.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sub_category')
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.category.main_category.name + ' -- ' + self.category.name + ' -- ' + self.name
class Section(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

class Color(models.Model):
    code = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.code
        
class Brand(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name

class CouponCode(models.Model):
    code = models.CharField(max_length=50)
    discount = models.IntegerField()

    def __str__(self) -> str:
        return self.code


class Product(models.Model):
    total_quantity = models.IntegerField()
    availability = models.IntegerField()
    featured_image = models.ImageField(upload_to='product_imgs')
    product_name = models.CharField(max_length=255)
    price = models.IntegerField()
    discount = models.IntegerField()
    tax = models.IntegerField(null=True,blank=True,default=0)
    packing_cost = models.IntegerField(null=True, blank=True, default=0)
    # product_info = RichTextField()
    model_name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    # tags = models.CharField(max_length=255)
    # description = RichTextField()
    section = models.ForeignKey(Section, on_delete=models.DO_NOTHING)
    slug = models.SlugField(default='',max_length=500, null=True, blank=True)

    def __str__(self) -> str:
        return self.product_name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('product_detail', kwargs={'slug':self.slug})

    class Meta:
        db_table = 'app_Product'



def create_slug(instance, new_slug=None):
    slug = slugify(instance.product_name)
    if new_slug is not None:
        slug = new_slug
    
    qs = Product.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = '%s-%s' % (slug,qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance,*args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Product)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_image')
    image_url = models.ImageField(upload_to='product_imgs')

class AdditionalInfo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='additional_info')
    specification = models.CharField(max_length=255)
    detail = models.CharField(max_length=255)




