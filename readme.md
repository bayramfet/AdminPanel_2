# Admin Panel Customization

```sh

    $ python -m venv env
    $ source env/bin/activate
    
    $ pip install django
    $ pip install djangorestframework
    $ pip install python-decouple
    $ pip freeze > requirements.txt

    $ django-admin startproject main .

```

create .env file:

```

SECRET_KEY = django-insecure-)=b-%-w+0_^slb(exmy*mfiaj&wz6_fb4m&s=az-zs!#1^ui7j

```

main/settings.py ->

```py
# ...
from decouple import config
# ...
# SECRET_KEY = django-insecure-chars
SECRET_KEY = config('SECRET_KEY')
# ...
```

go to terminal:

```sh

    $ python manage.py migrate
    $ python manage.py runserver

```

click the link with CTRL key pressed in the terminal and see django rocket.
go to terminal, stop project, add app.

```sh
    
    $ manage.py startapp product

```

main/settings.py ->

```py
# ...
INSTALLED_APPS = [
    # ...
    'product',
    # ...
]
# ...
```

products/models.py:

```py

from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_in_stock = models.BooleanField(default=True)
    slug = models.SlugField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
    
    def __str__(self):
        return self.name

```

```sh
    
    $ python manage.py makemigraions
    $ python manage.py migrate
    $ python manage.py createsuperuser

```

products/admin.py:

```py

from django.contrib import admin
from .models import Product

admin.site.register(Product)

admin.site.site_title = "Clarusway Title"
admin.site.site_header = "Clarusway Admin Portal"  
admin.site.index_title = "Welcome to Clarusway Admin Portal"

```

### FAKER

```sh
    
    $ pip install faker
    $ pip freeze > requirements.txt

```

product/faker.py:

```py

from product.models import *
from faker import Faker

# Model:Product:
def runProduct():

    faker = Faker() # Faker(['tr-TR'])

    for _ in range(200):
        product = Product(name=faker.domain_word(), description=faker.paragraph(), is_in_stock=faker.pybool())
        product.save()

    print ('Finished')

# Model:Review:
def runReview():

    faker = Faker()

    for product in Product.objects.iterator():
        reviews = [Review(review=faker.paragraph(), product=product) for _ in range(3)]
        Review.objects.bulk_create(reviews)

    print ('Finished')

```

go to terminal, work on shell:

```sh

    $ python manage.py shell
    > from product.faker import runProduct
    > runProduct()
    > exit()

```

go to admin site and check data.

-------------------------------------------------------------------------------------------------

### ModelAdmin options and methods

product/admin.py ->

```py

class ProductAdmin(admin.ModelAdmin):
    # Tablo sutunları:
    list_display = ['id', 'name', 'is_in_stock', 'create_date', 'update_date']
    # Tablo üzerinde güncelleyebilme:
    list_editable = ['is_in_stock']
    # Kayda gitmek için linkleme:
    list_display_links = ['name']
    # Filtreleme (arama değil):
    list_filter = ['is_in_stock', 'create_date', 'update_date']
    # Arama:
    search_fields = ['id', 'name']
    # Default Sıralama:
    ordering = ['-id']
    # Sayfa başına kayıt sayısı:
    list_per_page = 20
    # Tümünü göster yaparken max kayıt sayısı:
    list_max_show_all = 200
    # Arama bilgilendirme yazısı: 
    search_help_text = 'Arama Yapmak için burayı kullanabilirsiniz.'
    # Otomatik kaıyıt oluştur:
    prepopulated_fields = {'slug' : ['name']}
    # Tarihe göre filtreleme başlığı:
    date_hierarchy = 'create_date'
    # Form liste görüntüleme
    fields = (
        ('name', 'is_in_stock'),
        'slug',
        'description',
    )
    '''
    # Detaylı form liste görüntüleme
    fieldsets = (
        ('General Settings', {
            "classes": ("wide",),
            "fields": (
                ('name', 'slug'),
                "is_in_stock"
            ),
        }),
        ('Optionals Settings', {
            "classes": ("collapse",),
            "fields": ("description",),
            'description': "You can use this section for optionals settings"
        }),
    )
    '''

admin.site.register(Product, ProductAdmin)

```

product/admin.py -> actions:

```py
# ...

class ProductAdmin(admin.ModelAdmin):
    # ...

    def set_stock_in(self, request, queryset):
        count = queryset.update(is_in_stock=True)
        self.message_user(request, f'{count} adet "Stokta Var" olarak işaretlendi.')
    

    def set_stock_out(self, request, queryset):
        count = queryset.update(is_in_stock=False)
        self.message_user(request, f'{count} adet "Stokta Yok" olarak işaretlendi.')

    actions = ('set_stock_in', 'set_stock_out')
    set_stock_in.short_description = 'İşaretli ürünleri stoğa ekle'
    set_stock_out.short_description = 'İşaretli ürünleri stoktan çıkar'

```

product/admin.py -> extra field from methods:

