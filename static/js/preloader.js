// ============================================
// PRELOADER CINEMATOGRÁFICO - AUDIO CON CLICK
// MODIFICADO: SOLO SE MUESTRA UNA VEZ
// ============================================

class CinematicPreloader {
    constructor() {
        // ✅ VERIFICAR SI YA SE VIO EL PRELOADER
        this.hasSeenBefore = localStorage.getItem('hasSeenPreloader') === 'true';
        
        if (this.hasSeenBefore) {
            console.log('✅ Usuario ya vio el preloader - omitiendo');
            // Asegurar que el body sea scrolleable
            document.body.style.overflow = '';
            return; // Salir sin hacer nada
        }
        
        console.log('🎬 Primera visita - mostrando preloader cinematográfico');
        
        this.progress = 0;
        this.targetProgress = 0;
        this.isComplete = false;
        this.audioReady = false;
        this.hasStarted = false;
        this.init();
    }
    
    init() {
        this.createPreloader();
        this.createStartOverlay();
        this.createLogoParticles();
        this.animateProgress();
    }
    
    createStartOverlay() {
        const overlay = document.createElement('div');
        overlay.id = 'start-overlay';
        overlay.innerHTML = `
            <div class="start-content">
                <div class="start-icon">
                    <i class="fas fa-play-circle"></i>
                </div>
                <h2>PACUNATO S.A.</h2>
                <p>Click para comenzar</p>
            </div>
        `;
        
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.95);
            z-index: 100000;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
        `;
        
        document.body.appendChild(overlay);
        
        overlay.addEventListener('click', async () => {
            if (!this.hasStarted) {
                this.hasStarted = true;
                
                // Fade out del overlay
                overlay.style.transition = 'opacity 0.5s';
                overlay.style.opacity = '0';
                
                setTimeout(() => {
                    overlay.remove();
                }, 500);
                
                // Iniciar audio y carga
                await this.initAudio();
                this.simulateLoading();
            }
        });
    }
    
    async initAudio() {
        try {
            await window.audioSystem.init();
            this.audioReady = true;
            
            window.audioSystem.play('startup');
            
            setTimeout(() => {
                window.audioSystem.play('ambient');
            }, 500);
        } catch (error) {
            console.warn('Audio not available:', error);
            this.audioReady = false;
        }
    }
    
    createPreloader() {
        const preloader = document.createElement('div');
        preloader.id = 'cinematic-preloader';
        preloader.innerHTML = `
            <div class="preloader-bg">
                <div class="grid-overlay"></div>
                <div class="scanlines"></div>
            </div>
            
            <div class="preloader-content">
                <div class="logo-container">
                    <canvas id="logo-particles"></canvas>
                    <div class="logo-reveal">
                        <img src="${window.logoPath || '/static/images/logo.png'}" alt="Pacunato" class="preloader-logo">
                        <div class="logo-glitch"></div>
                    </div>
                </div>
                
                <div class="company-name">
                    <span class="company-text">PACUNATO S.A.</span>
                    <div class="company-subtitle">COMPRAS INTERNACIONALES</div>
                </div>
                
                <div class="progress-container">
                    <div class="progress-bar-outer">
                        <div class="progress-bar-inner" id="progressBar"></div>
                        <div class="progress-glow"></div>
                    </div>
                    <div class="progress-details">
                        <span class="progress-text" id="progressText">ESPERANDO INICIALIZACIÓN</span>
                        <span class="progress-percent" id="progressPercent">0%</span>
                    </div>
                    <div class="loading-stages" id="loadingStages"></div>
                </div>
                
                <div class="holographic-overlay"></div>
            </div>
            
