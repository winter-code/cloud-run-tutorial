from django.urls import path
from helloapp import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', views.homepage, name='home'),
    path('about/', views.aboutpage, name='about'),
    path('pub-sub', csrf_exempt(views.recieve_pubsub_message), name='pub-sub'),
    path('send', views.send_message, name='send-message-to-pub-sub-topic')
]