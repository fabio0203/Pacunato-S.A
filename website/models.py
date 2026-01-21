from django.db import models
from django.utils.text import slugify
from django.utils import timezone

# ============================================
# MODELOS DE BLOG
# ============================================

class BlogTag(models.Model):
    """Modelo para las etiquetas de los artículos"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Etiqueta"
        verbose_name_plural = "Etiquetas"


class BlogPost(models.Model):
    """Modelo para los artículos del blog"""
    
    CATEGORY_CHOICES = [
        ('eventos', 'Eventos'),
        ('logistica', 'Logística'),
        ('comercio', 'Comercio Internacional'),
        ('tendencias', 'Tendencias'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Título')
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    excerpt = models.TextField(max_length=300, verbose_name='Extracto')
    content = models.TextField(verbose_name='Contenido')
    featured_image = models.ImageField(upload_to='blog/', verbose_name='Imagen Destacada', blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='eventos')
    author = models.CharField(max_length=100, default='Equipo Pacunato')
    read_time = models.IntegerField(default=3, verbose_name='Tiempo de Lectura (min)')
    
    # ⭐ CAMPO EXISTENTE - Se mantiene y se usa para el contador
    views = models.IntegerField(default=0, verbose_name='Vistas')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False, verbose_name='¿Destacado?')
    is_published = models.BooleanField(default=True, verbose_name='¿Publicado?')
    
    # Relación con tags
    tags = models.ManyToManyField(BlogTag, blank=True, related_name='posts')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Artículo'
        verbose_name_plural = 'Artículos'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title


class BlogPostView(models.Model):
    """
    ⭐ NUEVO: Modelo para rastrear vistas únicas por IP
    Evita que una misma IP cuente múltiples veces
    """
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='unique_views')
    ip_address = models.GenericIPAddressField(verbose_name="Dirección IP")
    user_agent = models.CharField(max_length=500, blank=True, verbose_name="Navegador/Dispositivo")
    viewed_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Vista")
    
    class Meta:
        # ⭐ CLAVE: Esta combinación evita duplicados
        unique_together = ('post', 'ip_address')
        ordering = ['-viewed_at']
        verbose_name = "Vista de Artículo"
        verbose_name_plural = "Vistas de Artículos"
    
    def __str__(self):
        return f"{self.ip_address} - {self.post.title} - {self.viewed_at.strftime('%d/%m/%Y %H:%M')}"


# ============================================
# MODELOS DE FORMULARIOS
# ============================================

class ConsultaAsesoria(models.Model):
    """
    Modelo para guardar consultas de asesoría
    También se envía a Make.com para automatización
    """
    # Campos del formulario
    nombre = models.CharField(max_length=200, verbose_name="Nombre Completo")
    email = models.EmailField(verbose_name="Correo Electrónico")
    telefono = models.CharField(max_length=20, verbose_name="Número de Teléfono")
    duda = models.TextField(verbose_name="Duda o Consulta")
    
    # Metadata
    fecha_envio = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Envío")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP del Usuario")
    user_agent = models.CharField(max_length=500, null=True, blank=True, verbose_name="Navegador")
    
    # Estado de procesamiento
    procesado = models.BooleanField(default=False, verbose_name="Procesado")
    enviado_make = models.BooleanField(default=False, verbose_name="Enviado a Make")
    fecha_procesamiento = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Procesamiento")
    
    # Notas internas
    notas_admin = models.TextField(blank=True, verbose_name="Notas del Administrador")
    
    class Meta:
        verbose_name = "Consulta de Asesoría"
        verbose_name_plural = "Consultas de Asesoría"
        ordering = ['-fecha_envio']
    
    def __str__(self):
        return f"{self.nombre} - {self.email} - {self.fecha_envio.strftime('%d/%m/%Y %H:%M')}"
    
    def marcar_como_procesado(self):
        """Marcar consulta como procesada"""
        self.procesado = True
        self.fecha_procesamiento = timezone.now()
        self.save()


class SolicitudCotizacion(models.Model):
    """
    Modelo para guardar solicitudes de cotización del formulario principal
    También se envía a Make.com para automatización
    Incluye país de origen Y país de destino
    """
    # Campos del formulario
    nombre = models.CharField(max_length=200, verbose_name="Nombre Completo")
    empresa = models.CharField(max_length=200, blank=True, verbose_name="Empresa")
    email = models.EmailField(verbose_name="Correo Electrónico")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    
    # País de origen y destino
    pais_origen = models.CharField(max_length=100, verbose_name="País de Origen")
    pais_destino = models.CharField(max_length=100, verbose_name="País de Destino")
    
    tipo_servicio = models.CharField(max_length=100, verbose_name="Tipo de Servicio")
    mensaje = models.TextField(verbose_name="Descripción del Proyecto")
    
    # Metadata
    fecha_envio = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Envío")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP del Usuario")
    user_agent = models.CharField(max_length=500, null=True, blank=True, verbose_name="Navegador")
    
    # Estado de procesamiento
    procesado = models.BooleanField(default=False, verbose_name="Procesado")
    enviado_make = models.BooleanField(default=False, verbose_name="Enviado a Make")
    fecha_procesamiento = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Procesamiento")
    
    # Notas internas
    notas_admin = models.TextField(blank=True, verbose_name="Notas del Administrador")
    
    class Meta:
        verbose_name = "Solicitud de Cotización"
        verbose_name_plural = "Solicitudes de Cotización"
        ordering = ['-fecha_envio']
    
    def __str__(self):
        return f"{self.nombre} - {self.pais_origen}→{self.pais_destino} - {self.tipo_servicio} - {self.fecha_envio.strftime('%d/%m/%Y %H:%M')}"
    
    def marcar_como_procesado(self):
        """Marcar solicitud como procesada"""
        self.procesado = True
        self.fecha_procesamiento = timezone.now()
        self.save()
    
    def get_ruta_display(self):
        """Retorna la ruta en formato legible"""
        return f"{self.pais_origen} → {self.pais_destino}"


# ============================================
# MODELO DE NEWSLETTER
# ============================================

class NewsletterSubscriber(models.Model):
    """Modelo para suscriptores del newsletter"""
    email = models.EmailField(unique=True, verbose_name="Email")
    name = models.CharField(max_length=100, blank=True, verbose_name="Nombre")
    subscribed_date = models.DateTimeField(default=timezone.now, verbose_name="Fecha de suscripción")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP")
    user_agent = models.TextField(blank=True, verbose_name="Navegador")
    source_page = models.CharField(max_length=200, blank=True, verbose_name="Página de origen")
    
    # Campos GDPR
    consent_given = models.BooleanField(default=True, verbose_name="Consentimiento")
    consent_date = models.DateTimeField(default=timezone.now, verbose_name="Fecha consentimiento")
    
    # Control
    unsubscribed_date = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de baja")
    sent_to_make = models.BooleanField(default=False, verbose_name="Enviado a Make")
    notes = models.TextField(blank=True, verbose_name="Notas")
    
    class Meta:
        verbose_name = "Suscriptor Newsletter"
        verbose_name_plural = "Suscriptores Newsletter"
        ordering = ['-subscribed_date']
    
    def __str__(self):
        return f"{self.email} - {'Activo' if self.is_active else 'Inactivo'}"