from django import template
from django.templatetags.static import static
from pathlib import Path

register = template.Library()

@register.simple_tag
def webp_image(image_path, css_class='', alt='', loading='lazy'):
    """
    Genera etiqueta <picture> con soporte WebP y fallback
    
    Uso: {% webp_image 'images/hero.jpg' 'hero-image' 'Descripción' %}
    """
    # Obtener ruta base sin extensión
    path_obj = Path(image_path)
    base_path = str(path_obj.with_suffix(''))
    extension = path_obj.suffix
    
    # Construir URLs
    webp_url = static(f"{base_path}.webp")
    fallback_url = static(image_path)
    
    html = f'''<picture>
    <source srcset="{webp_url}" type="image/webp">
    <img src="{fallback_url}" 
         alt="{alt}" 
         class="{css_class}"
         loading="{loading}"
         decoding="async">
</picture>'''
    
    return html