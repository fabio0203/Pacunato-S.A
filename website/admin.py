from django.contrib import admin
from .models import (
    BlogPost, BlogTag, BlogPostView,
    ConsultaAsesoria, SolicitudCotizacion, 
    NewsletterSubscriber
)

# ============================================
# ADMIN DE BLOG
# ============================================

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    """
    Panel de administración para artículos del blog
    ⭐ MEJORADO: Incluye estadísticas de vistas únicas
    """
    list_display = [
        'title', 
        'category', 
        'is_featured', 
        'is_published', 
        'views',  # ⭐ Vistas totales
        'get_unique_views',  # ⭐ NUEVO: Vistas únicas (por IP)
        'created_at'
    ]
    list_filter = ['category', 'is_featured', 'is_published', 'created_at']
    search_fields = ['title', 'excerpt', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_featured', 'is_published']
    date_hierarchy = 'created_at'
    
    readonly_fields = ['views', 'created_at', 'updated_at', 'get_unique_views_detail']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('title', 'slug', 'excerpt', 'content')
        }),
        ('Multimedia', {
            'fields': ('featured_image',)
        }),
        ('Categorización', {
            'fields': ('category', 'tags', 'author', 'read_time')
        }),
        ('Estado', {
            'fields': ('is_featured', 'is_published')
        }),
        ('Estadísticas', {
            'fields': ('views', 'get_unique_views_detail', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_unique_views(self, obj):
        """Muestra el número de vistas únicas (IPs diferentes)"""
        unique_count = obj.unique_views.count()
        return f"{unique_count} únicas"
    get_unique_views.short_description = 'Vistas Únicas'
    
    def get_unique_views_detail(self, obj):
        """Muestra estadísticas detalladas de vistas"""
        total_views = obj.views
        unique_count = obj.unique_views.count()
        
        if unique_count > 0:
            repeated_views = total_views - unique_count
            return f"""
            📊 Estadísticas de Vistas:
            • Total de vistas: {total_views}
            • Visitantes únicos: {unique_count}
            • Vistas repetidas: {repeated_views}
            """
        else:
            return f"Total de vistas: {total_views} (sistema de tracking iniciando)"
    get_unique_views_detail.short_description = 'Detalle de Vistas'


@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    """Panel de administración para etiquetas"""
    list_display = ['name', 'slug', 'get_posts_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    
    def get_posts_count(self, obj):
        """Muestra cuántos posts tienen esta etiqueta"""
        count = obj.posts.count()
        return f"{count} post(s)"
    get_posts_count.short_description = 'Artículos'


@admin.register(BlogPostView)
class BlogPostViewAdmin(admin.ModelAdmin):
    """
    ⭐ NUEVO: Panel de administración para vistas de artículos
    Permite ver qué IPs visitaron cada post
    """
    list_display = ['post', 'ip_address', 'viewed_at', 'get_location_hint']
    list_filter = ['viewed_at', 'post']
    search_fields = ['ip_address', 'user_agent', 'post__title']
    date_hierarchy = 'viewed_at'
    readonly_fields = ['post', 'ip_address', 'user_agent', 'viewed_at']
    
    fieldsets = (
        ('Información de Vista', {
            'fields': ('post', 'ip_address', 'viewed_at')
        }),
        ('Detalles Técnicos', {
            'fields': ('user_agent',),
            'classes': ('collapse',)
        }),
    )
    
    def get_location_hint(self, obj):
        """Muestra el tipo de dispositivo basado en user_agent"""
        ua = obj.user_agent.lower()
        
        if 'mobile' in ua or 'android' in ua or 'iphone' in ua:
            return "📱 Móvil"
        elif 'tablet' in ua or 'ipad' in ua:
            return "📱 Tablet"
        else:
            return "💻 Desktop"
    get_location_hint.short_description = 'Dispositivo'
    
    def has_add_permission(self, request):
        """No permitir agregar vistas manualmente"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """No permitir editar vistas (son automáticas)"""
        return False


# ============================================
# ADMIN DE FORMULARIOS
# ============================================

@admin.register(ConsultaAsesoria)
class ConsultaAsesoriaAdmin(admin.ModelAdmin):
    """Panel de administración para Consultas de Asesoría"""
    list_display = [
        'nombre', 
        'email', 
        'telefono', 
        'fecha_envio', 
        'procesado', 
        'enviado_make'
    ]
    list_filter = ['procesado', 'enviado_make', 'fecha_envio']
    search_fields = ['nombre', 'email', 'telefono', 'duda']
    readonly_fields = ['fecha_envio', 'ip_address', 'user_agent', 'fecha_procesamiento']
    
    fieldsets = (
        ('Información del Cliente', {
            'fields': ('nombre', 'email', 'telefono', 'duda')
        }),
        ('Metadata', {
            'fields': ('fecha_envio', 'ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
        ('Estado', {
            'fields': ('procesado', 'enviado_make', 'fecha_procesamiento', 'notas_admin')
        }),
    )
    
    actions = ['marcar_como_procesado', 'marcar_como_no_procesado']
    
    def marcar_como_procesado(self, request, queryset):
        """Marcar consultas seleccionadas como procesadas"""
        updated = queryset.update(procesado=True)
        self.message_user(request, f'{updated} consulta(s) marcada(s) como procesada(s).')
    marcar_como_procesado.short_description = "✅ Marcar como procesado"
    
    def marcar_como_no_procesado(self, request, queryset):
        """Marcar consultas seleccionadas como no procesadas"""
        updated = queryset.update(procesado=False)
        self.message_user(request, f'{updated} consulta(s) marcada(s) como no procesada(s).')
    marcar_como_no_procesado.short_description = "❌ Marcar como NO procesado"


@admin.register(SolicitudCotizacion)
class SolicitudCotizacionAdmin(admin.ModelAdmin):
    """Panel de administración para Solicitudes de Cotización"""
    list_display = [
        'nombre', 
        'empresa', 
        'email', 
        'telefono', 
        'get_ruta_display',
        'tipo_servicio', 
        'fecha_envio', 
        'procesado', 
        'enviado_make'
    ]
    
    list_filter = [
        'procesado', 
        'enviado_make', 
        'tipo_servicio', 
        'pais_origen',
        'pais_destino',
        'fecha_envio'
    ]
    
    search_fields = [
        'nombre', 
        'empresa', 
        'email', 
        'telefono', 
        'pais_origen',
        'pais_destino',
        'mensaje'
    ]
    
    readonly_fields = ['fecha_envio', 'ip_address', 'user_agent', 'fecha_procesamiento']
    
    fieldsets = (
        ('Información del Cliente', {
            'fields': ('nombre', 'empresa', 'email', 'telefono')
        }),
        ('📍 Ruta de Envío', {
            'fields': ('pais_origen', 'pais_destino'),
            'description': 'País de origen (donde se compra) → País de destino (donde se entrega)'
        }),
        ('Detalles del Servicio', {
            'fields': ('tipo_servicio', 'mensaje')
        }),
        ('Metadata', {
            'fields': ('fecha_envio', 'ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
        ('Estado', {
            'fields': ('procesado', 'enviado_make', 'fecha_procesamiento', 'notas_admin')
        }),
    )
    
    actions = ['marcar_como_procesado', 'marcar_como_no_procesado', 'exportar_a_csv']
    
    def get_ruta_display(self, obj):
        """Muestra la ruta origen → destino"""
        return f"🛫 {obj.pais_origen} → 🛬 {obj.pais_destino}"
    get_ruta_display.short_description = 'Ruta'
    
    def marcar_como_procesado(self, request, queryset):
        """Marcar solicitudes seleccionadas como procesadas"""
        updated = queryset.update(procesado=True)
        self.message_user(request, f'{updated} solicitud(es) marcada(s) como procesada(s).')
    marcar_como_procesado.short_description = "✅ Marcar como procesado"
    
    def marcar_como_no_procesado(self, request, queryset):
        """Marcar solicitudes seleccionadas como no procesadas"""
        updated = queryset.update(procesado=False)
        self.message_user(request, f'{updated} solicitud(es) marcada(s) como no procesada(s).')
    marcar_como_no_procesado.short_description = "❌ Marcar como NO procesado"
    
    def exportar_a_csv(self, request, queryset):
        """Exportar solicitudes seleccionadas a CSV"""
        import csv
        from django.http import HttpResponse
        from datetime import datetime
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="cotizaciones_{datetime.now().strftime("%Y%m%d")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Fecha', 'Nombre', 'Empresa', 'Email', 'Teléfono', 
            'País Origen', 'País Destino', 'Tipo Servicio', 'Mensaje', 'Procesado'
        ])
        
        for solicitud in queryset:
            writer.writerow([
                solicitud.fecha_envio.strftime('%Y-%m-%d %H:%M'),
                solicitud.nombre,
                solicitud.empresa,
                solicitud.email,
                solicitud.telefono,
                solicitud.pais_origen,
                solicitud.pais_destino,
                solicitud.tipo_servicio,
                solicitud.mensaje,
                'Sí' if solicitud.procesado else 'No'
            ])
        
        self.message_user(request, f'{queryset.count()} solicitud(es) exportada(s) a CSV.')
        return response
    exportar_a_csv.short_description = "📥 Exportar a CSV"


# ============================================
# ADMIN DE NEWSLETTER
# ============================================

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    """Panel de administración para suscriptores del newsletter"""
    list_display = [
        'email', 
        'name', 
        'subscribed_date', 
        'is_active', 
        'sent_to_make'
    ]
    list_filter = ['is_active', 'sent_to_make', 'subscribed_date']
    search_fields = ['email', 'name']
    readonly_fields = ['subscribed_date', 'consent_date', 'ip_address']
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('email', 'name')
        }),
        ('Estado', {
            'fields': ('is_active', 'subscribed_date', 'unsubscribed_date')
        }),
        ('Tracking', {
            'fields': ('ip_address', 'user_agent', 'source_page', 'sent_to_make'),
            'classes': ('collapse',)
        }),
        ('Consentimiento', {
            'fields': ('consent_given', 'consent_date'),
            'classes': ('collapse',)
        }),
        ('Notas', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['export_emails', 'reenviar_a_make', 'reactivar_suscriptores']
    
    def export_emails(self, request, queryset):
        """Exportar emails activos"""
        emails = queryset.filter(is_active=True).values_list('email', flat=True)
        emails_str = '\n'.join(emails)
        self.message_user(request, f'{len(emails)} emails activos copiados.')
    export_emails.short_description = "📧 Exportar emails activos"
    
    def reenviar_a_make(self, request, queryset):
        """Reenviar suscriptores a Make"""
        from .views import enviar_a_make_newsletter
        count = 0
        for subscriber in queryset:
            try:
                enviar_a_make_newsletter(subscriber)
                subscriber.sent_to_make = True
                subscriber.save()
                count += 1
            except Exception as e:
                print(f"Error reenviando {subscriber.email}: {str(e)}")
        self.message_user(request, f'{count} suscriptor(es) reenviado(s) a Make.')
    reenviar_a_make.short_description = "🔄 Reenviar a Make"
    
    def reactivar_suscriptores(self, request, queryset):
        """Reactivar suscriptores seleccionados"""
        count = queryset.update(
            is_active=True,
            unsubscribed_date=None
        )
        self.message_user(request, f'{count} suscriptor(es) reactivado(s).')
    reactivar_suscriptores.short_description = '✅ Reactivar suscriptores'