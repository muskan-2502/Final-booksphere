"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from myapp import views

if settings.DEBUG:
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', views.index, name='index'),
        path('about', views.about, name='about'),
        path('contact', views.contact, name='contact'),
        path('book', views.book, name='book'),
        path('signup', views.signup, name='signup'),
        path('login', views.login, name='login'),
        path('logout', views.logout, name='logout'),
        path('adduserdetail', views.adduserdetail, name='adduserdetail'),
        path('showuser', views.showuser, name='showuser'),
        path('editprofile', views.editprofile, name='editprofile'),
        path('update', views.update, name='update'),
        path('addauthor', views.addauthor, name='addauthor'),
        path('showauthor', views.showauthor, name='showauthor'),
        path('editauthor', views.editauthor, name='editauthor'),
        path('updateauthor', views.updateauthor, name='updateauthor'),
        path('upload_book', views.upload_book, name='upload_book'),
        path('bookdetail/<int:bid>', views.bookdetail, name='bookdetail'),
        path('pricing', views.pricing, name='pricing'),
        path('create_order/<int:plan_id>', views.create_order, name='create_order'),
        path('payment_success', views.payment_success, name='payment_success'),
        path('showfeedback', views.showfeedback, name='showfeedback'),
        path('complaint_submit', views.complaint_submit, name='complaint_submit'),
        path('upload_book_detail', views.upload_book_detail, name='upload_book_detail'),
        path('send_publish_request', views.send_publish_request, name='send_publish_request'),
        path('update_publisher_request', views.update_publisher_request, name='update_publisher_request'),
        path('showrequest', views.showrequest, name='showrequest'),
        path('find_products', views.find_products, name='find_products'),
        path('forgotpassword', views.forgotpassword, name='forgotpassword'),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
