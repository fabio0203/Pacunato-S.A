// Newsletter JavaScript - CON SISTEMA DE MODALES UNIVERSAL
document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ Newsletter JS cargado');
    
    const newsletterForms = document.querySelectorAll('.newsletter-form');
    
    newsletterForms.forEach(form => {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const emailInput = this.querySelector('input[type="email"]');
            const nameInput = this.querySelector('input[name="name"]');
            const submitBtn = this.querySelector('button[type="submit"]');
            
            const email = emailInput.value.trim();
            const name = nameInput ? nameInput.value.trim() : '';
            
            // Validación
            if (!email) {
                showErrorModal('Por favor ingresa tu email');
                return;
            }
            
            // Validar formato de email
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                showErrorModal('Por favor ingresa un email válido');
                return;
            }
            
            // Deshabilitar botón mientras se procesa
            const originalBtnContent = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Suscribiendo...';
            
            try {
                const response = await fetch('/suscribir-newsletter/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({
                        email: email,
                        name: name,
                        page: window.location.href
                    })
                });
                
                const data = await response.json();
                
                if (response.ok && data.success) {
                    // ⭐ MOSTRAR MODAL DE ÉXITO
                    showSuccessModal(
                        '¡Bienvenido al Equipo! 🎉',
                        '¡Felicidades! Te has suscrito exitosamente al newsletter de Pacunato S.A.<br>Mantente atento a tu email para recibir nuestras últimas novedades, promociones exclusivas y contenido especial.',
                        true,  // Mostrar info del usuario
                        name || 'Suscriptor',
                        email
                    );
                    
                    // Limpiar formulario
                    form.reset();
                    
                    console.log('✅ Suscripción exitosa:', email);
                } else {
                    // Error del servidor
                    const errorMessage = data.message || 'Hubo un problema al suscribirte. Por favor intenta nuevamente.';
                    showErrorModal(errorMessage);
                    console.error('❌ Error en suscripción:', data.message);
                }
                
            } catch (error) {
                console.error('❌ Error de red:', error);
                showErrorModal('Error de conexión. Por favor verifica tu internet e intenta nuevamente.');
            } finally {
                // Restaurar botón
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnContent;
            }
        });
    });
});

// Función para obtener CSRF token
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