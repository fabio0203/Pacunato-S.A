// ============================================
// NAVBAR - BOTÓN COTIZAR AHORA
// Lleva al formulario de cotización en home desde cualquier página
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('🎯 Script de Cotizar Ahora cargado');
    
    const cotizarBtn = document.getElementById('cotizarBtn');
    const currentPath = window.location.pathname;
    
    if (!cotizarBtn) {
        console.warn('⚠️ Botón #cotizarBtn no encontrado');
        return;
    }
    
    console.log('📍 Página actual:', currentPath);
    
    cotizarBtn.addEventListener('click', function(e) {
        e.preventDefault(); // Prevenir navegación por defecto
        
        console.log('🖱️ Click en Cotizar Ahora');
        
        // Verificar si estamos en la página de inicio
        const isHomePage = currentPath === '/' || currentPath === '/home/' || currentPath === '';
        
        if (isHomePage) {
            // Estamos en home, hacer scroll directo al formulario
            console.log('✅ En home - Scroll al formulario');
            scrollToQuoteForm();
        } else {
            // Estamos en otra página, navegar a home con hash
            console.log('🔄 En otra página - Navegando a home');
            
            // Opción 1: Navegar a home y el anchor hará el scroll automáticamente
            window.location.href = cotizarBtn.getAttribute('href');
            
            // Nota: No necesitamos hacer nada más porque el navegador
            // automáticamente hará scroll al #cotizacion después de cargar home
        }
    });
    
    // ============================================
    // FUNCIÓN: SCROLL AL FORMULARIO
    // ============================================
    function scrollToQuoteForm() {
        const quoteForm = document.getElementById('cotizacion');
        
        if (quoteForm) {
            console.log('📋 Formulario encontrado - Haciendo scroll');
            
            // Calcular posición con offset para el navbar
            const offsetTop = quoteForm.offsetTop - 100; // 100px de espacio superior
            
            // Smooth scroll
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
            
            // Efecto visual opcional: destacar el formulario brevemente
            highlightForm(quoteForm);
            
        } else {
            console.error('❌ Formulario #cotizacion no encontrado en la página');
        }
    }
    
    // ============================================
    // FUNCIÓN: DESTACAR FORMULARIO (OPCIONAL)
    // ============================================
    function highlightForm(element) {
        // Añadir clase de animación
        element.classList.add('highlight-animation');
        
        // Remover clase después de la animación
        setTimeout(() => {
            element.classList.remove('highlight-animation');
        }, 2000);
    }
    
    // ============================================
    // MANEJAR HASH AL CARGAR PÁGINA
    // Si llegamos a home con #cotizacion en la URL
    // ============================================
    window.addEventListener('load', function() {
        const hash = window.location.hash;
        
        if (hash === '#cotizacion') {
            console.log('🔗 Detectado hash #cotizacion - Haciendo scroll');
            
            // Pequeño delay para asegurar que la página esté completamente cargada
            setTimeout(() => {
                scrollToQuoteForm();
            }, 300);
        }
    });
    
    console.log('✅ Script de Cotizar Ahora inicializado');
});

// ============================================
// FALLBACK: Si el usuario usa navegación del navegador
// ============================================
window.addEventListener('hashchange', function() {
    if (window.location.hash === '#cotizacion') {
        console.log('📍 Hash cambió a #cotizacion');
        const quoteForm = document.getElementById('cotizacion');
        
        if (quoteForm) {
            const offsetTop = quoteForm.offsetTop - 100;
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    }
});