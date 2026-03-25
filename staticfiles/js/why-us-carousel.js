// Carrusel de Fondo del Hero
document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ why-us-carousel.js cargado correctamente');
    
    // Hero Background Carousel
    const bgSlides = document.querySelectorAll('.hero-bg-slide');
    console.log('🖼️ Slides de fondo encontrados:', bgSlides.length);
    
    if (bgSlides.length > 0) {
        let currentBgSlide = 0;
        
        function nextBgSlide() {
            bgSlides[currentBgSlide].classList.remove('active');
            currentBgSlide = (currentBgSlide + 1) % bgSlides.length;
            bgSlides[currentBgSlide].classList.add('active');
            console.log('🔄 Cambiando a slide:', currentBgSlide);
        }
        
        // Cambiar cada 4 segundos
        setInterval(nextBgSlide, 4000);
    }
    
    // Team Carousel
    const teamSlides = document.querySelectorAll('.team-slide');
    const teamIndicators = document.querySelectorAll('.team-indicator');
    console.log('👥 Team slides encontrados:', teamSlides.length);
    console.log('🔘 Indicadores encontrados:', teamIndicators.length);
    
    if (teamSlides.length > 0 && teamIndicators.length > 0) {
        let currentTeamSlide = 0;
        
        function showTeamSlide(index) {
            teamSlides.forEach(slide => slide.classList.remove('active'));
            teamIndicators.forEach(indicator => indicator.classList.remove('active'));
            
            teamSlides[index].classList.add('active');
            teamIndicators[index].classList.add('active');
            console.log('👥 Mostrando team slide:', index);
        }
        
        function nextTeamSlide() {
            currentTeamSlide = (currentTeamSlide + 1) % teamSlides.length;
            showTeamSlide(currentTeamSlide);
        }
        
        // Event listeners para indicadores
        teamIndicators.forEach((indicator, index) => {
            indicator.addEventListener('click', () => {
                console.log('👆 Click en indicador:', index);
                currentTeamSlide = index;
                showTeamSlide(currentTeamSlide);
            });
        });
        
        // Auto-avance cada 5 segundos
        setInterval(nextTeamSlide, 5000);
    }
    
    // Toggle Contact Options
    const toggleBtn = document.getElementById('toggleContactBtn');
    const contactCollapse = document.getElementById('contactOptionsCollapse');
    
    console.log('🔘 Botón toggle encontrado:', toggleBtn !== null);
    console.log('📋 Collapse encontrado:', contactCollapse !== null);
    
    if (toggleBtn && contactCollapse) {
        toggleBtn.addEventListener('click', function() {
            console.log('👆 Click en botón de contacto');
            contactCollapse.classList.toggle('active');
            
            // Cambiar icono del botón
            const icon = toggleBtn.querySelector('i');
            if (contactCollapse.classList.contains('active')) {
                console.log('✅ Abriendo opciones de contacto');
                icon.className = 'fas fa-times';
                toggleBtn.innerHTML = '<i class="fas fa-times"></i> Cerrar';
            } else {
                console.log('❌ Cerrando opciones de contacto');
                icon.className = 'fas fa-comments';
                toggleBtn.innerHTML = '<i class="fas fa-comments"></i> Contáctanos Ahora';
            }
            
            // Scroll suave al formulario cuando se abre
            if (contactCollapse.classList.contains('active')) {
                setTimeout(() => {
                    contactCollapse.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                }, 300);
            }
        });
    } else {
        console.error('❌ ERROR: No se encontraron los elementos del toggle');
        if (!toggleBtn) console.error('   - Botón toggleContactBtn no encontrado');
        if (!contactCollapse) console.error('   - Elemento contactOptionsCollapse no encontrado');
    }
});