from django.shortcuts import render,get_object_or_404,redirect
from .models import Product,Order
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


def products(request):
    return render(request,'store/products.html',{'products':Product.objects.all()})


def detail(request,id):
    return render(request,'store/detail.html',{'p':get_object_or_404(Product,id=id)})


def add_cart(request,id):
    cart=request.session.get('cart',[])
    if id not in cart:
        cart.append(id)
    request.session['cart']=cart
    return redirect('cart')


@login_required
def cart(request):
    items=Product.objects.filter(id__in=request.session.get('cart',[]))
    return render(request,'store/cart.html',{'items':items})


# ⭐ payment page
@login_required
def buy(request,id):
    product=get_object_or_404(Product,id=id)
    return render(request,'store/payment.html',{'p':product})


# ⭐ payment success + order save
@login_required
def success(request, id):
    product = Product.objects.get(id=id)

    # ⭐ order save
    Order.objects.create(
        user=request.user,
        product=product
    )

    # ⭐ cart मधून remove
    cart = request.session.get('cart', [])
    if id in cart:
        cart.remove(id)
    request.session['cart'] = cart

    return render(request, 'store/success.html')


def remove_cart(request,id):
    cart=request.session.get('cart',[])
    if id in cart:
        cart.remove(id)
    request.session['cart']=cart
    return redirect('cart')


# ⭐ order history
@login_required
def orders(request):
    data = Order.objects.filter(user=request.user).order_by('-created')
    return render(request,'store/orders.html',{'orders':data})


# ⭐ signup
def signup(request):
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('home')
    else:
        form=UserCreationForm()

    return render(request,'registration/signup.html',{'form':form})