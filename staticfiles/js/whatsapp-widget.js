// ============================================
// WHATSAPP FLOATING WIDGET
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    const bubble = document.getElementById('whatsapp-bubble');
    const popup = document.getElementById('whatsapp-popup');
    const closeBtn = document.getElementById('whatsapp-close');
    
    if (!bubble || !popup) return;
    
    // Toggle popup
    bubble.addEventListener('click', function(e) {
        e.stopPropagation();
        const isActive = bubble.classList.contains('active');
        
        if (isActive) {
            closePopup();
        } else {
            openPopup();
        }
    });
    
    // Close when clicking outside
    document.addEventListener('click', function(e) {
        if (!popup.contains(e.target) && !bubble.contains(e.target)) {
            closePopup();
        }
    });
    
    // Prevent popup clicks from closing
    popup.addEventListener('click', function(e) {
        e.stopPropagation();
    });
    
    function openPopup() {
        bubble.classList.add('active');
        popup.classList.add('active');
        
        // Analytics tracking
        if (typeof trackEvent === 'function') {
            trackEvent('whatsapp_widget_open', {
                'event_category': 'WhatsApp Widget',
                'event_label': 'Widget Abierto'
            });
        }
    }
    
    function closePopup() {
        bubble.classList.remove('active');
        popup.classList.remove('active');
    }
    
    // Track WhatsApp link clicks
    const whatsappCTA = popup.querySelector('.whatsapp-cta');
    if (whatsappCTA) {
        whatsappCTA.addEventListener('click', function() {
            if (typeof trackEvent === 'function') {
                trackEvent('contact', {
                    'event_category': 'WhatsApp Widget',
                    'event_label': 'Conversación Iniciada',
                    'method': 'whatsapp_widget'
                });
            }
        });
    }
    
    // Auto-show after 5 seconds (optional)
    setTimeout(function() {
        bubble.classList.add('animated');
    }, 5000);
});