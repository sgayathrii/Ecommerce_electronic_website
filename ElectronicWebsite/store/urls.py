from django.conf.urls import url
from store import views

#Template urls!

app_name = 'store'

urlpatterns = [
    #url(r'^store/$',views.store, name='store'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^checkout/$', views.checkout, name='checkout'),
]
