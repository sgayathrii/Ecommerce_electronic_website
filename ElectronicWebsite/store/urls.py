from django.conf.urls import url
from store import views
from django.contrib.auth import views as auth_views

#Template urls!

app_name = 'store'

urlpatterns = [
    #url(r'^store/$',views.store, name='store'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^checkout/$', views.checkout, name='checkout'),

    url(r'^update_item/$', views.updateItem, name='update_item'),
    url(r'^process_order/$', views.processOrder, name='process_order'),
    url(r'^login/$', views.loginPage, name='login'),
    url(r'^register/$', views.registerPage, name='register'),
    url(r'^logout/$', views.logoutUser, name='logout'),
    url(r'^reset_password/$', auth_views.PasswordResetView.as_view(template_name="store/password_reset.html"),
     name="reset_password"),
]
