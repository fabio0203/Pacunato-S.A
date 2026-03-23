// ============================================
// SISTEMA DE MODALES UNIVERSAL
// ============================================

/**
 * Muestra modal de éxito con información personalizada
 * @param {string} title - Título del modal
 * @param {string} message - Mensaje principal
 * @param {boolean} showInfo - Mostrar información adicional
 * @param {string} name - Nombre del usuario (opcional)
 * @param {string} email - Email del usuario (opcional)
 */
function showSuccessModal(title = '¡Felicitaciones!', message = 'Operación exitosa', showInfo = false, name = '', email = '') {
    // Crear modal si no existe
    if (!document.getElementById('universalSuccessModal')) {
        createSuccessModal();
    }
    
    const modal = document.getElementById('universalSuccessModal');
    const modalTitle = modal.querySelector('.modal-title');
    const modalMessage = modal.querySelector('.modal-message');
    const modalInfo = modal.querySelector('.modal-user-info');
    
    // Actualizar contenido
    modalTitle.textContent = title;
    modalMessage.innerHTML = message;
    
    // Mostrar/ocultar info adicional
    if (showInfo && (name || email)) {
        modalInfo.style.display = 'block';
        modalInfo.innerHTML = `
            ${name ? `<p><strong>Nombre:</strong> ${name}</p>` : ''}
            ${email ? `<p><strong>Email:</strong> ${email}</p>` : ''}
        `;
    } else {
        modalInfo.style.display = 'none';
    }
    
    // Mostrar modal
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
    
    // Confetti opcional (si existe la librería)
    if (typeof confetti !== 'undefined') {
        confetti({
            particleCount: 100,
            spread: 70,
            origin: { y: 0.6 }
        });
    }
    
    console.log('✅ Modal de éxito mostrado');
}

/**
 * Muestra modal de error
 * @param {string} message - Mensaje de error
 */
function showErrorModal(message = 'Hubo un error. Por favor intenta nuevamente.') {
    // Crear modal si no existe
    if (!document.getElementById('universalErrorModal')) {
        createErrorModal();
    }
    
    const modal = document.getElementById('universalErrorModal');
    const modalMessage = modal.querySelector('.error-modal-message');
    
    // Actualizar contenido
    modalMessage.textContent = message;
    
    // Mostrar modal
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
    
    console.log('❌ Modal de error mostrado:', message);
}

/**
 * Cierra el modal de éxito
 */
function closeSuccessModal() {
    const modal = document.getElementById('universalSuccessModal');
    if (modal) {
        modal.style.animation = 'fadeOut 0.3s ease';
        setTimeout(() => {
            modal.style.display = 'none';
            modal.style.animation = '';
            document.body.style.overflow = '';
        }, 300);
    }
}

/**
 * Cierra el modal de error
 */
function closeErrorModal() {
    const modal = document.getElementById('universalErrorModal');
    if (modal) {
        modal.style.animation = 'fadeOut 0.3s ease';
        setTimeout(() => {
            modal.style.display = 'none';
            modal.style.animation = '';
            document.body.style.overflow = '';
        }, 300);
    }
}

/**
 * Crea el HTML del modal de éxito dinámicamente
 */
function createSuccessModal() {
    const modalHTML = `
    <div id="universalSuccessModal" class="modal-overlay" style="display: none;">
        <div class="modal-container">
            <div class="modal-content">
                <!-- Icono de éxito con animación -->
                <div class="success-icon">
                    <div class="success-icon-circle">
                        <svg class="checkmark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52">
                            <circle class="checkmark-circle" cx="26" cy="26" r="25" fill="none"/>
                            <path class="checkmark-check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/>
                        </svg>
                    </div>
                </div>
                
                <!-- Título -->
                <h2 class="modal-title">¡Felicitaciones!</h2>
                
                <!-- Mensaje -->
                <p class="modal-message">
                    Operación exitosa
                </p>
                
                <!-- Información adicional del usuario -->
                <div class="modal-user-info" style="display: none;">
                </div>
                
                <!-- Información adicional -->
                <div class="modal-info">
                    <div class="info-item">
                        <i class="fas fa-clock"></i>
                        <span>Respuesta en 24 horas</span>
                    </div>
                    <div class="info-item">
                        <i class="fas fa-envelope"></i>
                        <span>Revisa tu correo</span>
                    </div>
                    <div class="info-item">
                        <i class="fas fa-phone"></i>
                        <span>Te llamaremos pronto</span>
                    </div>
                </div>
                
                <!-- Botones -->
                <div class="modal-actions">
                    <button class="btn-primary" onclick="closeSuccessModal()">
                        <i class="fas fa-check"></i>
                        Entendido
                    </button>
                </div>
            </div>
        </div>
    </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
}

/**
 * Crea el HTML del modal de error dinámicamente
 */
function createErrorModal() {
    const modalHTML = `
    <div id="universalErrorModal" class="modal-overlay" style="display: none;">
        <div class="modal-container">
            <div class="modal-content modal-error">
                <!-- Icono de error -->
                <div class="error-icon">
                    <div class="error-icon-circle">
                        <i class="fas fa-exclamation-triangle"></i>
                    </div>
                </div>
                
                <!-- Título -->
                <h2 class="modal-title">Algo salió mal</h2>
                
                <!-- Mensaje -->
                <p class="error-modal-message">
                    Hubo un error. Por favor intenta nuevamente.
                </p>
                
                <!-- Botones -->
                <div class="modal-actions">
                    <button class="btn-primary" onclick="closeErrorModal()">
                        <i class="fas fa-times"></i>
                        Cerrar
                    </button>
                </div>
            </div>
        </div>
    </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
}

// ============================================
// EVENT LISTENERS
// ============================================

// Cerrar modal con ESC
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeSuccessModal();
        closeErrorModal();
    }
});

// Cerrar modal al hacer click fuera (en el overlay)
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('modal-overlay')) {
        closeSuccessModal();
        closeErrorModal();
    }
});

console.log('✅ Sistema de modales universal cargado');