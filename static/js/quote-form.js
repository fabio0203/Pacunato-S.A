// ============================================
// QUOTE-FORM.JS CON MODAL - VERSIÓN AJAX
// Usa el sistema de modales universal
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('📝 Quote Form Script (con Modal Universal) cargado');
    
    const quoteForm = document.getElementById('quoteForm');
    
    if (!quoteForm) {
        console.warn('⚠️ Formulario de cotización no encontrado en esta página');
        return;
    }
    
    console.log('✅ Formulario de cotización encontrado');
    
    quoteForm.addEventListener('submit', async function(e) {
        e.preventDefault(); // Prevenir envío tradicional
        
        console.log('📤 Formulario enviándose por AJAX...');
        
        const submitBtn = this.querySelector('button[type="submit"]');
        const btnText = submitBtn.querySelector('#btnText');
        const btnLoading = submitBtn.querySelector('#btnLoading');
        
        // Validar todos los campos
        let isValid = true;
        const requiredFields = [
            { id: 'nombre', name: 'Nombre' },
            { id: 'email', name: 'Email' },
            { id: 'telefono', name: 'Teléfono' },
            { id: 'pais_origen', name: 'País de Origen' },
            { id: 'pais_destino', name: 'País de Destino' },
            { id: 'tipo_servicio', name: 'Tipo de Servicio' },
            { id: 'mensaje', name: 'Mensaje' }
        ];
        
        // Limpiar errores previos
        document.querySelectorAll('.field-error').forEach(error => error.remove());
        document.querySelectorAll('.error').forEach(field => field.classList.remove('error'));
        
        // Validar cada campo
        for (const field of requiredFields) {
            const element = document.getElementById(field.id);
            if (!element) continue;
            
            const value = element.value.trim();
            if (!value) {
                showFieldError(element, `${field.name} es requerido`);
                isValid = false;
            } else {
                // Validaciones específicas
                if (field.id === 'email') {
                    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                    if (!emailRegex.test(value)) {
                        showFieldError(element, 'Email inválido');
                        isValid = false;
                    }
                }
                
                if (field.id === 'telefono') {
                    const phoneRegex = /^[\d\s\-\+\(\)]+$/;
                    if (!phoneRegex.test(value)) {
                        showFieldError(element, 'Teléfono inválido');
                        isValid = false;
                    }
                }
                
                if ((field.id === 'pais_origen' || field.id === 'pais_destino') && value.length < 3) {
                    showFieldError(element, 'Debe tener al menos 3 caracteres');
                    isValid = false;
                }
                
                if (field.id === 'mensaje' && value.length < 10) {
                    showFieldError(element, 'El mensaje debe tener al menos 10 caracteres');
                    isValid = false;
                }
            }
        }
        
        if (!isValid) {
            console.error('❌ Validación falló');
            const firstError = document.querySelector('.error');
            if (firstError) {
                firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                firstError.focus();
            }
            return false;
        }
        
        console.log('✅ Validación exitosa');
        
        // Mostrar loading
        if (submitBtn) submitBtn.disabled = true;
        if (btnText) btnText.style.display = 'none';
        if (btnLoading) btnLoading.style.display = 'inline';
        
        // Preparar datos
        const formData = new FormData(quoteForm);
        
        try {
            // Obtener CSRF token
            const csrftoken = getCookie('csrftoken');
            
            // Enviar por AJAX
            const response = await fetch(quoteForm.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: formData
            });
            
            if (response.ok) {
                console.log('✅ Formulario enviado exitosamente');
                
                // Limpiar formulario
                quoteForm.reset();
                
                // ⭐ MOSTRAR MODAL DE ÉXITO (usa función global del sistema de modales)
                showSuccessModal();
                
                // Scroll al inicio después de cerrar modal
                setTimeout(() => {
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                }, 500);
                
            } else {
                console.error('❌ Error del servidor:', response.status);
                showErrorModal('Hubo un problema al enviar tu solicitud. Por favor intenta nuevamente.');
            }
            
        } catch (error) {
            console.error('❌ Error:', error);
            showErrorModal('Hubo un error al enviar la solicitud. Por favor intenta nuevamente o contáctanos por WhatsApp.');
        } finally {
            // Rehabilitar botón
            if (submitBtn) submitBtn.disabled = false;
            if (btnText) btnText.style.display = 'inline';
            if (btnLoading) btnLoading.style.display = 'none';
        }
    });
    
    console.log('✅ Event listener de formulario (AJAX con Modal Universal) configurado');
});

// ============================================
// VALIDACIÓN EN TIEMPO REAL
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('.quote-form input, .quote-form select, .quote-form textarea');
    
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.hasAttribute('required') && this.value.trim()) {
                validateField(this);
            }
        });
        
        input.addEventListener('input', function() {
            if (this.classList.contains('error')) {
                const existingError = this.parentElement.querySelector('.field-error');
                if (existingError) existingError.remove();
                this.classList.remove('error');
            }
        });
    });
});

function validateField(field) {
    const value = field.value.trim();
    field.classList.remove('error');
    const existingError = field.parentElement.querySelector('.field-error');
    if (existingError) existingError.remove();
    
    if (field.type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            showFieldError(field, 'Email inválido');
            return false;
        }
    }
    
    if (field.type === 'tel' && value) {
        const phoneRegex = /^[\d\s\-\+\(\)]+$/;
        if (!phoneRegex.test(value)) {
            showFieldError(field, 'Teléfono inválido');
            return false;
        }
    }
    
    if ((field.id === 'pais_origen' || field.id === 'pais_destino') && value.length > 0 && value.length < 3) {
        showFieldError(field, 'Debe tener al menos 3 caracteres');
        return false;
    }
    
    return true;
}

function showFieldError(field, message) {
    field.classList.add('error');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error';
    errorDiv.textContent = message;
    errorDiv.style.color = '#FF6B6B';
    errorDiv.style.fontSize = '0.875rem';
    errorDiv.style.marginTop = '0.5rem';
    field.parentElement.appendChild(errorDiv);
}

// ============================================
// HELPER FUNCTIONS
// ============================================
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// ============================================
// ESTILOS CSS ADICIONALES
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    if (!document.getElementById('form-error-styles')) {
        const style = document.createElement('style');
        style.id = 'form-error-styles';
        style.innerHTML = `
            .quote-form input.error,
            .quote-form select.error,
            .quote-form textarea.error {
                border-color: #FF6B6B !important;
                animation: shake 0.3s ease;
            }
            
            @keyframes shake {
                0%, 100% { transform: translateX(0); }
                25% { transform: translateX(-10px); }
                75% { transform: translateX(10px); }
            }
            
            .field-error {
                animation: fadeIn 0.3s ease;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(-5px); }
                to { opacity: 1; transform: translateY(0); }
            }
        `;
        document.head.appendChild(style);
    }
});

console.log('✅ Quote Form Script (AJAX con Modal Universal) completamente cargado');