from django.contrib import admin
from .models import Product,Customer,Cart,Payment,Orderplaced
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','title','discounted_price','category','product_image']

class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','name','locality','city','state','zipcode']

class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']

class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','razorpay_order_id','razorpay_payment_id','razorpay_payment_status','paid']

class OrderplacedModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','customer','product','quantity','ordered_date','status','payment']

admin.site.register(Product,ProductAdmin)
admin.site.register(Customer,CustomerModelAdmin)
admin.site.register(Cart,CartModelAdmin)
admin.site.register(Payment,PaymentModelAdmin)
admin.site.register(Orderplaced,OrderplacedModelAdmin)