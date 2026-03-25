// ============================================
// CARRUSEL AUTOMÁTICO
// ============================================

class Carousel {
    constructor(containerId, options = {}) {
        this.container = document.querySelector(containerId);
        if (!this.container) return;
        
        this.slides = this.container.querySelectorAll('.carousel-slide');
        this.indicators = this.container.querySelectorAll('.indicator');
        this.prevBtn = this.container.querySelector('.carousel-control.prev');
        this.nextBtn = this.container.querySelector('.carousel-control.next');
        
        this.currentSlide = 0;
        this.autoPlayInterval = null;
        
        this.options = {
            autoPlay: options.autoPlay !== undefined ? options.autoPlay : true,
            interval: options.interval || 3000, // 5 segundos
            pauseOnHover: options.pauseOnHover !== undefined ? options.pauseOnHover : true
        };
        
        this.init();
    }
    
    init() {
        // Event listeners para controles
        if (this.prevBtn) {
            this.prevBtn.addEventListener('click', () => this.prev());
        }
        
        if (this.nextBtn) {
            this.nextBtn.addEventListener('click', () => this.next());
        }
        
        // Event listeners para indicadores
        this.indicators.forEach((indicator, index) => {
            indicator.addEventListener('click', () => this.goToSlide(index));
        });
        
        // Pausar en hover
        if (this.options.pauseOnHover) {
            this.container.addEventListener('mouseenter', () => this.pause());
            this.container.addEventListener('mouseleave', () => this.resume());
        }
        
        // Iniciar autoplay
        if (this.options.autoPlay) {
            this.start();
        }
        
        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') this.prev();
            if (e.key === 'ArrowRight') this.next();
        });
    }
    
    goToSlide(index) {
        // Remover active de slide actual
        this.slides[this.currentSlide].classList.remove('active');
        this.indicators[this.currentSlide].classList.remove('active');
        
        // Actualizar índice
        this.currentSlide = index;
        
        // Agregar active al nuevo slide
        this.slides[this.currentSlide].classList.add('active');
        this.indicators[this.currentSlide].classList.add('active');
    }
    
    next() {
        const nextSlide = (this.currentSlide + 1) % this.slides.length;
        this.goToSlide(nextSlide);
    }
    
    prev() {
        const prevSlide = (this.currentSlide - 1 + this.slides.length) % this.slides.length;
        this.goToSlide(prevSlide);
    }
    
    start() {
        this.autoPlayInterval = setInterval(() => {
            this.next();
        }, this.options.interval);
    }
    
    pause() {
        if (this.autoPlayInterval) {
            clearInterval(this.autoPlayInterval);
            this.autoPlayInterval = null;
        }
    }
    
    resume() {
        if (this.options.autoPlay && !this.autoPlayInterval) {
            this.start();
        }
    }
}

// ============================================
// INICIALIZAR CARRUSEL
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    new Carousel('.carousel-container', {
        autoPlay: true,
        interval: 3000,      // Cambiar cada 5 segundos
        pauseOnHover: false,   // Pausar al pasar el mouse
    });
});