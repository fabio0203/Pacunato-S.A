// ============================================
// NAVBAR ACTIVE STATE - DETECTA PÁGINA ACTUAL
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('🎯 Navbar active state script iniciado');
    
    // Obtener la URL actual
    const currentPath = window.location.pathname;
    console.log('📍 Página actual:', currentPath);
    
    // Obtener todos los links del navbar
    const navLinks = document.querySelectorAll('.nav-link');
    
    if (navLinks.length === 0) {
        console.warn('⚠️ No se encontraron links .nav-link en el navbar');
        return;
    }
    
    console.log(`✅ Encontrados ${navLinks.length} links en el navbar`);
    
    // Función para activar el link correspondiente
    function setActiveLink() {
        // Primero, remover la clase 'active' de todos los links
        navLinks.forEach(link => {
            link.classList.remove('active');
        });
        
        // Detectar qué página está activa según la URL
        if (currentPath === '/' || currentPath === '') {
            // Página de inicio
            if (navLinks[0]) {
                navLinks[0].classList.add('active');
                console.log('✅ Link activo: INICIO');
            }
        } 
        else if (currentPath.includes('/servicios')) {
            // Página de servicios
            if (navLinks[1]) {
                navLinks[1].classList.add('active');
                console.log('✅ Link activo: SERVICIOS');
            }
        } 
        else if (currentPath.includes('/nosotros') || currentPath.includes('/por-que-nosotros')) {
            // Página Por Qué Nosotros
            if (navLinks[2]) {
                navLinks[2].classList.add('active');
                console.log('✅ Link activo: POR QUÉ NOSOTROS');
            }
        } 
        else if (currentPath.includes('/blog')) {
            // Blog (incluye posts individuales)
            if (navLinks[3]) {
                navLinks[3].classList.add('active');
                console.log('✅ Link activo: BLOG');
            }
        } 
        else if (currentPath.includes('/contacto')) {
            // Página de contacto
            if (navLinks[4]) {
                navLinks[4].classList.add('active');
                console.log('✅ Link activo: CONTACTO');
            }
        }
        else {
            console.log('⚠️ Página no reconocida:', currentPath);
        }
    }
    
    // Ejecutar la función
    setActiveLink();
    
    // ============================================
    // MOBILE MENU TOGGLE
    // ============================================
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const navMenu = document.getElementById('navMenu');
    
    if (mobileMenuBtn && navMenu) {
        console.log('✅ Mobile menu detectado');
        
        mobileMenuBtn.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            
            // Cambiar icono hamburguesa <-> X
            const icon = this.querySelector('i');
            if (navMenu.classList.contains('active')) {
                icon.className = 'fas fa-times';
            } else {
                icon.className = 'fas fa-bars';
            }
        });
        
        // Cerrar menú móvil al hacer click en un link
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                if (window.innerWidth <= 768) {
                    navMenu.classList.remove('active');
                    const icon = mobileMenuBtn.querySelector('i');
                    icon.className = 'fas fa-bars';
                }
            });
        });
    }
    
    console.log('🎯 Navbar active state configurado correctamente');
});

// ============================================
// VERSIÓN ALTERNATIVA: COMPARACIÓN POR HREF
// ============================================
// Usa esta versión si la anterior no funciona bien
/*
document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('.nav-link');
    const currentPath = window.location.pathname;
    
    navLinks.forEach(link => {
        const linkHref = link.getAttribute('href');
        
        // Marcar como activo si coincide
        if (currentPath === linkHref) {
            link.classList.add('active');
        }
        // Caso especial: si está en una subpágina
        else if (linkHref !== '/' && currentPath.includes(linkHref)) {
            link.classList.add('active');
        }
    });
});
*/