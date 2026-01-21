from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.home, name='home'),
    path('servicios/', views.servicios, name='servicios'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('contacto/', views.contacto, name='contacto'),
    path('api/cotizacion/', views.solicitar_cotizacion, name='solicitar_cotizacion'),
    
    # Blog Routes
    path('blog/', views.blog, name='blog'),
    path('blog/feria-internacional-colon/', views.blog_post, name='blog_post'),
    
    # Páginas legales
    path('privacidad/', views.privacidad, name='privacidad'),
    path('terminos/', views.terminos, name='terminos'),

    # Formularios
    path('asesoria/', views.asesoria, name='asesoria'),
    path('cotizacion/', views.cotizacion, name='cotizacion'),

    # Newsletter - ⭐ CAMBIAR ESTO
    path('suscribir-newsletter/', views.suscribir_newsletter, name='suscribir_newsletter'),
]