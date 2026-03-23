// ============================================
// FOOTER - SCROLL TO TOP EN PÁGINA ACTUAL
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('🦶 Footer script cargado');
    
    // Obtener la URL actual (sin parámetros)
    const currentPath = window.location.pathname;
    console.log('📍 Página actual:', currentPath);
    
    // Obtener todos los enlaces de página en el footer
    const footerPageLinks = document.querySelectorAll('.footer-page-link');
    
    footerPageLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const linkHref = this.getAttribute('href');
            const linkPath = new URL(linkHref, window.location.origin).pathname;
            
            console.log('🔗 Click en:', linkPath);
            console.log('📄 Comparando con:', currentPath);
            
            // Si estamos en la misma página
            if (linkPath === currentPath) {
                e.preventDefault();
                console.log('✅ Misma página - Scroll to top');
                
                // Smooth scroll to top
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
                
                // Opcional: Añadir clase de animación temporal
                document.body.classList.add('scrolling-to-top');
                setTimeout(() => {
                    document.body.classList.remove('scrolling-to-top');
                }, 1000);
            } else {
                console.log('⏭️ Navegando a otra página');
                // Dejar que el navegador maneje la navegación normal
            }
        });
    });
    
    // ============================================
    // ENLACES DE ANCLAS (#cotizacion, etc)
    // ============================================
    const footerAnchorLinks = document.querySelectorAll('.footer-anchor-link');
    
    footerAnchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            // Si es un ancla (#algo)
            if (href && href.startsWith('#')) {
                e.preventDefault();
                const targetId = href.substring(1);
                const target = document.getElementById(targetId);
                
                if (target) {
                    console.log('🎯 Scroll to anchor:', targetId);
                    
                    const offsetTop = target.offsetTop - 80; // 80px para el navbar
                    
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                } else {
                    console.warn('⚠️ Ancla no encontrada:', targetId);
                }
            }
        });
    });
    
    // ============================================
    // WHATSAPP - ANALYTICS (OPCIONAL)
    // ============================================
    const whatsappLink = document.querySelector('.social-link.whatsapp');
    
    if (whatsappLink) {
        whatsappLink.addEventListener('click', function() {
            console.log('💬 Click en WhatsApp desde footer');
            
            // Aquí puedes añadir tracking de analytics si lo necesitas
            // Por ejemplo: gtag('event', 'whatsapp_click', {...});
        });
    }
    
    // ============================================
    // ENLACES DE CONTACTO CLICABLES
    // ============================================
    const contactLinks = document.querySelectorAll('.contact-link');
    
    contactLinks.forEach(link => {
        link.addEventListener('click', function() {
            const type = this.href.includes('tel:') ? 'teléfono' : 'email';
            console.log(`📞 Click en ${type}:`, this.href);
        });
    });
    
    // ============================================
    // ANIMACIÓN HOVER EN REDES SOCIALES
    // ============================================
    const socialLinks = document.querySelectorAll('.social-link');
    
    socialLinks.forEach(link => {
        link.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) rotate(5deg)';
        });
        
        link.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) rotate(0deg)';
        });
    });
    
    console.log('✅ Footer funcionalidades activadas');
});

// ============================================
// SCROLL TO TOP BUTTON (BONUS)
// ============================================
// Crear un botón flotante de scroll to top
function createScrollToTopButton() {
    // Verificar si ya existe
    if (document.getElementById('scrollToTopBtn')) return;
    
    const button = document.createElement('button');
    button.id = 'scrollToTopBtn';
    button.className = 'scroll-to-top-btn';
    button.innerHTML = '<i class="fas fa-chevron-up"></i>';
    button.setAttribute('aria-label', 'Volver arriba');
    button.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
        color: white;
        border: none;
        border-radius: 50%;
        cursor: pointer;
        display: none;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
        box-shadow: 0 5px 20px rgba(0, 180, 216, 0.4);
        z-index: 999;
        transition: all 0.3s ease;
    `;
    
    document.body.appendChild(button);
    
    // Mostrar/ocultar según scroll
    window.addEventListener('scroll', function() {
        if (window.scrollY > 300) {
            button.style.display = 'flex';
        } else {
            button.style.display = 'none';
        }
    });
    
    // Click para scroll to top
    button.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // Hover effect
    button.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-5px) scale(1.1)';
        this.style.boxShadow = '0 10px 30px rgba(0, 180, 216, 0.6)';
    });
    
    button.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0) scale(1)';
        this.style.boxShadow = '0 5px 20px rgba(0, 180, 216, 0.4)';
    });
    
    console.log('🔼 Botón scroll to top creado');
}

// Activar botón scroll to top
document.addEventListener('DOMContentLoaded', createScrollToTopButton);