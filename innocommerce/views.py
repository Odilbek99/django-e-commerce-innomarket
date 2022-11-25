from django.shortcuts import render, redirect
from app.models import Slider, BannerArea, MainCategoty, Product, Category, Color, Brand, CouponCode
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required   
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Max, Min, Sum
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.shortcuts import get_object_or_404

def base(request):
    return render(request, 'base.html')

def home(request):
    sliders = Slider.objects.all()
    banners = BannerArea.objects.all()
    main_categories = MainCategoty.objects.all().order_by('-id')
    section = Product.objects.filter(section__name='Top Deals Of The Day')
    section2 = Product.objects.filter(section__name='Top Featured Products')

    context = {
        'sliders':sliders,
        'banners': banners,
        'main_categories': main_categories,
        'section':section,
        'section2': section2,
    }
    return render(request, 'main/home.html',context)

def PRODUCT_DETAILS(request, slug):
    product = Product.objects.filter(slug = slug)

    try:
        product = Product.objects.get(slug = slug)
        context = {
            'product' : product,
        }
      
        return render(request, 'products/product_details.html', context)
    
    except Product.DoesNotExist:
        return redirect('404')
    


def Error404(request):
    return render(request, 'errors/404.html')

def my_account(request):
    return render(request, 'accounts/my_account.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
      
        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,message='Email and Password are Invalid!!!')
            return redirect('login')
        


def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('Username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            messages.error(request,'This Username already exists!')
            return redirect('login')

        if User.objects.filter(email=email).exists():
            messages.error(request,'This Email already exists!')
            return redirect('login')
        



        user = User(
            username = username,
            email = email,
            
        )
        user.set_password(password)
        user.save()
        return redirect('login')
        
    # return redirect('404')

@login_required(login_url='accounts/login/')
def profile(request):
    return render(request, 'profile/profile.html')


@login_required(login_url='accounts/login/')
def profile_update(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_id = request.user.id

        user = User.objects.get(id=user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        if password != None and password != '':
            user.set_password(password)

        user.save()
        messages.success(request,'Profile is successfully updated')
        return redirect('profile')


def about(request):
    return render(request, 'main/about.html')
    

def contact_us(request):
    return render(request, 'main/contact_us.html')

def product(request):
    category = Category.objects.all()
    product = Product.objects.all()
    color = Color.objects.all()
    brand = Brand.objects.all()

    min_price = Product.objects.all().aggregate(Min('price'))
    max_price = Product.objects.all().aggregate(Max('price'))
    FilterPrice = request.GET.get('FilterPrice')
    color_id = request.GET.get('colorID')
    
    if FilterPrice:
        Int_FilterPrice = int(FilterPrice)
        product = Product.objects.filter(price__lte = Int_FilterPrice)
    elif color_id:
        product = Product.objects.filter(color__id = color_id)
    else:
        product = Product.objects.all()

    
    

    context = {
        'category': category,
        'product': product,
        'min_price': min_price,
        'max_price': max_price,
        'FilterPrice':FilterPrice,
        'color': color,
        'brand': brand,
    }
    return render(request, 'products/product.html', context)

def filter_data(request):
    categories = request.GET.getlist('category[]')
    brand = request.GET.getlist('brand[]')

    allProducts = Product.objects.all().order_by('-id').distinct()
    if len(categories) > 0:
        allProducts = allProducts.filter(category__id__in=categories).distinct()
        print(allProducts)

    if len(brand) > 0:
        allProducts = allProducts.filter(brand__id__in=brand).distinct()


    t = render_to_string('ajax/product.html', {'product': allProducts})

    return JsonResponse({'data': t})

@login_required(login_url="/accounts/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def cart_detail(request):
    cart = request.session.get('cart')
    # packing_cost = sum(i['packing_cost'] for i in cart.values() if i)
    # tax = sum(i['tax'] for i in cart.values() if i)
    valid_coupon = None
    invalid_coupon = None
    coupon = None

    if request.method == 'GET':
        coupon_code = request.GET.get('coupon_code')
        if coupon_code:
            try:
                coupon = CouponCode.objects.get(code = coupon_code)
                valid_coupon = 'Is Applicable on current Order!'
            except:
                invalid_coupon = 'Invalid  Coupon!'

    context = {
        # 'packing_cost': packing_cost,
        # 'tax': tax,
        'coupon': coupon,
        'valid_coupon': valid_coupon,
        'invalid_coupon':invalid_coupon,    
    }

    return render(request, 'cart/cart.html',context)
