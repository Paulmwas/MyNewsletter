from django.urls import path
from .views import home, send_mail_page

urlpatterns = [
    path('', home, name='home'),
    path('send_mail', send_mail_page, name='send_mail') 
]
