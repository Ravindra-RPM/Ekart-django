from django.shortcuts import render, HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from ecomapp.models import Product, Cart, Order, OrderHistory
from django.db.models import Q
import razorpay
from django.core.mail import send_mail

# Create your views here.
def product(request):
    #p=Product.objects.all()                    # --> it gives active and non active records
    p=Product.objects.filter(is_active=True)    # --> it gives only active records
    #print(p)
    context={}
    context['data']=p
    return render(request,'index.html',context)

def register(request):
    if request.method=='GET':
        return render(request,'register.html')
    else:
        n = request.POST['uname']
        e = request.POST['uemail']
        p = request.POST['upass']
        cp = request.POST['ucpass']
        # print(n)
        # print(e)
        # print(p)
        # print(cp)
        context={}
        if n=="" or e=="" or p=="" or cp=="":
            # print("Please fill out all fields")
            context['errmsg']="Please fill out all fields"
        elif p!=cp:
            # print("password and conform password not matching")
            context['errmsg']="password and conform password not matching"
        elif len(p)<8:
            # print("password length is less than 8")
            context['errmsg']="password length is less than 8"
        else:
            # auth_user table used for user registration so User class object created
            #u = User.objects.create(username=n, password=p, email=e) #--> password is not encrypted for this
            u = User.objects.create(username=n, email=e) #--> password is not encrypted for this
            u.set_password(p)  # --> password is encrypted for this and "set_password()" method is used
            u.save()
            context['success']="User Created Successfully"
        
        return render(request,'register.html',context)

def user_login(request):
    if request.method=="GET":
        return render(request,'login.html')
    else:
        n = request.POST['uname']
        p = request.POST['upass']
        print(n)
        print(p)

        # authenticate method checks username and password for auth_user table
        # it returns 'username' if username and password matches or gives 'None' <-- None is keyword not a string
        u=authenticate(username=n,password=p)
        print(u)
        context={}
        if u==None:
            context['errmsg']="Invalid username or password"
            return render(request,'login.html',context)
        else:
            # login() stores the users id in session table, session is for server-side & cockies are for client-side 
            # login() is function
            login(request,u)
            return redirect('/product')
            # request.session.id
            #for template we use --> user.is_authenticated
            # for py

def user_logout(request):
    logout(request)                 # used to destroy the id stored in session table
    return redirect('/product')

def catfilter(request,cid):
    #p=Product.objects.filter(cat=cid,is_active=True)
    q1=Q(cat=cid)
    q2=Q(is_active=True)
    p=Product.objects.filter(q1 & q2)
    #p=Product.objects.filter(cat=cid,is_active=True)
    print(p)
    context={}
    context['data']=p
    return render(request,'index.html',context)

def sort(request,sid):
    context={}
    print(type(sid))
    if int(sid)==1:
        #p=Product.objects.order_by('-price').filter(is_active=True)
        t='-price'
    else:
        #p=Product.objects.order_by('price').filter(is_active=True) 
        t='price'

    p=Product.objects.order_by(t).filter(is_active=True)
    context['data']=p
    return render(request,'index.html',context)

def pricefilter(request):
    min=request.GET['minprice']
    max=request.GET['maxprice']
    print(min,max)
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    p=Product.objects.filter(q1 & q2).filter(is_active=True)
    context={}
    context['data']=p
    return render(request,'index.html',context)

def search(request):
    srch=request.GET['search']
    print(srch)
    n=Product.objects.filter(name__icontains=srch).filter(is_active=True)
    pdet=Product.objects.filter(pdetail__icontains=srch).filter(is_active=True)

    context={}
    all=n.union(pdet)

    if len(all)==0:
        context['errmsg']='Product not found'

    context['data']=all
    return render(request,'index.html',context)

def product_details(request,pid):
    p=Product.objects.filter(id=pid)
    print(pid)
    print(p)
    context={}
    context['data']=p
    return render(request,'product_details.html',context)

def addtocart(request,pid):
    if request.user.is_authenticated:      
        # print("User is logged in...")
        # u=request.user.id
        u=User.objects.filter(id=request.user.id)
        # print(u)
        p=Product.objects.filter(id=pid)
        context={}
        context['data']=p
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1 & q2)

        if len(c)==0:
            c=Cart.objects.create(uid=u[0],pid=p[0])  # as foreign key is used we have to pass the list's index position
            c.save()
            # return HttpResponse('Product added to cart Successfully....')                     
            context['success']="Product Added Successfully in the Cart"
            return render(request,'product_details.html',context)
        else:
            context['errmsg']="Product already exists in the cart.."
            return render(request,'product_details.html',context)
    else:
        return redirect('/login')

def cart(request):
    c=Cart.objects.filter(uid=request.user.id)
    # print(c)
    context={}
    context['data']=c
    s = 0
    for i in c:
        s = s+i.pid.price*i.qty
    context['total']=s
    context['n']=len(c)
    return render(request,'cart.html',context)

def updateqty(request,x,cid):
    c=Cart.objects.filter(id=cid)
    q=c[0].qty

    if x=='1':
        q = q+1
    elif q > 1:
        q=q-1
    c.update(qty=q)
    return redirect('/cart')

def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    print(c)
    c.delete()
    return redirect('/cart')

def placeorder(request):
    c=Cart.objects.filter(uid=request.user.id)

    for i in c:
        amt=i.qty*i.pid.price
        o=Order.objects.create(uid=i.uid, pid=i.pid, qty=i.qty, amt=amt)
        o.save()
        i.delete()
          
    return redirect('/fetchorder')

def fetchorder(request):
    o=Order.objects.filter(uid=request.user.id)
    context={}
    s=0
    for i in o:
        s=s+i.amt
    context['data']=o
    context['total']=s
    context['n']=len(o)
    return render(request,'place_order.html',context)

def makepayments(request):
    
    # client = razorpay.Client(auth=("YOUR_ID", "YOUR_SECRET"))
    client = razorpay.Client(auth=("rzp_test_qXk2HIXIysZL4s", "op8NrNxEw1nrHGN3KOnk5zna"))

    o=Order.objects.filter(uid=request.user.id)
    s=0
    for i in o:
        s=s+i.amt
    
    data = { "amount": s * 100, "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create(data=data)
    print(payment)
    context={}
    context['payment']=payment
    return render(request, 'pay.html', context)

def payment_success(request):
    o=Order.objects.filter(uid=request.user.id)
    for i in o:
        oh=OrderHistory.objects.create(uid=i.uid, pid=i.pid, qty=i.qty, amt=i.amt)
        i.delete()
        oh.save()
    sub='EDROAD | New Course Enrollment'
    msg='<h1>Order Placed Successfully...!!!</h1>'
    frm='menkudaleravindra@gmail.com'
    u=User.objects.filter(id=request.user.id)
    to=u[0].email

    send_mail(
        sub,
        msg,
        frm,
        [to],
        fail_silently=False

    )

    return render(request,'payment_success.html')

def order_history(request):
    oh=OrderHistory.objects.filter(uid=request.user.id)
    context={}
    context['data']=oh
    return render(request,'order_history.html',context)
     



        