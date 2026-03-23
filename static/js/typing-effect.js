// ============================================
// TYPING EFFECT - EFECTO MÁQUINA DE ESCRIBIR
// CON RESALTADO DE PALABRAS CLAVE
// ============================================

class TypingEffect {
    constructor(element, texts, options = {}) {
        this.element = element;
        this.texts = Array.isArray(texts) ? texts : [texts];
        this.options = {
            typingSpeed: options.typingSpeed || 80,
            deletingSpeed: options.deletingSpeed || 50,
            pauseEnd: options.pauseEnd || 2000,
            pauseStart: options.pauseStart || 500,
            loop: options.loop !== undefined ? options.loop : true,
            highlightWords: options.highlightWords || [] // Palabras a resaltar
        };
        
        this.textIndex = 0;
        this.charIndex = 0;
        this.isDeleting = false;
        this.currentTextArray = [];
        
        this.init();
    }
    
    init() {
        // Preparar el texto con HTML para palabras resaltadas
        this.prepareTexts();
        
        // Pequeña pausa antes de empezar
        setTimeout(() => {
            this.type();
        }, this.options.pauseStart);
    }
    
    prepareTexts() {
        // Convertir textos a arrays de caracteres con markup HTML
        this.processedTexts = this.texts.map(text => {
            return this.highlightKeywords(text);
        });
    }
    
    highlightKeywords(text) {
        let result = text;
        
        // Reemplazar palabras clave con spans
        this.options.highlightWords.forEach(word => {
            const regex = new RegExp(`(${word})`, 'gi');
            result = result.replace(regex, '<span class="text-primary">$1</span>');
        });
        
        return result;
    }
    
    type() {
        const currentText = this.processedTexts[this.textIndex];
        
        if (this.isDeleting) {
            // Borrando texto
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = currentText;
            const plainText = tempDiv.textContent || tempDiv.innerText;
            
            this.charIndex--;
            const visibleText = plainText.substring(0, this.charIndex);
            this.element.innerHTML = this.highlightKeywords(visibleText);
            
            if (this.charIndex === 0) {
                this.isDeleting = false;
                this.textIndex = (this.textIndex + 1) % this.texts.length;
                
                // Si solo hay un texto y no es loop, detener
                if (this.texts.length === 1 && !this.options.loop) {
                    return;
                }
                
                setTimeout(() => this.type(), 500);
                return;
            }
        } else {
            // Escribiendo texto
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = currentText;
            const plainText = tempDiv.textContent || tempDiv.innerText;
            
            this.charIndex++;
            const visibleText = plainText.substring(0, this.charIndex);
            this.element.innerHTML = this.highlightKeywords(visibleText);
            
            if (this.charIndex === plainText.length) {
                // Texto completo escrito
                if (this.texts.length > 1 || this.options.loop) {
                    setTimeout(() => {
                        this.isDeleting = true;
                        this.type();
                    }, this.options.pauseEnd);
                } else {
                    // Si no hace loop, ocultar cursor después de terminar
                    setTimeout(() => {
                        document.querySelector('.typing-cursor')?.classList.add('hide-cursor');
                    }, 2000);
                }
                return;
            }
        }
        
        const speed = this.isDeleting ? this.options.deletingSpeed : this.options.typingSpeed;
        setTimeout(() => this.type(), speed);
    }
}

// ============================================
// INICIALIZAR EFECTO AL CARGAR LA PÁGINA
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    const typingElement = document.getElementById('typingText');
    
    if (typingElement) {
        // OPCIÓN 1: Un solo texto que se repite con palabras resaltadas
        new TypingEffect(typingElement, 
            'Conectamos tu Negocio con Proveedores Confiables en Todo el Mundo',
            {
                typingSpeed: 60,
                deletingSpeed: 40,
                pauseEnd: 2500,         // Pausa después de escribir
                pauseStart: 500,
                loop: true,              // CAMBIAR A true PARA QUE SE REPITA
               highlightWords: [
    'Proveedores Confiables',  // Primera palabra clave
    'Todo el Mundo'            // Segunda palabra clave
]
            }
        );
        
        /* 
        // OPCIÓN 2: Múltiples textos alternados (descomentar si quieres)
        new TypingEffect(typingElement, [
            'Conectamos tu Negocio con Proveedores Confiables en Todo el Mundo',
            'Soluciones Logísticas Integrales desde Panamá',
            'Tu Socio Estratégico en Comercio Internacional'
        ], {
            typingSpeed: 60,
            deletingSpeed: 40,
            pauseEnd: 2500,
            pauseStart: 500,
            loop: true,
            highlightWords: [
                'Proveedores Confiables', 
                'Logísticas Integrales', 
                'Socio Estratégico',
                'Comercio Internacional'
            ]
        });
        */
    }
});

