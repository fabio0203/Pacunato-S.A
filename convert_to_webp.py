"""
Script para convertir todas las imágenes a formato WebP
Mantiene las originales y crea versiones .webp optimizadas
"""

from PIL import Image
import os
from pathlib import Path

# Directorios a procesar
IMAGE_DIRS = [
    'static/images',
    'media',  # Si tienes uploads de usuarios
]

# Extensiones soportadas
SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.gif'}

# Calidad WebP (0-100, recomendado 80-90)
WEBP_QUALITY = 85

def convert_image_to_webp(image_path):
    """
    Convierte una imagen a WebP manteniendo el original
    """
    try:
        # Abrir imagen
        img = Image.open(image_path)
        
        # Convertir RGBA a RGB si es necesario
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # Crear ruta del archivo WebP
        webp_path = image_path.with_suffix('.webp')
        
        # Guardar como WebP
        img.save(
            webp_path,
            'WEBP',
            quality=WEBP_QUALITY,
            method=6  # Mejor compresión
        )
        
        # Calcular tamaños
        original_size = image_path.stat().st_size
        webp_size = webp_path.stat().st_size
        reduction = ((original_size - webp_size) / original_size) * 100
        
        print(f"✅ {image_path.name}")
        print(f"   Original: {original_size / 1024:.1f} KB")
        print(f"   WebP: {webp_size / 1024:.1f} KB")
        print(f"   Reducción: {reduction:.1f}%\n")
        
        return True
        
    except Exception as e:
        print(f"❌ Error procesando {image_path}: {e}\n")
        return False

def process_directory(directory):
    """
    Procesa todas las imágenes en un directorio
    """
    dir_path = Path(directory)
    
    if not dir_path.exists():
        print(f"⚠️  Directorio no encontrado: {directory}\n")
        return
    
    print(f"\n{'='*60}")
    print(f"📁 Procesando: {directory}")
    print(f"{'='*60}\n")
    
    images_found = 0
    images_converted = 0
    
    # Buscar todas las imágenes
    for ext in SUPPORTED_FORMATS:
        for image_path in dir_path.rglob(f'*{ext}'):
            images_found += 1
            
            # Verificar si ya existe la versión WebP
            webp_path = image_path.with_suffix('.webp')
            if webp_path.exists():
                print(f"⏭️  Ya existe: {image_path.name} (saltando)\n")
                continue
            
            # Convertir
            if convert_image_to_webp(image_path):
                images_converted += 1
    
    print(f"\n{'='*60}")
    print(f"📊 Resumen de {directory}:")
    print(f"   Imágenes encontradas: {images_found}")
    print(f"   Convertidas: {images_converted}")
    print(f"   Ya existían: {images_found - images_converted}")
    print(f"{'='*60}\n")

def main():
    """
    Función principal
    """
    print("\n" + "="*60)
    print("🎨 CONVERSOR DE IMÁGENES A WEBP")
    print("="*60)
    print(f"Calidad WebP: {WEBP_QUALITY}%")
    print(f"Formatos soportados: {', '.join(SUPPORTED_FORMATS)}")
    print("="*60 + "\n")
    
    total_dirs = 0
    for directory in IMAGE_DIRS:
        if Path(directory).exists():
            total_dirs += 1
            process_directory(directory)
    
    if total_dirs == 0:
        print("⚠️  No se encontraron directorios para procesar")
    else:
        print("\n✨ ¡Conversión completada!\n")

if __name__ == '__main__':
    main()