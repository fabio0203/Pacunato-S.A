from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
import json
import requests
import re

def home(request):
    """Vista principal de la página de inicio"""
    context = {
        'page_title': 'Pacunato S.A. - Compras Internacionales',
    }
    return render(request, 'home.html', context)

def servicios(request):
    """Vista de la página de servicios"""
    return render(request, 'servicios.html')

def nosotros(request):
    """Vista de la página quiénes somos"""
    return render(request, 'nosotros.html')

def blog(request):
    """Vista para la página principal del blog con datos dinámicos"""
    from .models import BlogPost

    # Posts publicados ordenados por fecha
    published_posts = BlogPost.objects.filter(is_published=True).order_by('-created_at')

    # Post destacado (primero con is_featured=True)
    featured_post = published_posts.filter(is_featured=True).first()

    # Posts regulares (excluir el destacado para no duplicar)
    if featured_post:
        regular_posts = published_posts.exclude(id=featured_post.id)
    else:
        regular_posts = published_posts

    # Posts recientes para sidebar (top 5)
    recent_posts = published_posts[:5]

    # Contar posts por categoría
    category_counts = {}
    for category_code, category_name in BlogPost.CATEGORY_CHOICES:
        count = published_posts.filter(category=category_code).count()
        category_counts[category_code] = {
            'name': category_name,
            'count': count
        }

    # Total de posts
    total_posts = published_posts.count()

    context = {
        'featured_post': featured_post,
        'regular_posts': regular_posts,
        'recent_posts': recent_posts,
        'category_counts': category_counts,
        'total_posts': total_posts,
    }

    return render(request, 'blog.html', context)

def blog_post(request, slug=None):
    """
    Vista para artículo individual con conteo de vistas únicas
    ⭐ ACTUALIZADO: Usa el campo 'views' existente
    """
    from .models import BlogPost, BlogPostView
    
    # Obtener el post por slug (o el primero si no hay slug)
    if slug:
        post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    else:
        # Fallback: primer post publicado
        post = BlogPost.objects.filter(is_published=True).first()
        if not post:
            # Si no hay posts, crear mensaje
            return render(request, 'blog_post.html', {
                'error': 'No hay artículos publicados aún.'
            })
    
    # Obtener IP del visitante
    ip_address = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
    
    # Verificar si esta IP ya vio este post
    try:
        view, view_created = BlogPostView.objects.get_or_create(
            post=post,
            ip_address=ip_address,
            defaults={'user_agent': user_agent}
        )

        # Solo incrementar si es vista NUEVA
        if view_created:
            post.views += 1
            post.save()

    except Exception as e:
        pass  # Silenciar errores de tracking para no afectar la visualización
    
    # Obtener número de visitantes únicos
    unique_visitors = post.unique_views.count()

    # Navegación anterior/siguiente
    published_posts_all = BlogPost.objects.filter(is_published=True).order_by('-created_at')

    # Post anterior (más nuevo)
    previous_post = published_posts_all.filter(created_at__gt=post.created_at).order_by('created_at').first()

    # Post siguiente (más viejo)
    next_post = published_posts_all.filter(created_at__lt=post.created_at).order_by('-created_at').first()

    context = {
        'post': post,
        'view_count': post.views,  # Total de vistas
        'unique_visitors': unique_visitors,  # Visitantes únicos
        'previous_post': previous_post,  # Post anterior
        'next_post': next_post,  # Post siguiente
    }
    
    return render(request, 'blog_post.html', context)

def contacto(request):
    """Vista de la página de contacto"""
    return render(request, 'contacto.html')

@require_http_methods(["POST"])
def solicitar_cotizacion(request):
    """Procesar solicitud de cotización vía AJAX"""
    try:
        data = json.loads(request.body)
        return JsonResponse({
            'success': True,
            'message': 'Cotización recibida. Nos contactaremos en menos de 24 horas.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Error al enviar la solicitud. Por favor intente nuevamente.'
        }, status=400)

def privacidad(request):
    """Página de Política de Privacidad"""
    return render(request, 'privacidad.html')

def terminos(request):
    """Página de Términos y Condiciones"""
    return render(request, 'terminos.html')

