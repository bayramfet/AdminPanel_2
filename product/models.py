from django.db import models
from ckeditor.fields import RichTextField

# Category:
class Category(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        
    def __str__(self):
        return self.name

# Product:
countries = [
    ('TR', 'Turkey'),
    ('EN', 'England'),
    ('DE', 'Germany'),
    ('FR', 'France'),
]

class Product(models.Model):
    category = models.ManyToManyField(Category, related_name='products')
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=2, choices=countries, blank=True, null=True, default='DE')
    description = RichTextField() # models.TextField(blank=True, null=True)
    is_in_stock = models.BooleanField(default=True)
    slug = models.SlugField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    image = models.ImageField(null=True, blank=True, default='clarusway.png', upload_to='product/')

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
    
    def __str__(self):
        return self.name

    ### Show Image In Details ###
    def view_image(self):
        from django.utils.safestring import mark_safe
        if self.image:
            return mark_safe(f'<a target="_blank" href="{self.image.url}"><img src={self.image.url} style="max-height:100px; max-width:200px;"></img></a>')
        return mark_safe('<h2>NO IMAGE</h2>')
    ### --- ###

# Review:
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    review = models.TextField()
    is_released = models.BooleanField(default=True)
    created_date = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return f"{self.product.name} - {self.review}"