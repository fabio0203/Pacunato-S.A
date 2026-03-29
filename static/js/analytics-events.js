/**
 * analytics-events.js
 * GA4 Custom Event Tracking — Pacunato S.A.
 *
 * Tracks: form submissions, CTA clicks, WhatsApp clicks, newsletter sign-ups,
 * scroll depth, and phone/email link clicks.
 *
 * Requires Firebase Analytics (GA4) initialized in base.html.
 */

(function () {
    'use strict';

    // ─── Helpers ─────────────────────────────────────────────────────────────

    /** Fire a GA4 custom event safely (Firebase gtag wrapper). */
    function trackEvent(eventName, params) {
        if (typeof gtag === 'function') {
            gtag('event', eventName, params);
        } else if (typeof window.firebaseAnalytics !== 'undefined' && typeof window.firebaseAnalytics.logEvent === 'function') {
            window.firebaseAnalytics.logEvent(eventName, params);
        }
        // Debug log in development
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            console.log('[Analytics]', eventName, params);
        }
    }

    /** Get the current page path label for context. */
    function getPageLabel() {
        return window.location.pathname || '/';
    }

    // ─── 1. Form Submit — Cotización ──────────────────────────────────────────
    document.addEventListener('DOMContentLoaded', function () {

        // Cotización form (AJAX-based, tracked on success response)
        var cotizacionForm = document.getElementById('cotizacionForm') ||
            document.querySelector('form[data-form="cotizacion"]');

        if (cotizacionForm) {
            cotizacionForm.addEventListener('submit', function () {
                trackEvent('form_submit', {
                    form_name: 'cotizacion',
                    form_location: getPageLabel(),
                    event_category: 'Lead',
                    event_label: 'Solicitud de Cotización'
                });
            });
        }

        // ─── 2. Form Submit — Asesoría ────────────────────────────────────────
        var asesoriaForm = document.getElementById('asesoriaForm');

        if (asesoriaForm) {
            asesoriaForm.addEventListener('submit', function () {
                trackEvent('form_submit', {
                    form_name: 'asesoria',
                    form_location: getPageLabel(),
                    event_category: 'Lead',
                    event_label: 'Consulta de Asesoría'
                });
            });
        }

        // ─── 3. Newsletter Subscribe ──────────────────────────────────────────
        var newsletterForms = document.querySelectorAll(
            'form[action*="suscribir"], form[id*="newsletter"], .newsletter-form'
        );

        newsletterForms.forEach(function (form) {
            form.addEventListener('submit', function () {
                trackEvent('newsletter_subscribe', {
                    form_location: getPageLabel(),
                    event_category: 'Engagement',
                    event_label: 'Newsletter Subscription'
                });
            });
        });

        // ─── 4. CTA Button Clicks ─────────────────────────────────────────────
        var ctaButtons = document.querySelectorAll(
            '.btn-primary, .btn-secondary, .btn-outline, [class*="btn-lg"]'
        );

        ctaButtons.forEach(function (btn) {
            btn.addEventListener('click', function () {
                var label = btn.textContent.trim() || btn.getAttribute('aria-label') || 'CTA';
                var href = btn.getAttribute('href') || '';

                // Skip nav items and non-conversion CTAs
                if (href.indexOf('#cotizacion') !== -1 || label.toLowerCase().indexOf('cotiz') !== -1) {
                    trackEvent('cta_click', {
                        cta_label: label,
                        cta_destination: href,
                        cta_location: getPageLabel(),
                        event_category: 'Conversion',
                        event_label: 'CTA Cotizar'
                    });
                } else if (label.toLowerCase().indexOf('asesor') !== -1 || href.indexOf('asesoria') !== -1) {
                    trackEvent('cta_click', {
                        cta_label: label,
                        cta_destination: href,
                        cta_location: getPageLabel(),
                        event_category: 'Conversion',
                        event_label: 'CTA Asesoría'
                    });
                }
            });
        });

        // ─── 5. WhatsApp Clicks ───────────────────────────────────────────────
        var whatsappLinks = document.querySelectorAll(
            'a[href*="wa.me"], a[href*="whatsapp"], .whatsapp-cta, .social-link.whatsapp'
        );

        whatsappLinks.forEach(function (link) {
            link.addEventListener('click', function () {
                trackEvent('whatsapp_click', {
                    click_location: getPageLabel(),
                    event_category: 'Contact',
                    event_label: 'WhatsApp Click'
                });
            });
        });

        // ─── 6. Phone Clicks ──────────────────────────────────────────────────
        var phoneLinks = document.querySelectorAll('a[href^="tel:"]');

        phoneLinks.forEach(function (link) {
            link.addEventListener('click', function () {
                trackEvent('phone_click', {
                    click_location: getPageLabel(),
                    event_category: 'Contact',
                    event_label: 'Phone Click'
                });
            });
        });

        // ─── 7. Email Clicks ──────────────────────────────────────────────────
        var emailLinks = document.querySelectorAll('a[href^="mailto:"], a[href*="mail.google.com"]');

        emailLinks.forEach(function (link) {
            link.addEventListener('click', function () {
                trackEvent('email_click', {
                    click_location: getPageLabel(),
                    event_category: 'Contact',
                    event_label: 'Email Click'
                });
            });
        });

        // ─── 8. Blog Post Read Progress ───────────────────────────────────────
        if (document.querySelector('.post-content-body')) {
            var scrollMilestones = { 25: false, 50: false, 75: false, 100: false };
            var postTitle = document.querySelector('.post-title');
            var postLabel = postTitle ? postTitle.textContent.trim() : getPageLabel();

            window.addEventListener('scroll', function () {
                var scrollTop = window.scrollY || document.documentElement.scrollTop;
                var docHeight = document.documentElement.scrollHeight - window.innerHeight;
                if (docHeight <= 0) return;

                var scrollPct = Math.round((scrollTop / docHeight) * 100);

                [25, 50, 75, 100].forEach(function (milestone) {
                    if (scrollPct >= milestone && !scrollMilestones[milestone]) {
                        scrollMilestones[milestone] = true;
                        trackEvent('scroll_depth', {
                            percent_scrolled: milestone,
                            content_title: postLabel,
                            event_category: 'Engagement',
                            event_label: 'Blog Read ' + milestone + '%'
                        });
                    }
                });
            }, { passive: true });
        }

        // ─── 9. Lead Magnet Download / Interest ──────────────────────────────
        var leadMagnetLinks = document.querySelectorAll(
            '[data-event="lead-magnet"], .lead-magnet-cta, a[href*="lead-magnet"], a[href*="guia"]'
        );

        leadMagnetLinks.forEach(function (link) {
            link.addEventListener('click', function () {
                var label = link.dataset.magnetTitle || link.textContent.trim() || 'Lead Magnet';
                trackEvent('lead_magnet_click', {
                    magnet_title: label,
                    click_location: getPageLabel(),
                    event_category: 'Lead Generation',
                    event_label: label
                });
            });
        });

    }); // end DOMContentLoaded

    // ─── 10. Expose helper for inline use in forms ────────────────────────────
    window.pacunatoTrack = trackEvent;

})();
