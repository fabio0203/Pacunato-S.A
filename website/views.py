from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail, EmailMessage
import json
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

            # Registrar en Google Sheets
            from .sheets import log_to_sheets
            log_to_sheets('Asesoria', [
                timezone.now().strftime('%Y-%m-%d %H:%M'),
                nombre, email, telefono, duda
            ])

            # Notificación al equipo de Pacunato
            try:
                msg = EmailMessage(
                    subject=f'[Nueva Consulta de Asesoría] {nombre} — {email}',
                    body=(
                        f'Tipo: Consulta de Asesoría\n\n'
                        f'Nombre: {nombre}\n'
                        f'Email: {email}\n'
                        f'Teléfono: {telefono}\n\n'
                        f'Consulta:\n{duda}\n\n'
                        f'ID en base de datos: #{consulta.id}'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.CONTACT_EMAIL],
                    reply_to=[email],
                )
                msg.send(fail_silently=False)
                print(f"✅ Email equipo enviado — Asesoría #{consulta.id}")
            except Exception as e:
                print(f"⚠️ Error email equipo (Asesoría): {str(e)}")

            # Auto-respuesta al usuario
            try:
                send_mail(
                    subject='Recibimos tu consulta — Pacunato S.A.',
                    message=(
                        f'Hola {nombre},\n\n'
                        f'gracias por contactarnos, en breve nuestro equipo se pondrá en contacto.\n\n'
                        f'Tu consulta:\n{duda}\n\n'
                        f'Si tienes una urgencia, escríbenos a info@pacunato.com '
                        f'o por WhatsApp al +507 6441-8437.\n\n'
                        f'Saludos,\nEquipo Pacunato S.A.'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )
                print(f"✅ Email cliente enviado — Asesoría #{consulta.id} → {email}")
            except Exception as e:
                print(f"⚠️ Error email cliente (Asesoría): {str(e)}")

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

            # Registrar en Google Sheets
            from .sheets import log_to_sheets
            log_to_sheets('Cotizacion', [
                timezone.now().strftime('%Y-%m-%d %H:%M'),
                nombre, empresa, email, telefono,
                pais_origen, pais_destino, tipo_servicio, mensaje
            ])

            # Notificación al equipo de Pacunato
            empresa_str = f' ({empresa})' if empresa else ''
            try:
                msg = EmailMessage(
                    subject=f'[Nueva Cotización] {nombre}{empresa_str} — {pais_origen} → {pais_destino}',
                    body=(
                        f'Tipo: Solicitud de Cotización\n\n'
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
                    to=[settings.CONTACT_EMAIL],
                    reply_to=[email],
                )
                msg.send(fail_silently=False)
                print(f"✅ Email equipo enviado — Cotización #{solicitud.id}")
            except Exception as e:
                print(f"⚠️ Error email equipo (Cotización): {str(e)}")

            # Auto-respuesta al usuario
            try:
                send_mail(
                    subject='Recibimos tu solicitud de cotización — Pacunato S.A.',
                    message=(
                        f'Hola {nombre},\n\n'
                        f'gracias por contactarnos, en breve nuestro equipo se pondrá en contacto.\n\n'
                        f'Tu solicitud de cotización para la ruta {pais_origen} → {pais_destino} ha sido recibida.\n\n'
                        f'Si tienes una urgencia, escríbenos a info@pacunato.com '
                        f'o por WhatsApp al +507 6441-8437.\n\n'
                        f'Saludos,\nEquipo Pacunato S.A.'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )
                print(f"✅ Email cliente enviado — Cotización #{solicitud.id} → {email}")
            except Exception as e:
                print(f"⚠️ Error email cliente (Cotización): {str(e)}")

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
    """Vista para suscripción al newsletter y solicitud de guía"""
    from .models import NewsletterSubscriber

    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip().lower()
        name = data.get('name', '').strip()
        source = data.get('source', data.get('page', request.META.get('HTTP_REFERER', '')))

        if not email:
            return JsonResponse({'success': False, 'message': 'El email es requerido'}, status=400)

        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            return JsonResponse({'success': False, 'message': 'Email inválido'}, status=400)

        ip_address = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        es_guia = source == 'home-lead-magnet'

        subscriber, created = NewsletterSubscriber.objects.get_or_create(
            email=email,
            defaults={
                'name': name,
                'is_active': True,
                'ip_address': ip_address,
                'user_agent': user_agent,
                'source_page': source,
                'consent_given': True,
                'consent_date': timezone.now()
            }
        )

        if created:
            message = '¡Gracias! Revisa tu correo.' if es_guia else '¡Gracias por suscribirte!'
            is_new = True
        else:
            if subscriber.is_active and not es_guia:
                return JsonResponse({'success': False, 'message': 'Este email ya está suscrito'}, status=400)
            subscriber.is_active = True
            subscriber.unsubscribed_date = None
            subscriber.consent_date = timezone.now()
            subscriber.name = name if name else subscriber.name
            subscriber.ip_address = ip_address
            subscriber.user_agent = user_agent
            subscriber.source_page = source
            subscriber.save()
            message = '¡Gracias! Revisa tu correo.' if es_guia else '¡Bienvenido de nuevo!'
            is_new = False

        nombre_display = name if name else 'Cliente'

        # Registrar en Google Sheets
        from .sheets import log_to_sheets
        if es_guia:
            log_to_sheets('Guia', [
                timezone.now().strftime('%Y-%m-%d %H:%M'),
                nombre_display, email
            ])
        else:
            log_to_sheets('Newsletter', [
                timezone.now().strftime('%Y-%m-%d %H:%M'),
                nombre_display, email, source
            ])

        # --- Email a info@pacunato.com ---
        try:
            tipo_label = 'Solicitud de Guía de Importación' if es_guia else 'Suscripción al Newsletter'
            msg = EmailMessage(
                subject=f'[{tipo_label}] {nombre_display} — {email}',
                body=(
                    f'Tipo: {tipo_label}\n\n'
                    f'Nombre: {nombre_display}\n'
                    f'Email: {email}\n'
                    f'Fuente: {source}\n'
                    f'Estado: {"Nuevo suscriptor" if is_new else "Suscriptor reactivado"}\n'
                    f'IP: {ip_address}'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.CONTACT_EMAIL],
                reply_to=[email],
            )
            msg.send(fail_silently=False)
        except Exception as e:
            print(f"⚠️ Error email interno: {str(e)}")

        # --- Auto-respuesta al usuario ---
        try:
            if es_guia:
                # Email con la guía de importación
                asunto_usuario = 'Tu Guía de Importación — Pacunato S.A.'
                cuerpo_usuario = (
                    f'Hola {nombre_display},\n\n'
                    f'gracias por tu interés en Pacunato S.A. Aquí está tu guía completa sobre cómo importar a Cuba desde Panamá.\n\n'
                    f'━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
                    f'CÓMO IMPORTAR A CUBA DESDE PANAMÁ\n'
                    f'Guía Completa para Empresas — 2026\n'
                    f'━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n'
                    f'Panamá, con su Zona Libre de Colón — la segunda zona franca más grande del mundo — '
                    f'actúa como hub natural para abastecer a empresas e importadoras cubanas con productos de todo el mundo.\n\n'
                    f'¿POR QUÉ PANAMÁ ES EL PUNTO DE PARTIDA IDEAL?\n\n'
                    f'• Zona Libre de Colón: más de 2,600 empresas operando, acceso a productos de Asia, Europa y Norteamérica\n'
                    f'• Conectividad marítima directa: rutas regulares hacia el Puerto de Mariel y Puerto de La Habana\n'
                    f'• Infraestructura logística avanzada: operadores y agencias con experiencia en la ruta Panamá–Cuba\n'
                    f'• Ubicación estratégica: menos de 3 días de tránsito marítimo desde Panamá a Cuba\n\n'
                    f'PROCESO PASO A PASO\n\n'
                    f'1. Identificar el producto y el proveedor\n'
                    f'   Desde Panamá puedes acceder a proveedores globales. En Pacunato buscamos y verificamos proveedores para que no tengas que hacerlo tú.\n\n'
                    f'2. Verificar que el producto puede ingresar a Cuba\n'
                    f'   Cuba tiene restricciones para ciertos productos. Verificamos permisos del MINSAP, MINAG o CITMA según el caso.\n\n'
                    f'3. Identificar la entidad importadora en Cuba\n'
                    f'   Sin el receptor legal correcto, la mercancía no entra. Conocemos el ecosistema cubano y te orientamos desde el primer día.\n\n'
                    f'4. Cotizar el flete\n'
                    f'   • LCL (consolidada): ideal para volúmenes pequeños, reduce costos\n'
                    f'   • FCL (contenedor completo): para volúmenes mayores, mayor control\n'
                    f'   Tiempo de tránsito: 3 a 7 días desde Panamá.\n\n'
                    f'5. Preparar la documentación\n'
                    f'   Factura comercial, packing list, Bill of Lading, certificado de origen, permisos sanitarios y contrato comercial.\n\n'
                    f'6. Despacho aduanero en Cuba\n'
                    f'   Lo gestiona la entidad importadora cubana con su agente de aduana local.\n\n'
                    f'ERRORES MÁS COMUNES (Y CÓMO EVITARLOS)\n\n'
                    f'✗ No verificar al receptor cubano — puede bloquear toda la operación\n'
                    f'✗ Subestimar los tiempos — el proceso completo toma 30 a 90 días\n'
                    f'✗ No documentar el origen de los fondos — las transacciones en MLC requieren trazabilidad\n'
                    f'✗ No consolidar la carga — pierdes dinero enviando contenedores a medio llenar\n\n'
                    f'━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n'
                    f'¿Listo para importar? En Pacunato S.A. nos encargamos de todo el proceso.\n'
                    f'Solicita tu cotización gratuita en: https://www.pacunato.com/#cotizacion\n\n'
                    f'━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
                    f'DATOS DE CONTACTO\n'
                    f'━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
                    f'Pacunato S.A.\n'
                    f'Email: info@pacunato.com\n'
                    f'WhatsApp: +507 6441-8437\n'
                    f'Web: https://www.pacunato.com\n\n'
                    f'De vez en cuando nuestro equipo te enviará recomendaciones, novedades del sector '
                    f'y contenido de interés sobre importaciones y comercio internacional.\n\n'
                    f'Saludos,\nEquipo Pacunato S.A.'
                )
            else:
                # Email de bienvenida al newsletter
                asunto_usuario = 'Bienvenido al Newsletter de Pacunato S.A.'
                cuerpo_usuario = (
                    f'Hola {nombre_display},\n\n'
                    f'gracias por suscribirte. A partir de ahora recibirás de nuestra parte:\n\n'
                    f'• Guías prácticas sobre importaciones y logística internacional\n'
                    f'• Novedades del sector de comercio exterior en Panamá y Centroamérica\n'
                    f'• Consejos para optimizar tus operaciones de importación\n'
                    f'• Oportunidades y tendencias del mercado\n\n'
                    f'Si en algún momento necesitas importar o tienes alguna consulta, estamos aquí para ayudarte.\n\n'
                    f'━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
                    f'DATOS DE CONTACTO\n'
                    f'━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
                    f'Pacunato S.A.\n'
                    f'Email: info@pacunato.com\n'
                    f'WhatsApp: +507 6441-8437\n'
                    f'Web: https://www.pacunato.com\n\n'
                    f'Saludos,\nEquipo Pacunato S.A.'
                )

            send_mail(
                subject=asunto_usuario,
                message=cuerpo_usuario,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"⚠️ Error email usuario: {str(e)}")

        print(f"✅ Newsletter: {email} — {'Guía' if es_guia else 'Newsletter'} — {'Nuevo' if is_new else 'Reactivado'}")

        return JsonResponse({'success': True, 'message': message})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Datos inválidos'}, status=400)

    except Exception as e:
        print(f"❌ Error newsletter: {str(e)}")
        return JsonResponse({'success': False, 'message': 'Error al procesar la suscripción'}, status=500)

# ============================================
# FUNCIONES AUXILIARES
# ============================================

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