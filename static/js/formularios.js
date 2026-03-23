// Formularios de Cotización - CON MODAL UNIFICADO
document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ Formularios JS cargado');
    
    // ============================================
    // FORMULARIO DE COTIZACIÓN (todas las páginas)
    // ============================================
    const cotizacionForms = document.querySelectorAll('form[action*="cotizacion"]');
    
    cotizacionForms.forEach(form => {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const submitBtn = this.querySelector('button[type="submit"]');
            const formData = new FormData(this);
            
            // Validación básica
            const nombre = formData.get('nombre');
            const email = formData.get('email');
            const telefono = formData.get('telefono');
            const paisOrigen = formData.get('pais_origen');
            const paisDestino = formData.get('pais_destino');
            const tipoServicio = formData.get('tipo_servicio');
            const mensaje = formData.get('mensaje');
            
            if (!nombre || !email || !telefono || !paisOrigen || !paisDestino || !tipoServicio || !mensaje) {
                showErrorModal('Por favor completa todos los campos requeridos');
                return;
            }
            
            // Validar email
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                showErrorModal('Por favor ingresa un email válido');
                return;
            }
            
            // Deshabilitar botón
            const originalBtnContent = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Enviando...';
            
            try {
                const response = await fetch(this.action, {
                    method: 'POST',
                    body: formData
                });
                
                if (response.ok) {
                    // ⭐ MOSTRAR MODAL DE ÉXITO
                    showSuccessModal(
                        '¡Cotización Enviada! ✅',
                        `¡Gracias ${nombre}! Tu solicitud de cotización para la ruta ${paisOrigen} → ${paisDestino} ha sido recibida. Nuestro equipo la revisará y te contactará en menos de 24 horas.`,
                        true,
                        nombre,
                        email
                    );
                    
                    // Limpiar formulario
                    this.reset();
                    
                    console.log('✅ Cotización enviada exitosamente');
                } else {
                    showErrorModal('Hubo un problema al enviar tu solicitud. Por favor intenta nuevamente.');
                    console.error('❌ Error en respuesta del servidor');
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
    
    // ============================================
    // FORMULARIO DE ASESORÍA (si existe)
    // ============================================
    const asesoriaForms = document.querySelectorAll('form[action*="asesoria"]');
    
    asesoriaForms.forEach(form => {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const submitBtn = this.querySelector('button[type="submit"]');
            const formData = new FormData(this);
            
            // Validación básica
            const nombre = formData.get('nombre');
            const email = formData.get('email');
            const telefono = formData.get('telefono');
            const duda = formData.get('duda');
            
            if (!nombre || !email || !telefono || !duda) {
                showErrorModal('Por favor completa todos los campos requeridos');
                return;
            }
            
            // Validar email
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                showErrorModal('Por favor ingresa un email válido');
                return;
            }
            
            // Deshabilitar botón
            const originalBtnContent = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Enviando...';
            
            try {
                const response = await fetch(this.action, {
                    method: 'POST',
                    body: formData
                });
                
                if (response.ok) {
                    // ⭐ MOSTRAR MODAL DE ÉXITO
                    showSuccessModal(
                        '¡Consulta Enviada! 💬',
                        `¡Gracias ${nombre}! Tu consulta ha sido recibida. Nuestro equipo de expertos la revisará y te contactará pronto para ayudarte con tu duda.`,
                        true,
                        nombre,
                        email
                    );
                    
                    // Limpiar formulario
                    this.reset();
                    
                    console.log('✅ Consulta de asesoría enviada');
                } else {
                    showErrorModal('Hubo un problema al enviar tu consulta. Por favor intenta nuevamente.');
                    console.error('❌ Error en respuesta del servidor');
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

// ============================================
// FUNCIONES DE VALIDACIÓN
// ============================================

function validarEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

function validarTelefono(telefono) {
    // Permitir números, espacios, guiones, paréntesis y el símbolo +
    const regex = /^[\d\s\-\+\(\)]+$/;
    return regex.test(telefono) && telefono.replace(/\D/g, '').length >= 7;
}

// ============================================
// NOTA: Las funciones showSuccessModal y showErrorModal
// están definidas en el MODAL_UNIVERSAL.html
// Asegúrate de incluir ese archivo en base.html
// ============================================