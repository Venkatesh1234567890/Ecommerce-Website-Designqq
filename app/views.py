from http.client import HTTPResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .form import CustomUserForm
from django.contrib import messages
from .models import *
# from .models import Category, Product
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
import json

def home(request):
    print(request.user)
    products = Product.objects.filter(trending=1)
    categories = Category.objects.all()
    return render(request, 'shop/index.html', {"products": products,'categories': categories})


def favviewpage(request):
    if request.user.is_authenticated:
        fav=Favourite.objects.filter(user=request.user)
        return render(request,"shop/fav.html",{"fav":fav})
    else:
        return redirect("/")

def remove_fav(request,fid):
    item=Cart.objects.get(id=fid)
    item.delete()
    return redirect("/favviewpagee")    

from django.db.models import Sum
def cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        total_cost = Cart.objects.aggregate(Sum('total_cost'))['total_cost__sum']

        return render(request,"shop/cart.html",{"cart":cart,"total_cost":total_cost})
    else:
        return redirect("/")

def remove_cart(request,cid):
    cartitem=Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect("/")    

@csrf_exempt
def fav_page(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('pid')
            
            # Fetch the product instance
            product = get_object_or_404(Product, id=product_id)
            
            # Create a new favourite instance
            Favourite.objects.create(user=request.user, product=product)
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'invalid request'}, status=400)
                                                
@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_qty = data.get('product_qty')
            pid = data.get('pid')

            product = get_object_or_404(Product, id=pid)
            user = request.user

            Cart.objects.create(user=user, product=product, quantity=product_qty)

            return JsonResponse({'status': 'Product added to cart successfully!'})
        except Exception as e:
            return JsonResponse({'status': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'Invalid request method!'}, status=400)

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged out Successfully")
        return redirect("/")

@csrf_exempt
def login_page(request):
 
    if request.method == 'POST':
        name = request.POST.get('username')
        pwd = request.POST.get('password')
        print(name,pwd)
        user = authenticate(request, username=name, password=pwd)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in Successfully")
            return redirect("/")
        else:
            messages.error(request, "Invalid User Name or Password")
            return redirect("/login_page")
    return render(request, 'shop/login.html')
    
@csrf_exempt
def register(request):
    form = CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Registratioon Success You can Login Now..!')
            return redirect('/login_page')
    return render(request, "shop/register.html", {'form': form})

def collections(request):
    categories = Category.objects.all()
    return render(request, 'shop/collections.html', {'categories': categories})

# views.py
# views.py
# views.py
def collection_detail(request, cname):
    category = get_object_or_404(Category, name=cname)
    products = Product.objects.filter(Category=category)  # Use 'Category' as defined in the model
    print(products)
    return render(request, 'shop/collection_details.html', {'products': products, 'category': category})




def product_details(request,id):
    # if Category.objects.filter(name=cname, status=0):
    if Product.objects.filter(id=id, status=0).exists():
        products = Product.objects.filter(id=id, status=0).first()
        return render(request, "shop/products/product_details.html", {"products": products})
    else:
        messages.error(request, "No Such Product Found")
        return redirect('collections')
    # else:
    #     messages.warning(request, "No Such Category Found")
    #     return redirect('collections')


def add_to_cart_main(request):
    if request.method =="POST":
        products_id =request.POST.get('products_id')
        quantity_1 = request.POST.get('quantity_1')

        c_user = User.objects.get(username=request.user)
        product = Product.objects.get(id=products_id)
        total =int(quantity_1) * product.selling_price
        # print(total,"total")
        # print(c_user,"user")
        cart = Cart.objects.create(
            user =c_user,
            product = product,
            product_qty=quantity_1,
            total_cost =total
            )
        cart.save()
    messages.success(request,"Product Added Successfully")
    return render(request,"shop/products/product_details.html",{"products": product})

def fav_page_main(request):
    if request.method == 'POST':
        product_id = request.POST.get('products_id')
        quantity = request.POST.get('quantity_1')

        # Handle the logic to add the product to favorites
        # For example:
        product = Product.objects.get(id=product_id)
        # Assuming you have a model for favorite products
        # Favorite.objects.create(user=request.user, product=product, quantity=quantity)
        
        # return HttpResponse('Product added to favorites')  # or redirect to a different page
    return render(request,"shop/products/product_details.html",{"products": product})


def favorite(request):
    if request.method =="POST":
        products_id =request.POST.get('products_id')
        product = Product.objects.get(id=products_id)
        quantity = request.POST.get('quantity_1')


        product = get_object_or_404(Product, id=products_id)
            
            # Create a new favourite instance
        Favourite.objects.create(user=request.user, product=product,product_qty=quantity)
        print(request.user,"user")
    messages.success(request,"Favorite Added Successfully")
    return render(request,"shop/products/product_details.html",{"products": product})