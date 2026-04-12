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
    path('blog/<slug:slug>/', views.blog_post, name='blog_post'),
    
    # Páginas legales
    path('privacidad/', views.privacidad, name='privacidad'),
    path('terminos/', views.terminos, name='terminos'),

    # Landing pages SEO
    path('empresa-importacion-exportacion-panama/', views.landing_importacion, name='landing_importacion'),

    # Formularios
    path('asesoria/', views.asesoria, name='asesoria'),
    path('cotizacion/', views.cotizacion, name='cotizacion'),

    # Newsletter
    path('suscribir-newsletter/', views.suscribir_newsletter, name='suscribir_newsletter'),

    # SEO: Sitemap y Robots
    path('sitemap.xml', views.sitemap_xml, name='sitemap'),
    path('robots.txt', views.robots_txt, name='robots'),
]