from django.urls import path
from ecomapp import views    
from django.conf import settings 
from django.conf.urls.static import static


urlpatterns = [
    path('product', views.product),
    path('register', views.register),
    path('login',views.user_login),
    path('logout',views.user_logout),
    path('catfilter/<cid>',views.catfilter),
    path('sort/<sid>',views.sort),
    path('pricefilter',views.pricefilter),
    path('search',views.search),
    path('product_details/<pid>',views.product_details),
    path('addtocart/<pid>',views.addtocart),
    path('cart',views.cart),
    path('updateqty/<x>/<cid>',views.updateqty),
    path('remove/<cid>',views.remove),
    path('place_order',views.placeorder),
    path('fetchorder',views.fetchorder),
    path('makepayments',views.makepayments),
    path('payment_success',views.payment_success),
    path('order_history',views.order_history),
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)