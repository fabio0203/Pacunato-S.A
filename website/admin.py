from django.contrib import admin
from .models import (
    BlogPost, BlogTag, BlogPostView,
    ConsultaAsesoria, SolicitudCotizacion,
    NewsletterSubscriber, SolicitudGuia
)

# ============================================
# ADMIN DE BLOG
# ============================================

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'category',
        'is_featured',
        'is_published',
        'views',
        'get_unique_views',
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
            'fields': ('featured_image', 'featured_image_url')
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
        return f"{obj.unique_views.count()} únicas"
    get_unique_views.short_description = 'Vistas Únicas'

    def get_unique_views_detail(self, obj):
        total_views = obj.views
        unique_count = obj.unique_views.count()
        if unique_count > 0:
            return f"Total: {total_views} | Únicos: {unique_count} | Repetidas: {total_views - unique_count}"
        return f"Total de vistas: {total_views}"
    get_unique_views_detail.short_description = 'Detalle de Vistas'


@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'get_posts_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

    def get_posts_count(self, obj):
        return f"{obj.posts.count()} post(s)"
    get_posts_count.short_description = 'Artículos'


@admin.register(BlogPostView)
class BlogPostViewAdmin(admin.ModelAdmin):
    list_display = ['post', 'ip_address', 'viewed_at', 'get_dispositivo']
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

    def get_dispositivo(self, obj):
        ua = obj.user_agent.lower()
        if 'mobile' in ua or 'android' in ua or 'iphone' in ua:
            return "Móvil"
        elif 'tablet' in ua or 'ipad' in ua:
            return "Tablet"
        return "Desktop"
    get_dispositivo.short_description = 'Dispositivo'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


# ============================================
# ADMIN DE FORMULARIOS
# ============================================

