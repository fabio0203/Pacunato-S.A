// Blog JavaScript - VERSIÓN MEJORADA
document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ Blog JS cargado correctamente');
    
    // ===== TABLE OF CONTENTS - SCROLL TRACKING DINÁMICO =====
    const tocLinks = document.querySelectorAll('.toc-link');
    const contentSections = document.querySelectorAll('.post-content-body h2');
    
    if (tocLinks.length > 0 && contentSections.length > 0) {
        console.log(`📋 Table of Contents encontrado - ${contentSections.length} secciones`);
        
        // Smooth scroll al hacer click
        tocLinks.forEach((link, index) => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Scroll a la sección correspondiente
                if (contentSections[index]) {
                    const targetPosition = contentSections[index].offsetTop - 100; // offset para navbar
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                }
                
                console.log(`📍 Navegando a sección ${index + 1}`);
            });
        });
        
        // ⭐ ACTUALIZACIÓN AUTOMÁTICA AL HACER SCROLL
        function updateActiveSection() {
            const scrollPosition = window.scrollY + 150; // offset para activar antes
            
            let currentSectionIndex = 0;
            
            // Encontrar la sección actual
            contentSections.forEach((section, index) => {
                const sectionTop = section.offsetTop;
                const sectionBottom = sectionTop + section.offsetHeight;
                
                if (scrollPosition >= sectionTop && scrollPosition < sectionBottom) {
                    currentSectionIndex = index;
                }
            });
            
            // Actualizar clases active
            tocLinks.forEach((link, index) => {
                if (index === currentSectionIndex) {
                    link.classList.add('active');
                } else {
                    link.classList.remove('active');
                }
            });
        }
        
        // Ejecutar al hacer scroll
        let scrollTimeout;
        window.addEventListener('scroll', function() {
            // Throttle para mejor rendimiento
            if (scrollTimeout) {
                clearTimeout(scrollTimeout);
            }
            
            scrollTimeout = setTimeout(updateActiveSection, 50);
        });
        
        // Ejecutar una vez al cargar
        updateActiveSection();
    }
    
    // ===== SHARE BUTTONS - VERSIÓN CORREGIDA =====
const shareButtons = document.querySelectorAll('.share-btn');