```py
# ...

class ProductAdmin(admin.ModelAdmin):
    # ...

    def added_days_ago(self, object):
        from django.utils import timezone
        different = timezone.now() - object.create_date
        return different.days

    list_display += ['added_days_ago']

```

-----------------------------------------------------------------------------------------------------

### RichText Editors
    WYSIWYG (what you see is what you get)

    https://djangopackages.org/grids/g/wysiwyg/
    https://django-ckeditor.readthedocs.io/en/latest/

Install module:

```sh
    
    $ pip install django-ckeditor
    $ pip freeze > requirements.txt

```

main/settings.py -> 

```py
# ...
INSTALLED_APPS = (
    # ...
    'ckeditor',
    # ...
)
# ...
CKEDITOR_CONFIGS = {
    'default' : {
        'toolbar' : 'full',
        'height' : 700,
        'width' : 1000
    }
}
```

product/models.py ->

```py
# ...
from ckeditor.fields import RichTextField
# ...
class Review(models.Model):
    # ...
    description = RichTextField() # models.TextField(blank=True, null=True)

```

```sh
    
    $ python manage.py makemigraions
    $ python manage.py migrate

```

* Not: Template dosyasında kullanım: {{description | safe}}

-----------------------------------------------------------------------------------------------------

### Model Relations

product/models.py ->

```py
#...

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

```

```sh
    
    $ python manage.py makemigraions
    $ python manage.py migrate

```

product/admin.py -> 

```py
#...

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created_date', 'is_released')
    list_per_page = 50
    raw_id_fields = ('product',) 

admin.site.register(Review, ReviewAdmin)

```

go to terminal, work on shell:

```sh

    $ python manage.py shell
    > from product.faker import runReview
    > runReview()
    > exit()

```

### TabularInline

product/admin.py ->

```py
#...

class ReviewInline(admin.TabularInline):  # Alternatif: StackedInline (farklı görünüm aynı iş)
    model = Review # Model
    extra = 1 # Yeni ekleme için ekstra boş alan
    classes = ['collapse'] # Görüntülme tipi (default: tanımsız)


class ProductAdmin(admin.ModelAdmin):
    #...
    #...
    inlines = (ReviewInline,)

```

### Custom Fields

product/admin.py ->

```py
#...

class ProductAdmin(admin.ModelAdmin):
    #...
    #...
    
    # Kaçtane yorum var:
    def how_many_reviews(self, object):
        count = object.reviews.count()
        return count

    list_display += ['how_many_reviews']

```

### Horizontal & Vertical Viewing (ManyToManyField)

product/models.py ->

```py
# ...

class Category(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        
    def __str__(self):
        return self.name

class Product(models.Model):
    categories = models.ManyToManyField(Category, related_name="products")
    # ...

```

```sh
    
    $ python manage.py makemigraions
    $ python manage.py migrate

```

product/admin.py ->

```py
# ...

admin.site.register(Category)

# ...

class ProductAdmin(admin.ModelAdmin):
    # ...
    # ...
    # Form liste görüntüleme
    fields = (
        ('name', 'is_in_stock'),
        ('slug'),
        ('description', 'category'),
    )
    # İlişkili tablo (many2many) nasıl görünsün:
    filter_horizontal = ["category"] # Yatay Görünüm
    # filter_vertical = ["category"] # Dikey Görünüm

```
----
2. Session:
----

# Display Image Fields

main/settings.py ->

```py
#...

import os

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
# STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

#...
```

main/urls.py:

```py

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]

from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

```

product/models.py ->

```py
# ...

class Product(models.Model):
    # ...
    image = models.ImageField(null=True, blank=True, default="clarusway.png", upload_to="product/")

```

```sh
    
    $ pip install pillow
    $ pip freeze > requirements.txt
    $ python manage.py makemigraions
    $ python manage.py migrate

```

product/models.py ->

```py
# ...

class Product(models.Model):
    # ...
    # ...

    # Method for view image-large in detail page:
    def view_image(self):
        from django.utils.safestring import mark_safe
        if self.image:
            return mark_safe(f'<img src={self.image.url} style="max-height:100px; max-width:200px;"></img>')
        return mark_safe(f'<h2>No Image</h2>')

```

product/admin.py ->

```py
# ...

class ProductAdmin(admin.ModelAdmin):
    # ...
    # ...
    # Resim gösterme read_only olarak çağır:
    readonly_fields = ["view_image"]
    # Form liste görüntüleme
    fields = (
        ('name', 'is_in_stock'),
        ('image', 'view_image'),
        ('slug'),
        ('description', 'category'),
    )
    # ...
    # ...

    # Listede küçük resim göster:
    def view_image_in_list(self, obj):
        from django.utils.safestring import mark_safe
        if obj.image:
            return mark_safe(f'<img src={obj.image.url} style="height:30px; width:30px;"></img>')
        return '-*-'

    view_image_in_list.short_description = 'Image'
    list_display = ['view_image_in_list'] + list_display

```