            <div class="corner-decoration top-left"></div>
            <div class="corner-decoration top-right"></div>
            <div class="corner-decoration bottom-left"></div>
            <div class="corner-decoration bottom-right"></div>
        `;
        
        document.body.appendChild(preloader);
        document.body.style.overflow = 'hidden';
    }
    
    createLogoParticles() {
        const canvas = document.getElementById('logo-particles');
        if (!canvas) return;
        
        const ctx = canvas.getContext('2d');
        const container = canvas.parentElement;
        
        canvas.width = container.offsetWidth;
        canvas.height = container.offsetHeight;
        
        const particles = [];
        const particleCount = 150;
        
        for (let i = 0; i < particleCount; i++) {
            particles.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                targetX: canvas.width / 2 + (Math.random() - 0.5) * 200,
                targetY: canvas.height / 2 + (Math.random() - 0.5) * 200,
                size: Math.random() * 3 + 1,
                speedX: (Math.random() - 0.5) * 2,
                speedY: (Math.random() - 0.5) * 2,
                color: `hsl(${190 + Math.random() * 20}, 100%, ${50 + Math.random() * 30}%)`,
                alpha: Math.random()
            });
        }
        
        const animate = () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            particles.forEach((p, index) => {
                const dx = p.targetX - p.x;
                const dy = p.targetY - p.y;
                
                p.x += dx * 0.05 + p.speedX;
                p.y += dy * 0.05 + p.speedY;
                
                p.speedX *= 0.95;
                p.speedY *= 0.95;
                p.alpha = Math.min(1, p.alpha + 0.01);
                
                // Dibujar partícula principal
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
                ctx.fillStyle = p.color;
                ctx.globalAlpha = p.alpha;
                ctx.fill();
                
                // Efecto glow - CORREGIDO
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.size * 3, 0, Math.PI * 2);
                
                const gradient = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.size * 3);
                
                // Extraer valores RGB del color HSL
                const alphaHex = Math.floor(p.alpha * 255).toString(16).padStart(2, '0');
                
                // Convertir HSL a RGB para usar con alpha
                const hslMatch = p.color.match(/hsl\((\d+),\s*(\d+)%,\s*(\d+)%\)/);
                if (hslMatch) {
                    const h = parseInt(hslMatch[1]);
                    const s = parseInt(hslMatch[2]);
                    const l = parseInt(hslMatch[3]);
                    
                    // Simplificado: usar rgba directamente
                    gradient.addColorStop(0, `hsla(${h}, ${s}%, ${l}%, ${p.alpha})`);
                    gradient.addColorStop(0.5, `hsla(${h}, ${s}%, ${l}%, ${p.alpha * 0.3})`);
                    gradient.addColorStop(1, 'transparent');
                    
                    ctx.fillStyle = gradient;
                    ctx.fill();
                }
                
                // Conectar partículas cercanas
                for (let j = index + 1; j < particles.length; j++) {
                    const dx2 = particles[j].x - p.x;
                    const dy2 = particles[j].y - p.y;
                    const dist = Math.sqrt(dx2 * dx2 + dy2 * dy2);
                    
                    if (dist < 100) {
                        ctx.beginPath();
                        ctx.moveTo(p.x, p.y);
                        ctx.lineTo(particles[j].x, particles[j].y);
                        ctx.strokeStyle = `rgba(0, 180, 216, ${0.3 * (1 - dist / 100)})`;
                        ctx.lineWidth = 1;
                        ctx.stroke();
                    }
                }
            });
            
            ctx.globalAlpha = 1;
            
            if (!this.isComplete) {
                requestAnimationFrame(animate);
            }
        };
        
        animate();
    }
    
    simulateLoading() {
        const stages = [
            { name: 'INICIANDO CONEXIÓN SEGURA', duration: 800, sound: 'stage' },
            { name: 'VERIFICANDO PROTOCOLOS', duration: 600, sound: 'stage' },
            { name: 'CARGANDO MÓDULOS PRINCIPALES', duration: 900, sound: 'stage' },
            { name: 'ESTABLECIENDO ENLACE GLOBAL', duration: 700, sound: 'stage' },
            { name: 'SINCRONIZANDO DATOS', duration: 600, sound: 'stage' },
            { name: 'PREPARANDO INTERFAZ', duration: 500, sound: 'stage' },
            { name: 'SISTEMA LISTO', duration: 400, sound: 'complete' }
        ];
        
        const stagesContainer = document.getElementById('loadingStages');
        const progressText = document.getElementById('progressText');
        
        let currentStage = 0;
        
        const updateStage = () => {
            if (currentStage >= stages.length) {
                this.completeLoading();
                return;
            }
            
            const stage = stages[currentStage];
            
            if (this.audioReady && stage.sound) {
                window.audioSystem.play(stage.sound);
            }
            
            if (progressText) {
                progressText.textContent = stage.name;
                progressText.classList.add('stage-change');
                setTimeout(() => progressText.classList.remove('stage-change'), 300);
            }
            
            if (stagesContainer) {
                const indicator = document.createElement('div');
                indicator.className = 'stage-indicator';
                indicator.innerHTML = `<span class="stage-check">✓</span> ${stage.name}`;
                stagesContainer.appendChild(indicator);
                stagesContainer.scrollTop = stagesContainer.scrollHeight;
            }
            
            if (this.audioReady) {
                window.audioSystem.play('progress');
            }
            
            const increment = 100 / stages.length;
            this.targetProgress = Math.min(100, (currentStage + 1) * increment);
            
            currentStage++;
            
            setTimeout(updateStage, stage.duration);
        };
        
        setTimeout(updateStage, 500);
    }
    
    animateProgress() {
        const progressBar = document.getElementById('progressBar');
        const progressPercent = document.getElementById('progressPercent');
        
        const animate = () => {
            if (this.progress < this.targetProgress) {
                this.progress += (this.targetProgress - this.progress) * 0.1;
                
                if (Math.abs(this.targetProgress - this.progress) < 0.5) {
                    this.progress = this.targetProgress;
                }
            }
            
            if (progressBar) progressBar.style.width = this.progress + '%';
            if (progressPercent) progressPercent.textContent = Math.floor(this.progress) + '%';
            
            if (!this.isComplete) {
                requestAnimationFrame(animate);
            }
        };
        
        animate();
    }
    
    completeLoading() {
        this.isComplete = true;
        this.targetProgress = 100;
        
        if (this.audioReady) {
            window.audioSystem.play('complete');
        }
        
        setTimeout(() => {
            const preloader = document.getElementById('cinematic-preloader');
            
            if (preloader) {
                preloader.classList.add('complete');
                
                setTimeout(() => {
                    if (this.audioReady) {
                        window.audioSystem.play('whoosh');
                    }
                    
                    preloader.style.animation = 'preloaderExit 1.5s cubic-bezier(0.77, 0, 0.175, 1) forwards';
                    
                    setTimeout(() => {
                        if (this.audioReady) {
                            window.audioSystem.stopAll();
                        }
                        
                        preloader.remove();
                        document.body.style.overflow = '';
                        
                        // ✅ GUARDAR QUE YA SE VIO EL PRELOADER
                        localStorage.setItem('hasSeenPreloader', 'true');
                        console.log('💾 Preloader guardado en localStorage - no se volverá a mostrar');
                        
                        document.dispatchEvent(new Event('preloaderComplete'));
                    }, 1500);
                }, 800);
            }
        }, 500);
    }
}

// ✅ SOLO INICIALIZAR SI NO SE HA VISTO ANTES
window.addEventListener('load', () => {
    const hasSeenPreloader = localStorage.getItem('hasSeenPreloader') === 'true';
    
    if (hasSeenPreloader) {
        console.log('✅ Preloader omitido - usuario ya lo vio');
        document.body.style.overflow = '';
    } else {
        console.log('🎬 Iniciando preloader cinematográfico');
        new CinematicPreloader();
    }
});

// ============================================
// 🔧 FUNCIÓN DE DEBUGGING (SOLO PARA DESARROLLO)
// ============================================
// Descomenta para poder resetear el preloader durante pruebas
/*
window.resetPreloader = function() {
    localStorage.removeItem('hasSeenPreloader');
    console.log('🔄 Preloader reseteado - recarga la página para verlo de nuevo');
    location.reload();
};
console.log('💡 TIP: Escribe resetPreloader() en la consola para ver el preloader de nuevo');
*/