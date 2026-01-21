from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
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
    """Vista para la página principal del blog"""
    return render(request, 'blog.html')

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
        
        # ⭐ IMPORTANTE: Solo incrementar si es vista NUEVA
        if view_created:
            post.views += 1  # ← Usa el campo existente 'views'
            post.save()
            print(f"✅ Nueva vista única: {ip_address} - Total: {post.views}")
        else:
            print(f"ℹ️ Vista repetida (no suma): {ip_address} - Total sigue: {post.views}")
            
    except Exception as e:
        print(f"⚠️ Error al registrar vista: {str(e)}")
    
    # Obtener número de visitantes únicos
    unique_visitors = post.unique_views.count()
    
    context = {
        'post': post,
        'view_count': post.views,  # Total de vistas
        'unique_visitors': unique_visitors,  # Visitantes únicos
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
            
            webhook_url = getattr(settings, 'MAKE_WEBHOOK_ASESORIA', None)
            
            if webhook_url:
                enviar_a_make(webhook_url, {
                    'tipo': 'asesoria',
                    'nombre': nombre,
                    'email': email,
                    'telefono': telefono,
                    'duda': duda,
                    'fecha': consulta.fecha_envio.isoformat(),
                    'id_consulta': consulta.id
                })
                consulta.enviado_make = True
                consulta.save()
            
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
            
            webhook_url = getattr(settings, 'MAKE_WEBHOOK_COTIZACION', None)
            
            if webhook_url:
                enviar_a_make(webhook_url, {
                    'tipo': 'cotizacion',
                    'nombre': nombre,
                    'empresa': empresa,
                    'email': email,
                    'telefono': telefono,
                    'pais_origen': pais_origen,
                    'pais_destino': pais_destino,
                    'ruta': f"{pais_origen} → {pais_destino}",
                    'tipo_servicio': tipo_servicio,
                    'mensaje': mensaje,
                    'fecha': solicitud.fecha_envio.isoformat(),
                    'id_solicitud': solicitud.id
                })
                solicitud.enviado_make = True
                solicitud.save()
            
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