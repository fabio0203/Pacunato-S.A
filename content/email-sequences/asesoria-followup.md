# Secuencia de Follow-up: Consulta de Asesoría
## Advisory Consultation Handler — 3 Emails + 1 Alerta Interna

*Para usar en n8n workflow: "Advisory - Handler - Asesoria"*
*Trigger: Nueva ConsultaAsesoria guardada en Django*
*SLA objetivo: Respuesta al usuario en < 2 horas en horario laboral*

---

## Alerta Interna al Equipo (Enviar: inmediatamente, al instante)

**Para:** info@pacunato.com (equipo interno)
**Asunto:** 🔔 [Nueva Consulta] {{nombre}} — Asesoría recibida

---

**NUEVA CONSULTA DE ASESORÍA**

**Nombre:** {{nombre}}
**Email:** {{email}}
**Teléfono:** {{telefono}}
**Fecha:** {{fecha_envio}}
**ID en sistema:** #{{id}}

---

**Consulta del cliente:**

> {{duda}}

---

**Acción requerida:** Responder al cliente en menos de 2 horas (horario laboral).

Si no puedes responder ahora, configura el estado en el admin de Django para que el sistema envíe una alerta de seguimiento.

👉 [Ver en Django Admin](https://pacunato.com/admin/website/consultaasesoria/{{id}}/change/)

---

## Email 1 — Auto-respuesta al Usuario (Enviar: inmediatamente)

**Para:** {{email}}
**Asunto:** Recibimos tu consulta — te respondemos muy pronto

**Preview text:** {{nombre}}, un asesor revisará tu consulta y te contactará hoy

---

Hola {{nombre}},

Recibimos tu consulta correctamente.

Uno de nuestros asesores la revisará y te contactará **a la brevedad posible**, generalmente dentro de las próximas 2 horas en horario laboral (Lunes-Viernes, 8am-6pm hora Panamá).

**Tu consulta:**
> *"{{duda|truncatechars:200}}"*

Si necesitas respuesta más rápida, escríbenos directamente por WhatsApp y te atendemos de inmediato:

📱 [Abrir WhatsApp ahora](https://wa.me/50764418437?text=Hola%2C%20acabo%20de%20enviar%20una%20consulta%20de%20asesoría%20y%20necesito%20respuesta%20urgente)

Mientras esperas, quizás te sea útil:
→ [Nuestros servicios completos](https://www.pacunato.com/servicios/)
→ [Guía de Importación para Centroamérica](https://www.pacunato.com/#guia-importacion) (gratis)

Con gusto te ayudamos,

**Equipo Pacunato S.A.**
📧 info@pacunato.com | 🌐 www.pacunato.com | 📱 +507 6441-8437

---

## Email 2 — Recordatorio Interno (24h sin marcar como procesado)

*Este email va al equipo interno, NO al cliente*

**Para:** info@pacunato.com
**Asunto:** ⚠️ SEGUIMIENTO PENDIENTE — {{nombre}} lleva 24h sin respuesta

---

**ALERTA: CONSULTA SIN RESPUESTA**

La siguiente consulta lleva **más de 24 horas** sin ser marcada como procesada en el sistema:

**Cliente:** {{nombre}} ({{email}})
**Teléfono:** {{telefono}}
**Recibida:** {{fecha_envio}}

**Consulta:**
> {{duda}}

**Acción requerida:** Contactar al cliente INMEDIATAMENTE.

👉 [Ver y procesar en Django Admin](https://pacunato.com/admin/website/consultaasesoria/{{id}}/change/)

*Este recordatorio se envió automáticamente por el sistema n8n de Pacunato.*

---

## Email 3 — Seguimiento al Cliente (Enviar: 48h si consulta marcada como procesada)

*Este email va al CLIENTE después de que el equipo marcó la consulta como resuelta*

**Para:** {{email}}
**Asunto:** {{nombre}}, ¿pudimos resolver tu consulta?

**Preview text:** Queremos asegurarnos de que tienes toda la información que necesitas

---

Hola {{nombre}},

Espero que la información que te brindó nuestro equipo haya sido útil para tu consulta.

Si tienes preguntas adicionales o quieres dar el siguiente paso — sea solicitar una cotización formal o profundizar en algún aspecto específico — estoy aquí para ayudarte.

**Próximos pasos que puedes tomar:**

1. **Solicitar cotización formal** → [Cotizar ahora](https://www.pacunato.com/#cotizacion)
   *Si ya tienes claridad sobre lo que necesitas, este es el siguiente paso natural*

2. **Hablar con un asesor** → [WhatsApp directo](https://wa.me/50764418437)
   *Para preguntas adicionales o aclaraciones*

3. **Leer más sobre el proceso** → [Nuestros servicios](https://www.pacunato.com/servicios/)
   *Si quieres entender mejor cómo trabajamos antes de decidir*

¿Hay algo más en lo que pueda ayudarte?

Saludos,

**{{nombre_ejecutivo}}**
Ejecutivo de Cuenta — Pacunato S.A.
📧 info@pacunato.com | 📱 +507 6441-8437

---

## Configuración en n8n

```
Workflow: Advisory - Handler - Asesoria
Trigger: Webhook POST desde Django (nueva ConsultaAsesoria)

Nodos:
1. Webhook → Recibir datos de la consulta
2. Send Email → Alerta interna al equipo (inmediato)
3. Send Email → Auto-respuesta al usuario (inmediato)
4. Wait 24h → IF procesado=false → Send Email recordatorio interno
5. Wait 48h desde procesado=true → Send Email seguimiento al cliente
6. Update Django → marcar enviado_n8n=true
```
