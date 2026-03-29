# Secuencia de Bienvenida: Newsletter
## Welcome Sequence — 3 Emails

*Para usar en n8n workflow: "Newsletter - Welcome - Subscriber"*
*Trigger: Nuevo NewsletterSubscriber activo en Django*
*Objetivo: Convertir suscriptor en lead de cotización en 7-10 días*

---

## Email 1 — Bienvenida + Entrega del Lead Magnet (Enviar: inmediatamente)

**Asunto:** 🎁 Tu Guía de Importación está aquí, {{nombre}}

**Preview text:** Más un consejo que usamos con nuestros clientes desde día uno

---

Hola {{nombre}},

Bienvenido/a a la comunidad de Pacunato S.A.

Como prometimos, aquí está tu **Guía de Importación para Empresas Centroamericanas**:

👉 **[Descargar / Leer la Guía Completa](https://www.pacunato.com/content/guia-importacion-centroamerica/)**

La guía cubre:
- Los 7 errores más costosos al importar (y cómo evitarlos)
- Cómo verificar si un proveedor extranjero es legítimo
- INCOTERMS en español, sin complicaciones
- Los documentos que necesitas para cada país centroamericano
- Una calculadora de costos de importación

---

**Un consejo que no está en la guía:**

El momento más peligroso de una importación no es el envío — es antes de pagar. Una vez que el dinero sale, tus opciones se reducen drásticamente.

Por eso siempre recomendamos verificar primero, pagar después. Si algún proveedor te presiona para pagar antes de mostrarte documentación, es una señal de alerta.

Si estás considerando una importación próximamente, con gusto revisamos tu caso sin costo:
👉 [Hablar con un asesor](https://wa.me/50764418437?text=Hola%2C%20me%20suscribí%20al%20newsletter%20y%20quisiera%20hablar%20sobre%20una%20importación)

Buen provecho con la guía,

**Equipo Pacunato S.A.**
🌐 www.pacunato.com | 📧 info@pacunato.com

---
*Recibirás actualizaciones de comercio internacional, logística y oportunidades de negocio.*
*Para darte de baja, responde este correo con "Cancelar".*

---

## Email 2 — Valor / Caso de Uso (Enviar: Día 3)

**Asunto:** Cómo una empresa tica redujo sus costos de importación 28%

**Preview text:** No por hacer lo que todos hacen — sino por hacer una pregunta diferente

---

Hola {{nombre}},

Quiero contarte algo que pasó con uno de nuestros clientes en Costa Rica.

Tenían un proveedor de China con el que llevaban 2 años trabajando. Buen producto, entregas razonablemente puntuales. Estaban "conformes".

Cuando nos contactaron, les hicimos una pregunta simple: *¿Cuándo fue la última vez que compararon precios con proveedores alternativos?*

La respuesta fue: *"Nunca, ya confiamos en este".*

Hicimos una búsqueda de proveedores alternativos con especificaciones idénticas. Encontramos tres opciones de calidad comparable. El precio más competitivo era **28% más bajo** que lo que venían pagando.

No cambiaron de proveedor inmediatamente — primero verificamos la calidad con muestras. El nuevo proveedor las pasó. Hoy trabajan con ambos, usando el competidor como palanca de negociación.

---

Este proceso — buscar, comparar, verificar — es exactamente lo que hacemos para cada cliente.

¿Tienes un proveedor con el que llevas tiempo trabajando y no has comparado recientemente?
→ [Contáctanos para una revisión sin costo](https://www.pacunato.com/asesoria/)

Hasta pronto,

**Equipo Pacunato S.A.**

---

## Email 3 — Invitación a cotizar (Enviar: Día 7)

**Asunto:** {{nombre}}, ¿en qué estás trabajando ahora?

**Preview text:** Si hay una importación en tu radar, este es el momento

---

Hola {{nombre}},

Hace una semana te suscribiste al newsletter de Pacunato y descargaste la guía de importación.

Quiero hacerte una pregunta directa: **¿Hay algún proyecto de importación en tu radar para los próximos meses?**

No necesitas tener todo definido. A veces lo único que hay es una idea: "quiero traer X producto", "quiero mejorar el proveedor de Y", "quiero empezar a importar en lugar de comprar local".

Con eso alcanza para una conversación inicial sin compromiso.

Lo que obtienes de esa conversación:
- Una evaluación honesta de si tiene sentido importar ese producto
- Una estimación de costos y tiempos
- Recomendaciones sobre dónde buscar proveedores para ese tipo de producto

Es gratis. No hay compromiso de contratar.

Si te interesa:
→ **[Agendar conversación por WhatsApp](https://wa.me/50764418437?text=Hola%2C%20soy%20suscriptor%20del%20newsletter%20y%20quisiera%20hablar%20sobre%20un%20proyecto%20de%20importación)**
→ **[Llenar formulario de cotización](https://www.pacunato.com/#cotizacion)**

Si por ahora solo quieres seguir recibiendo contenido útil, perfecto también. Cada 2 semanas enviamos actualizaciones de comercio internacional, tendencias de logística y tips prácticos.

Saludos,

**Equipo Pacunato S.A.**
📧 info@pacunato.com | 📱 +507 6441-8437

---

## Configuración en n8n

```
Workflow: Newsletter - Welcome - Subscriber
Trigger: Webhook POST desde Django (nuevo NewsletterSubscriber con is_active=true)

Nodos:
1. Webhook → Recibir datos del suscriptor
2. Send Email → Email 1 Bienvenida + guía (inmediato)
3. Wait 3d → Send Email → Email 2 Caso de uso
4. Wait 7d desde suscripción → Send Email → Email 3 CTA cotización
5. IF email_abierto OR link_clicked → Tag "engaged" en sistema
6. Update Django → notas="welcome_sequence_completed"

Condición de salida anticipada:
- Si el suscriptor llena un formulario de cotización → salir del flujo y entrar al de nurturing
```