@admin.register(ConsultaAsesoria)
class ConsultaAsesoriaAdmin(admin.ModelAdmin):
    list_display = [
        'nombre',
        'email',
        'telefono',
        'fecha_envio',
        'procesado',
    ]
    list_filter = ['procesado', 'fecha_envio']
    search_fields = ['nombre', 'email', 'telefono', 'duda']
    readonly_fields = ['fecha_envio', 'ip_address', 'user_agent', 'fecha_procesamiento']

    fieldsets = (
        ('Información del Cliente', {
            'fields': ('nombre', 'email', 'telefono', 'duda')
        }),
        ('Estado', {
            'fields': ('procesado', 'fecha_procesamiento', 'notas_admin')
        }),
        ('Metadata', {
            'fields': ('fecha_envio', 'ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
    )

    actions = ['marcar_como_procesado', 'marcar_como_no_procesado']

    def marcar_como_procesado(self, request, queryset):
        updated = queryset.update(procesado=True)
        self.message_user(request, f'{updated} consulta(s) marcada(s) como procesada(s).')
    marcar_como_procesado.short_description = "Marcar como procesado"

    def marcar_como_no_procesado(self, request, queryset):
        updated = queryset.update(procesado=False)
        self.message_user(request, f'{updated} consulta(s) marcada(s) como no procesada(s).')
    marcar_como_no_procesado.short_description = "Marcar como NO procesado"


@admin.register(SolicitudCotizacion)
class SolicitudCotizacionAdmin(admin.ModelAdmin):
    list_display = [
        'nombre',
        'empresa',
        'email',
        'telefono',
        'get_ruta_display',
        'tipo_servicio',
        'get_fuente_badge',
        'fecha_envio',
        'procesado',
    ]

    list_filter = [
        'procesado',
        'tipo_servicio',
        'pais_destino',
        'source_page',
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

    readonly_fields = ['fecha_envio', 'ip_address', 'user_agent', 'fecha_procesamiento', 'source_page']

    fieldsets = (
        ('Información del Cliente', {
            'fields': ('nombre', 'empresa', 'email', 'telefono')
        }),
        ('Ruta de Envío', {
            'fields': ('pais_origen', 'pais_destino'),
            'description': 'País de origen → País de destino'
        }),
        ('Detalles del Servicio', {
            'fields': ('tipo_servicio', 'mensaje')
        }),
        ('Estado', {
            'fields': ('procesado', 'fecha_procesamiento', 'notas_admin')
        }),
        ('Origen de la Solicitud', {
            'fields': ('source_page',),
        }),
        ('Metadata', {
            'fields': ('fecha_envio', 'ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
    )

    def get_fuente_badge(self, obj):
        from django.utils.html import format_html
        fuente = obj.source_page or ''
        if fuente == 'landing-importacion':
            return format_html(
                '<span style="background:#00B4D8;color:#000;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:700;">⭐ LANDING</span>'
            )
        elif fuente:
            return format_html(
                '<span style="background:#444;color:#fff;padding:2px 8px;border-radius:4px;font-size:11px;">{}</span>',
                fuente
            )
        return format_html(
            '<span style="color:#888;font-size:11px;">Home</span>'
        )
    get_fuente_badge.short_description = 'Fuente'

    actions = ['marcar_como_procesado', 'marcar_como_no_procesado', 'exportar_a_csv']

    def get_ruta_display(self, obj):
        return f"{obj.pais_origen} → {obj.pais_destino}"
    get_ruta_display.short_description = 'Ruta'

    def marcar_como_procesado(self, request, queryset):
        updated = queryset.update(procesado=True)
        self.message_user(request, f'{updated} solicitud(es) marcada(s) como procesada(s).')
    marcar_como_procesado.short_description = "Marcar como procesado"

    def marcar_como_no_procesado(self, request, queryset):
        updated = queryset.update(procesado=False)
        self.message_user(request, f'{updated} solicitud(es) marcada(s) como no procesada(s).')
    marcar_como_no_procesado.short_description = "Marcar como NO procesado"

    def exportar_a_csv(self, request, queryset):
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

        for s in queryset:
            writer.writerow([
                s.fecha_envio.strftime('%Y-%m-%d %H:%M'),
                s.nombre, s.empresa, s.email, s.telefono,
                s.pais_origen, s.pais_destino, s.tipo_servicio,
                s.mensaje, 'Sí' if s.procesado else 'No'
            ])

        self.message_user(request, f'{queryset.count()} solicitud(es) exportada(s) a CSV.')
        return response
    exportar_a_csv.short_description = "Exportar a CSV"


# ============================================
# ADMIN DE NEWSLETTER
# ============================================

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = [
        'email',
        'name',
        'source_page',
        'subscribed_date',
        'is_active',
    ]
    list_filter = ['is_active', 'subscribed_date', 'source_page']
    search_fields = ['email', 'name']
    readonly_fields = ['subscribed_date', 'consent_date', 'ip_address']

    fieldsets = (
        ('Información Personal', {
            'fields': ('email', 'name')
        }),
        ('Estado', {
            'fields': ('is_active', 'subscribed_date', 'unsubscribed_date')
        }),
        ('Origen', {
            'fields': ('source_page',)
        }),
        ('Consentimiento GDPR', {
            'fields': ('consent_given', 'consent_date'),
            'classes': ('collapse',)
        }),
        ('Tracking', {
            'fields': ('ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
        ('Notas', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )

    actions = ['exportar_emails', 'reactivar_suscriptores']

    def exportar_emails(self, request, queryset):
        emails = list(queryset.filter(is_active=True).values_list('email', flat=True))
        self.message_user(request, f'{len(emails)} emails activos: {", ".join(emails[:10])}{"..." if len(emails) > 10 else ""}')
    exportar_emails.short_description = "Ver emails activos"

    def reactivar_suscriptores(self, request, queryset):
        count = queryset.update(is_active=True, unsubscribed_date=None)
        self.message_user(request, f'{count} suscriptor(es) reactivado(s).')
    reactivar_suscriptores.short_description = 'Reactivar suscriptores'


# ============================================
# ADMIN DE SOLICITUDES DE GUÍA DE IMPORTACIÓN
# ============================================

@admin.register(SolicitudGuia)
class SolicitudGuiaAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'subscribed_date', 'is_active']
    list_filter = ['is_active', 'subscribed_date']
    search_fields = ['email', 'name']
    readonly_fields = ['subscribed_date', 'consent_date', 'ip_address', 'source_page']

    fieldsets = (
        ('Datos del Solicitante', {
            'fields': ('email', 'name')
        }),
        ('Estado', {
            'fields': ('is_active', 'subscribed_date')
        }),
        ('Tracking', {
            'fields': ('source_page', 'ip_address'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(source_page='home-lead-magnet')

    def has_add_permission(self, request):
        return False
