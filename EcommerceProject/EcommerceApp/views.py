from django.shortcuts import render,redirect
from django.views import View
from .models import Product,Customer,Cart
from .forms import CustomerRegForm,CustomerProfileForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
import razorpay
from django.conf import settings

# Create your views here.
def home(request):
    return render(request, 'base.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

class CategoryView(View):
    def get(self,request,val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, 'category.html', locals())

class CategoryTitle(View):
    def get(self,request,val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=Product[0].category).values('title')
        return render(request, 'category.html', locals())

class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'productdetail.html',locals())

class CustomerRegView(View):
    def get(self,request):
        form = CustomerRegForm()
        return render(request, 'customerreg.html',locals())
    def post(self,request):
        form = CustomerRegForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! User Registration Successfully.")
        else:
            messages.warning(request ,"Invalid Credentials.")
        return render(request,'customerreg.html',locals())

class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request, 'profile.html',locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user,name=name,mobile=mobile,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulations! profile updated Successfully")
        else:
            messages.warning(request ,"Invalid Credentials.")
        return render(request, 'profile.html',locals())
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'address.html', locals())
class UpdateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'updateaddress.html',locals())
    def post(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(request.POST,instance=add)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! Address updated Successfully")
        else:
            messages.warning(request ,"Invalid Credentials.")
        return redirect('address')
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0.0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + 40
    return render(request, 'addtocart.html', locals())

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        cart = Cart.objects.filter(user=request.user)
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        cart = Cart.objects.filter(user=request.user)
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        cart = Cart.objects.filter(user=request.user)
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data = {
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

class Checkout(View):
    def get(self,request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 40.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
                razoramount = int(totalamount * 100)
                client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
                data = {
                    "amount": razoramount,
                    "currency": "INR",
                    "receipt": "order_rcptid_12",
                }
                order = client.order.create(data=data)
                p.razorpay_id = order['id']
                p.save()
            return render(request, 'checkout.html', locals())
        else:
            return render(request, 'emptycart.html')
    def post(self,request):
        user = request.user
        name = request.POST.get('name')