# Customize Templates

    default directory:
    env/lib/django/contrib/admin/templates/admin

    # Sayfalar:
    admin/change_list.html -> Liste Sayfası
    admin/change_form.html -> Ekleme ve Güncelleme Sayfaları
    admin/delete_confirmation.html -> Silme İşlemi İçin Onay Sayfası
    admin/object_history.html -> Modelin Geçmişi

    # Şablonlar:
    admin/<extend_edilecek_sablon_adi>.html -> admin ana sayfa
    admin/<app_adi>/<extend_edilecek_sablon_adi>.html -> applere özel
    admin/<app_adi>/<model_adi>/<extend_edilecek_sablon_adi>.html -> modellere özel

main/settings.py ->

```py

TEMPLATES = [
    {
        #...
        # İlk önce buraya bakar yoksa defaulta gider:
        'DIRS': [BASE_DIR, "templates"],
        #...
    },
]

```

* Oluştur: "templates/admin/product/product/change_form.html"
* İçi boş olduğu için Ekleme ve Güncelleme Sayfaları boş görünecek
* Default olan change_forma gidip blocklara bakabiliriz, extend edip istediğimizi güncelleriz.

```html

{% extends 'admin/change_form.html' %}

{% block form_top %}
    <h1>Product model new template</h1>
{% endblock  %}

```


* django/templates/admin extends hierarchy: base.html > base_site.html > change_form.html
* oluştur: "templates/admin/base_site.html"

```html

{% extends 'admin/base.html' %}
{% load static %}

{% block branding %}
    <div class="myDiv">
        <img src="{% static 'clarusway.png' %}" style="height: 50px; width: 50px;" alt="">
        <h1 id="head">Clarusway Admin Site</h1>
    </div>
{% endblock %}

{% block extrastyle %}
    <style>
        #header {
            height: 50px;
            background: #542380;
            color: #fff;
        }
        #branding h1 {
            color: #fff;
        }
        a:link, a:visited {
            color: #10284e;
        }
        div.breadcrumbs {
            background: #542380;
            color: #10284e;
            opacity: 0.75;
            margin-bottom: 10px;
            color: #fff !important;
        }
        div.breadcrumbs a {
            color: #fff !important;
        }
        .module h2, .module caption, .inline-group h2 {
            background: #542380;
        }
        .button, input[type=submit], input[type=button], .submit-row input, a.button {
            background: #10284e;
            color: #fff;
        }
        div.myDiv {
            display: flex;
            align-items: center;
        }
    </style>
{% endblock %}

```

# THIRD PARTY PACKAGES

## List Filter Dropdown

* https://github.com/mrts/django-admin-list-filter-dropdown


```sh
    
    $ pip install django-admin-list-filter-dropdown
    $ pip freeze > requirements.txt

```

main/settings.py -> 

```py
# ...
INSTALLED_APPS = (
    # ...
    'django_admin_listfilter_dropdown',
    # ...
)
# ...
```

product/admin.py ->

```py
#...
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter
#...

class ProductAdmin(admin.ModelAdmin):
    #...
    list_filter = [('name', DropdownFilter), 'create_date', 'update_date']
    #...

class ReviewAdmin(admin.ModelAdmin):
    #...
    list_filter = [('product', RelatedDropdownFilter)]
    #...

```

## Django Date Range Filter

* https://github.com/silentsokolov/django-admin-rangefilter


```sh
    
    $ pip install django-admin-rangefilter
    $ pip freeze > requirements.txt

```

main/settings.py ->

```py
# ...
INSTALLED_APPS = (
    # ...
    'rangefilter',
    # ...
)
# ...
```

product/admin.py ->

```py
# ...
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
# ...

class ProductAdmin(admin.ModelAdmin):
    # ...
    list_filter = [('name', DropdownFilter), ('create_date', DateRangeFilter), ('update_date', DateTimeRangeFilter)]
    # ...

```

## Import - Export

* https://django-import-export.readthedocs.io/en/latest/


```sh
    
    $ pip install django-import-export
    $ pip freeze > requirements.txt

```

main/settings.py ->

```py
# ...
INSTALLED_APPS = (
    # ...
    'import_export',
    # ...
)
# ...
```

product/admin.py ->

```py
# ...
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# ...

# ...
# Import-Export ModelResource:
class ProductResource(resources.ModelResource):
    class Meta:
        model = Product

# ...
class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ProductResource
    # ...
    # ...
```

## Template Module: Grappelli

* https://django-grappelli.readthedocs.io/en/latest/
* "/templates" klasörü varsa iptal edilebilir.


```sh
    
    $ install django-grappelli
    $ pip freeze > requirements.txt

```

main/settings.py ->

```py
# ...
INSTALLED_APPS = (
    'grappelli', # En üstte olacak.
    # ...
    # ...
)
# ...
```

main/urls.py ->

```py
# ...
from django.conf.urls import include
# ...
urlpatterns = [
    path('grappelli/', include('grappelli.urls')), # En üstte olacak.
    path('admin/', admin.site.urls),
    # ...
]
# ...
```

Finished :)