// ============================================
// ARREGLO JAVASCRIPT - EFECTO MÁQUINA SIN SALTOS
// Añade esto a tu archivo JS principal o crea typing-fix.js
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('🔧 Arreglo de typing effect cargado');
    
    // Encontrar el elemento que tiene el efecto de typing
    const typingElement = document.querySelector('.typing-text') || 
                         document.querySelector('[data-typing]') ||
                         document.querySelector('.hero h1') ||
                         document.querySelector('.hero-content h1');
    
    if (!typingElement) {
        console.warn('⚠️ No se encontró elemento con efecto typing');
        return;
    }
    
    console.log('✅ Elemento typing encontrado:', typingElement);
    
    // SOLUCIÓN 1: Calcular y fijar altura antes de que empiece la animación
    const originalText = typingElement.textContent;
    const tempSpan = document.createElement('span');
    tempSpan.style.visibility = 'hidden';
    tempSpan.style.position = 'absolute';
    tempSpan.style.whiteSpace = 'nowrap';
    tempSpan.textContent = originalText;
    document.body.appendChild(tempSpan);
    
    const fullWidth = tempSpan.offsetWidth;
    const fullHeight = tempSpan.offsetHeight;
    
    document.body.removeChild(tempSpan);
    
    // Fijar dimensiones mínimas del contenedor padre
    const container = typingElement.parentElement;
    if (container) {
        container.style.minHeight = `${fullHeight + 40}px`; // +40px de padding
        console.log(`📏 Altura mínima fijada: ${fullHeight + 40}px`);
    }
    
    // SOLUCIÓN 2: Fijar altura del elemento mismo
    typingElement.style.minHeight = `${fullHeight}px`;
    typingElement.style.display = 'inline-block';
    
    // SOLUCIÓN 3: Si el texto cambia dinámicamente, mantener altura
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList' || mutation.type === 'characterData') {
                // Asegurar que la altura no cambie
                const currentHeight = typingElement.offsetHeight;
                if (currentHeight < fullHeight) {
                    typingElement.style.minHeight = `${fullHeight}px`;
                }
            }
        });
    });
    
    observer.observe(typingElement, {
        childList: true,
        characterData: true,
        subtree: true
    });
    
    console.log('✅ Observador de mutaciones activo');
});

// ============================================
// ALTERNATIVA: Si usas un script de typing específico
// Modifica tu función de typing para incluir esto:
// ============================================

function typingEffectFixed(element, text, speed = 100) {
    // Calcular altura completa ANTES de empezar
    const tempDiv = document.createElement('div');
    tempDiv.style.visibility = 'hidden';
    tempDiv.style.position = 'absolute';
    tempDiv.style.font = window.getComputedStyle(element).font;
    tempDiv.textContent = text;
    document.body.appendChild(tempDiv);
    
    const fullHeight = tempDiv.offsetHeight;
    const fullWidth = tempDiv.offsetWidth;
    
    document.body.removeChild(tempDiv);
    
    // Fijar altura ANTES de empezar a escribir
    element.style.minHeight = `${fullHeight}px`;
    element.parentElement.style.minHeight = `${fullHeight + 40}px`;
    
    // Ahora sí, hacer el efecto de typing
    let i = 0;
    element.textContent = '';
    
    const interval = setInterval(() => {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
        } else {
            clearInterval(interval);
        }
    }, speed);
}

// Uso:
// typingEffectFixed(document.querySelector('.hero h1'), 'Tu texto aquí');