def asesoria(request):
    """Vista para la página de asesoría"""
    from .models import ConsultaAsesoria
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        email = request.POST.get('email', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        duda = request.POST.get('duda', '').strip()
        
        if not all([nombre, email, telefono, duda]):
            return render(request, 'asesoria.html', {
                'mensaje_error': 'Por favor completa todos los campos requeridos.',
                'form': request.POST
            })
        
        try:
            consulta = ConsultaAsesoria.objects.create(
                nombre=nombre,
                email=email,
                telefono=telefono,
                duda=duda,
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:500]
            )
            
            # Notificación al equipo de Pacunato
            try:
                send_mail(
                    subject=f'[Nueva Consulta] {nombre} - Asesoría',
                    message=(
                        f'Nueva consulta de asesoría recibida:\n\n'
                        f'Nombre: {nombre}\n'
                        f'Email: {email}\n'
                        f'Teléfono: {telefono}\n\n'
                        f'Consulta:\n{duda}\n\n'
                        f'ID en base de datos: #{consulta.id}'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=True,
                )
                # Auto-respuesta al usuario
                send_mail(
                    subject='Recibimos tu consulta — Pacunato S.A.',
                    message=(
                        f'Hola {nombre},\n\n'
                        f'Hemos recibido tu consulta y te responderemos en menos de 24 horas.\n\n'
                        f'Tu consulta:\n{duda}\n\n'
                        f'Si tienes una urgencia, escríbenos a info@pacunato.com '
                        f'o por WhatsApp al +507 6441-8437.\n\n'
                        f'Saludos,\nEquipo Pacunato S.A.'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=True,
                )
            except Exception:
                pass

            return render(request, 'asesoria.html', {
                'mensaje_exito': True,
                'nombre': nombre,
                'email': email,
                'telefono': telefono
            })
            
        except Exception as e:
            print(f"Error al procesar consulta de asesoría: {str(e)}")
            
            return render(request, 'asesoria.html', {
                'mensaje_error': 'Hubo un problema al enviar tu consulta. Por favor intenta de nuevo o contáctanos por WhatsApp.',
                'form': request.POST
            })
    
    return render(request, 'asesoria.html')

def cotizacion(request):
    """Vista para procesar el formulario de cotización"""
    from .models import SolicitudCotizacion
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        empresa = request.POST.get('empresa', '').strip()
        email = request.POST.get('email', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        pais_origen = request.POST.get('pais_origen', '').strip()
        pais_destino = request.POST.get('pais_destino', '').strip()
        tipo_servicio = request.POST.get('tipo_servicio', '').strip()
        mensaje = request.POST.get('mensaje', '').strip()
        
        if not all([nombre, email, telefono, pais_origen, pais_destino, tipo_servicio, mensaje]):
            messages.error(request, 'Por favor completa todos los campos requeridos.')
            return redirect('website:home')
        
        try:
            solicitud = SolicitudCotizacion.objects.create(
                nombre=nombre,
                empresa=empresa,
                email=email,
                telefono=telefono,
                pais_origen=pais_origen,
                pais_destino=pais_destino,
                tipo_servicio=tipo_servicio,
                mensaje=mensaje,
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:500]
            )
            
            # Notificación al equipo de Pacunato
            try:
                empresa_str = f' ({empresa})' if empresa else ''
                send_mail(
                    subject=f'[Nueva Cotización] {nombre}{empresa_str} — {pais_origen} → {pais_destino}',
                    message=(
                        f'Nueva solicitud de cotización recibida:\n\n'
                        f'Nombre: {nombre}\n'
                        f'Empresa: {empresa or "No especificada"}\n'
                        f'Email: {email}\n'
                        f'Teléfono: {telefono}\n'
                        f'Ruta: {pais_origen} → {pais_destino}\n'
                        f'Servicio: {tipo_servicio}\n\n'
                        f'Descripción:\n{mensaje}\n\n'
                        f'ID en base de datos: #{solicitud.id}'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=True,
                )
                # Auto-respuesta al usuario
                send_mail(
                    subject='Recibimos tu solicitud de cotización — Pacunato S.A.',
                    message=(
                        f'Hola {nombre},\n\n'
                        f'Hemos recibido tu solicitud de cotización para la ruta '
                        f'{pais_origen} → {pais_destino}.\n\n'
                        f'Nuestro equipo la revisará y te contactará en menos de 48 horas.\n\n'
                        f'Si tienes una urgencia, escríbenos a info@pacunato.com '
                        f'o por WhatsApp al +507 6441-8437.\n\n'
                        f'Saludos,\nEquipo Pacunato S.A.'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=True,
                )
            except Exception:
                pass

            messages.success(request, f'¡Gracias {nombre}! Tu solicitud ha sido enviada.')
            return redirect('website:home')
            
        except Exception as e:
            print(f"Error al procesar cotización: {str(e)}")
            messages.error(request, 'Hubo un problema al enviar tu solicitud.')
            return redirect('website:home')
    
    return redirect('website:home')

@csrf_exempt
@require_POST
def suscribir_newsletter(request):
    """Vista para suscripción al newsletter"""
    from .models import NewsletterSubscriber
    
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip().lower()
        name = data.get('name', '').strip()
        
        if not email:
            return JsonResponse({
                'success': False,
                'message': 'El email es requerido'
            }, status=400)
        
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            return JsonResponse({
                'success': False,
                'message': 'Email inválido'
            }, status=400)
        
        ip_address = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        source_page = data.get('page', request.META.get('HTTP_REFERER', ''))
        
        subscriber, created = NewsletterSubscriber.objects.get_or_create(
            email=email,
            defaults={
                'name': name,
                'is_active': True,
                'ip_address': ip_address,
                'user_agent': user_agent,
                'source_page': source_page,
                'consent_given': True,
                'consent_date': timezone.now()
            }
        )
        
        if created:
            message = '¡Gracias por suscribirte!'
            is_new = True
        else:
            if subscriber.is_active:
                return JsonResponse({
                    'success': False,
                    'message': 'Este email ya está suscrito'
                }, status=400)
            else:
                subscriber.is_active = True
                subscriber.unsubscribed_date = None
                subscriber.consent_date = timezone.now()
                subscriber.name = name if name else subscriber.name
                subscriber.ip_address = ip_address
                subscriber.user_agent = user_agent
                subscriber.source_page = source_page
                subscriber.save()
                message = '¡Bienvenido de nuevo!'
                is_new = False
        
        try:
            enviar_a_make_newsletter(subscriber)
        except Exception as e:
            print(f"⚠️ Error enviando a Make: {str(e)}")
        
        print(f"✅ Newsletter: {email} - {'Nuevo' if is_new else 'Reactivado'}")
        
        return JsonResponse({
            'success': True,
            'message': message
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Datos inválidos'
        }, status=400)
        
    except Exception as e:
        print(f"❌ Error newsletter: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': 'Error al procesar la suscripción'
        }, status=500)

# ============================================
# FUNCIONES AUXILIARES
# ============================================

def enviar_a_make(webhook_url, data):
    """Envía datos al webhook de Make.com"""
    try:
        response = requests.post(
            webhook_url,
            json=data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            print(f"✅ Datos enviados a Make: {data.get('tipo')}")
            return True
        else:
            print(f"⚠️ Error Make. Status: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("⚠️ Timeout Make")
        return False
    except Exception as e:
        print(f"⚠️ Error Make: {str(e)}")
        return False

def enviar_a_make_newsletter(subscriber):
    """Envía datos de newsletter a Make"""
    MAKE_WEBHOOK_URL = ''
    
    if not MAKE_WEBHOOK_URL:
        print("ℹ️ Make webhook no configurado")
        return
    
    payload = {
        'email': subscriber.email,
        'name': subscriber.name,
        'timestamp': subscriber.subscribed_date.isoformat(),
        'ip_address': subscriber.ip_address,
        'user_agent': subscriber.user_agent,
        'source': subscriber.source_page,
        'is_new': subscriber.subscribed_date == subscriber.consent_date,
        'consent': subscriber.consent_given,
        'language': 'es',
        'company': 'Pacunato S.A.'
    }
    
    try:
        response = requests.post(
            MAKE_WEBHOOK_URL,
            json=payload,
            timeout=5
        )
        
        if response.status_code == 200:
            subscriber.sent_to_make = True
            subscriber.save()
            print(f"✅ Enviado a Make: {subscriber.email}")
        else:
            print(f"⚠️ Make error: {response.status_code}")
            
    except requests.exceptions.Timeout:
        print(f"⚠️ Timeout Make")
    except Exception as e:
        print(f"⚠️ Error Make: {str(e)}")

def get_client_ip(request):
    """Obtiene la IP real del cliente"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# ============================================
# SEO: SITEMAP.XML Y ROBOTS.TXT
# ============================================

def sitemap_xml(request):
    """
    Genera sitemap.xml dinámico con todas las URLs del sitio
    Incluye páginas estáticas y posts del blog
    """
    from django.http import HttpResponse
    from django.urls import reverse
    from .models import BlogPost
    from datetime import datetime

    # Dominio base (cambiar cuando tengas dominio real)
    base_url = 'https://www.pacunato.com'

    # URLs estáticas con prioridades
    static_urls = [
        {'loc': reverse('website:home'), 'priority': '1.0', 'changefreq': 'daily'},
        {'loc': reverse('website:servicios'), 'priority': '0.9', 'changefreq': 'weekly'},
        {'loc': reverse('website:nosotros'), 'priority': '0.8', 'changefreq': 'monthly'},
        {'loc': reverse('website:blog'), 'priority': '0.8', 'changefreq': 'daily'},
        {'loc': reverse('website:contacto'), 'priority': '0.7', 'changefreq': 'monthly'},
        {'loc': reverse('website:asesoria'), 'priority': '0.7', 'changefreq': 'monthly'},
        {'loc': reverse('website:cotizacion'), 'priority': '0.7', 'changefreq': 'monthly'},
        {'loc': reverse('website:privacidad'), 'priority': '0.3', 'changefreq': 'yearly'},
        {'loc': reverse('website:terminos'), 'priority': '0.3', 'changefreq': 'yearly'},
    ]

    # Blog posts dinámicos
    blog_posts = BlogPost.objects.filter(is_published=True).order_by('-created_at')

    # Generar XML
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    # Agregar URLs estáticas
    for url in static_urls:
        xml.append('  <url>')
        xml.append(f'    <loc>{base_url}{url["loc"]}</loc>')
        xml.append(f'    <changefreq>{url["changefreq"]}</changefreq>')
        xml.append(f'    <priority>{url["priority"]}</priority>')
        xml.append(f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>')
        xml.append('  </url>')

    # Agregar blog posts
    for post in blog_posts:
        post_url = reverse('website:blog_post', kwargs={'slug': post.slug})
        xml.append('  <url>')
        xml.append(f'    <loc>{base_url}{post_url}</loc>')
        xml.append(f'    <changefreq>weekly</changefreq>')
        xml.append(f'    <priority>0.6</priority>')
        xml.append(f'    <lastmod>{post.updated_at.strftime("%Y-%m-%d")}</lastmod>')
        xml.append('  </url>')

    xml.append('</urlset>')

    return HttpResponse('\n'.join(xml), content_type='application/xml')

def robots_txt(request):
    """
    Genera robots.txt optimizado para SEO
    Permite todos los crawlers y apunta al sitemap
    """
    from django.http import HttpResponse

    lines = [
        "# robots.txt for Pacunato S.A.",
        "# Permitir todos los bots de búsqueda",
        "",
        "User-agent: *",
        "Allow: /",
        "",
        "# Bloquear admin y áreas privadas",
        "Disallow: /admin/",
        "Disallow: /api/",
        "Disallow: /media/private/",
        "",
        "# Googlebot específico",
        "User-agent: Googlebot",
        "Allow: /",
        "Crawl-delay: 0",
        "",
        "# Bingbot",
        "User-agent: Bingbot",
        "Allow: /",
        "Crawl-delay: 0",
        "",
        "# Sitemap",
        "Sitemap: https://www.pacunato.com/sitemap.xml",
        "",
        "# Host preferido (con www)",
        "Host: https://www.pacunato.com",
    ]

    return HttpResponse('\n'.join(lines), content_type='text/plain')