if (shareButtons.length > 0) {
    console.log('🔗 Botones de compartir encontrados:', shareButtons.length);
    
    shareButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Obtener datos del botón
            const platform = this.dataset.platform;
            const url = encodeURIComponent(this.dataset.url);
            const title = encodeURIComponent(this.dataset.title);
            
            let shareUrl = '';
            
            // Construir URL según la plataforma
            switch(platform) {
                case 'facebook':
                    shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${url}`;
                    console.log('📘 Compartiendo en Facebook');
                    break;
                    
                case 'twitter':
                    shareUrl = `https://twitter.com/intent/tweet?url=${url}&text=${title}`;
                    console.log('🐦 Compartiendo en Twitter');
                    break;
                    
                case 'linkedin':
                    shareUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${url}`;
                    console.log('💼 Compartiendo en LinkedIn');
                    break;
                    
                case 'whatsapp':
                    shareUrl = `https://wa.me/?text=${title}%20${url}`;
                    console.log('💬 Compartiendo en WhatsApp');
                    break;
                    
                default:
                    console.warn('⚠️ Plataforma no reconocida:', platform);
                    return;
            }
            
            if (shareUrl) {
                // Abrir ventana popup para compartir
                const popupWidth = 600;
                const popupHeight = 500;
                const left = (window.innerWidth - popupWidth) / 2;
                const top = (window.innerHeight - popupHeight) / 2;
                
                window.open(
                    shareUrl,
                    'share-dialog',
                    `width=${popupWidth},height=${popupHeight},left=${left},top=${top},menubar=no,toolbar=no,resizable=yes,scrollbars=yes`
                );
                
                // Efecto visual al hacer clic
                this.style.transform = 'scale(0.9)';
                setTimeout(() => {
                    this.style.transform = 'scale(1)';
                }, 150);
                
                // Tracking (si tienes analytics configurado)
                if (typeof trackEvent === 'function') {
                    trackEvent('share', {
                        'event_category': 'Social Share',
                        'event_label': platform,
                        'value': 1
                    });
                }
            }
        });
    });
}
    
    // ===== READING PROGRESS BAR =====
    const postContent = document.querySelector('.post-main-content');
    
    if (postContent) {
        console.log('📖 Contenido del post encontrado');
        
        // Crear barra de progreso
        const progressBar = document.createElement('div');
        progressBar.className = 'reading-progress-bar';
        progressBar.innerHTML = '<div class="reading-progress-fill"></div>';
        document.body.appendChild(progressBar);
        
        const progressFill = progressBar.querySelector('.reading-progress-fill');
        
        window.addEventListener('scroll', () => {
            const windowHeight = window.innerHeight;
            const documentHeight = document.documentElement.scrollHeight;
            const scrolled = window.scrollY;
            const progress = (scrolled / (documentHeight - windowHeight)) * 100;
            
            progressFill.style.width = `${Math.min(progress, 100)}%`;
        });
        
        // Estilos para la barra
        const style = document.createElement('style');
        style.textContent = `
            .reading-progress-bar {
                position: fixed;
                top: 80px;
                left: 0;
                width: 100%;
                height: 4px;
                background: var(--dark-bg-3);
                z-index: 999;
            }
            .reading-progress-fill {
                height: 100%;
                width: 0%;
                background: linear-gradient(90deg, var(--primary-color), var(--primary-dark));
                transition: width 0.1s ease;
            }
        `;
        document.head.appendChild(style);
    }
    
    // ===== LAZY LOADING DE IMÁGENES =====
    const lazyImages = document.querySelectorAll('img[data-src]');
    
    if (lazyImages.length > 0) {
        console.log(`🖼️ ${lazyImages.length} imágenes con lazy loading`);
        
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                    console.log('🖼️ Imagen cargada');
                }
            });
        });
        
        lazyImages.forEach(img => imageObserver.observe(img));
    }
    
    // ===== SCROLL TO TOP BUTTON =====
    const scrollToTopBtn = document.createElement('button');
    scrollToTopBtn.className = 'scroll-to-top';
    scrollToTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    scrollToTopBtn.setAttribute('aria-label', 'Volver arriba');
    document.body.appendChild(scrollToTopBtn);
    
    // Mostrar/ocultar botón
    window.addEventListener('scroll', () => {
        if (window.scrollY > 500) {
            scrollToTopBtn.classList.add('visible');
        } else {
            scrollToTopBtn.classList.remove('visible');
        }
    });
    
    // Click en botón
    scrollToTopBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
        console.log('⬆️ Scroll to top');
    });
    
    // Estilos para el botón
    const scrollBtnStyle = document.createElement('style');
    scrollBtnStyle.textContent = `
        .scroll-to-top {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            width: 50px;
            height: 50px;
            background: var(--primary-color);
            color: var(--text-light);
            border: none;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
            box-shadow: 0 5px 20px rgba(0, 180, 216, 0.4);
            opacity: 0;
            visibility: hidden;
            transform: translateY(20px);
            transition: all 0.3s ease;
            z-index: 998;
        }
        .scroll-to-top.visible {
            opacity: 1;
            visibility: visible;
            transform: translateY(0);
        }
        .scroll-to-top:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 180, 216, 0.5);
        }
        @media (max-width: 768px) {
            .scroll-to-top {
                bottom: 1rem;
                right: 1rem;
                width: 45px;
                height: 45px;
            }
        }
    `;
    document.head.appendChild(scrollBtnStyle);
    
    // ===== HIGHLIGHT DE SECCIONES AL NAVEGAR =====
    const sections = document.querySelectorAll('.post-content-body h2');
    
    sections.forEach(section => {
        // Agregar ID a cada sección si no tiene
        if (!section.id) {
            const id = section.textContent.toLowerCase()
                .replace(/[^\w\s]/gi, '')
                .replace(/\s+/g, '-');
            section.id = id;
        }
    });
    
    console.log('✅ Blog JS inicializado completamente');
});