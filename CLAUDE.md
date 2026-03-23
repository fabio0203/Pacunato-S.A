# CLAUDE.md - Proyecto Pacunato S.A. + n8n Automation

## 🎯 Propósito del Proyecto

Este proyecto es la plataforma web de **Pacunato S.A.**, una empresa panameña de logística y comercio internacional. El objetivo principal es **automatizar workflows de generación de leads, marketing y operaciones usando n8n**, reemplazando la integración actual con Make.com.

### Misión
Usar n8n para crear workflows profesionales de alta calidad que automaticen:
- Lead nurturing y seguimiento de cotizaciones
- Email marketing y campañas automatizadas
- Prospección y generación de leads
- Procesamiento de consultas de asesoría
- Gestión de suscriptores del newsletter
- Integraciones con APIs y servicios externos

---

## 🏗️ Arquitectura del Proyecto

### Stack Tecnológico
- **Backend**: Django 6.0.1
- **Python**: 3.13+
- **Base de datos**: SQLite (desarrollo) → PostgreSQL/MySQL (producción)
- **Automatización**: n8n (self-hosted en cloud)
- **Frontend**: HTML5, CSS3, JavaScript vanilla

### Estructura del Proyecto
```
pacunato-web/
├── pacunato_project/     # Configuración Django
│   ├── settings.py       # Configuración principal
│   └── urls.py           # Routing principal
├── website/              # App principal
│   ├── models.py         # Modelos de datos
│   ├── views.py          # Lógica de vistas
│   ├── admin.py          # Panel de administración
│   └── urls.py           # URLs de la app
├── templates/            # Templates HTML
├── static/               # CSS, JS, imágenes
├── media/                # Uploads de usuarios
└── db.sqlite3            # Base de datos
```

---

## 📊 Modelos de Datos

### 1. SolicitudCotizacion
**Propósito**: Captura solicitudes de cotización de servicios de logística

**Campos principales**:
- `nombre` (CharField): Nombre completo del solicitante
- `empresa` (CharField): Empresa del solicitante (opcional)
- `email` (EmailField): Email de contacto
- `telefono` (CharField): Número de teléfono
- `pais_origen` (CharField): País de origen de la mercancía
- `pais_destino` (CharField): País de destino
- `tipo_servicio` (CharField): Tipo de servicio solicitado
- `mensaje` (TextField): Descripción del proyecto/necesidad

**Metadata**:
- `fecha_envio` (DateTimeField): Timestamp de la solicitud
- `ip_address` (GenericIPAddressField): IP del usuario
- `user_agent` (CharField): Navegador/dispositivo
- `procesado` (BooleanField): Estado de procesamiento
- `enviado_make` (BooleanField): Si fue enviado a Make.com (deprecar)
- `fecha_procesamiento` (DateTimeField): Cuándo fue procesado
- `notas_admin` (TextField): Notas internas

**Workflow esperado**:
1. Usuario completa formulario en el sitio
2. Se guarda en base de datos
3. **Trigger n8n**: Enviar notificación por email al equipo
4. **Trigger n8n**: Agregar a CRM (futuro)
5. **Trigger n8n**: Iniciar secuencia de follow-up automático
6. Admin marca como procesado en Django admin

---

### 2. ConsultaAsesoria
**Propósito**: Captura consultas de asesoría de clientes potenciales

**Campos principales**:
- `nombre` (CharField): Nombre completo
- `email` (EmailField): Email de contacto
- `telefono` (CharField): Número de teléfono
- `duda` (TextField): Pregunta o consulta del usuario

**Metadata**: Similar a SolicitudCotizacion (fecha_envio, ip_address, user_agent, procesado, etc.)

**Workflow esperado**:
1. Usuario envía consulta desde página `/asesoria`
2. Se guarda en base de datos
3. **Trigger n8n**: Enviar notificación inmediata al equipo
4. **Trigger n8n**: Respuesta automática al usuario confirmando recepción
5. **Trigger n8n**: Recordatorio si no se responde en 24h

---

### 3. NewsletterSubscriber
**Propósito**: Gestión de suscriptores del newsletter

**Campos principales**:
- `email` (EmailField, unique): Email del suscriptor
- `name` (CharField): Nombre (opcional)
- `is_active` (BooleanField): Estado de suscripción activa
- `subscribed_date` (DateTimeField): Fecha de suscripción
- `consent_given` (BooleanField): Consentimiento GDPR
- `consent_date` (DateTimeField): Fecha del consentimiento
- `unsubscribed_date` (DateTimeField): Fecha de baja (si aplica)

**Metadata**: ip_address, user_agent, source_page, sent_to_make, notes

**Workflow esperado**:
1. Usuario se suscribe desde el sitio
2. Se guarda en base de datos con consentimiento GDPR
3. **Trigger n8n**: Email de bienvenida
4. **Trigger n8n**: Agregar a lista de email marketing
5. **Trigger n8n**: Campañas periódicas (semanal/mensual)
6. **Trigger n8n**: Reactivación de suscriptores inactivos

---

### 4. BlogPost
**Propósito**: Sistema de blog corporativo para SEO y content marketing

**Campos principales**:
- `title` (CharField): Título del artículo
- `slug` (SlugField): URL-friendly identifier
- `excerpt` (TextField): Resumen breve
- `content` (TextField): Contenido completo
- `featured_image` (ImageField): Imagen destacada
- `category` (CharField): eventos, logística, comercio, tendencias
- `author` (CharField): Autor del artículo
- `views` (IntegerField): Contador de vistas totales
- `tags` (ManyToMany): Etiquetas del artículo
- `is_published` (BooleanField): Estado de publicación
- `is_featured` (BooleanField): Artículo destacado

**Workflow esperado**:
1. Admin publica nuevo artículo
2. **Trigger n8n**: Enviar email a suscriptores del newsletter
3. **Trigger n8n**: Publicar en redes sociales (futuro)
4. **Trigger n8n**: Notificar a Slack/Discord del equipo

---

### 5. BlogPostView
**Propósito**: Tracking de vistas únicas por IP para analytics

**Campos**: post (FK), ip_address, user_agent, viewed_at

---

## 🔗 Integraciones Actuales (Make.com - A MIGRAR)

### Webhooks Actuales
1. **MAKE_WEBHOOK_COTIZACION**: Procesa SolicitudCotizacion
2. **MAKE_WEBHOOK_ASESORIA**: Procesa ConsultaAsesoria
3. **Newsletter webhook**: No configurado actualmente (string vacía en código)

### Código Relevante
- [views.py:322-344](website/views.py#L322-L344): Función `enviar_a_make(webhook_url, data)`
- [views.py:346-384](website/views.py#L346-L384): Función `enviar_a_make_newsletter(subscriber)`
- [views.py:137-150](website/views.py#L137-L150): Envío de ConsultaAsesoria a Make
- [views.py:201-219](website/views.py#L201-L219): Envío de SolicitudCotizacion a Make

---

## 🤖 Configuración de n8n

### Instancia
- **URL Base**: https://eduarodriguez.app.n8n.cloud/
- **MCP Server HTTP**: https://eduarodriguez.app.n8n.cloud/mcp-server/http
- **Tipo**: n8n Cloud (Hosted)
- **API Key**: [PENDIENTE - Usuario proporcionará]

**Cómo obtener API Key**:
1. Acceder a Settings (engranaje superior derecha)
2. Ir a sección "API"
3. Crear API Key si no existe
4. Copiar el key generado

### Herramientas Disponibles

#### 1. n8n MCP Server
- **Paquete NPM**: n8n-mcp@2.33.5
- **Propósito**: Servidor MCP para interactuar con la API de n8n
- **Instalación**: ✅ COMPLETADO (instalado globalmente via npm)
- **Database**: 803 nodos cargados, 2737 templates indexados

#### 2. n8n Skills
- **Repositorio**: https://github.com/czlonkowski/n8n-skills.git
- **Propósito**: 7 skills profesionales para trabajar con n8n
- **Instalación**: ✅ COMPLETADO (instalados en ~/.claude/skills/)
- **Skills activos**:
  - n8n-expression-syntax
  - n8n-mcp-tools-expert
  - n8n-workflow-patterns
  - n8n-validation-expert
  - n8n-node-configuration
  - n8n-code-javascript
  - n8n-code-python

---

## 🎯 Workflows Prioritarios a Crear

### 1. Lead Qualification & Nurturing (ALTA PRIORIDAD)
**Trigger**: Nueva SolicitudCotizacion
**Flujo**:
1. Recibir webhook de Django
2. Validar datos
3. Enviar notificación por email al equipo de ventas
4. Enviar email de confirmación al lead
5. Esperar 2 días → Enviar follow-up si no hay respuesta
6. Esperar 1 semana → Enviar segundo follow-up
7. Clasificar lead como "cold" si no responde en 14 días

### 2. Advisory Consultation Handler (ALTA PRIORIDAD)
**Trigger**: Nueva ConsultaAsesoria
**Flujo**:
1. Recibir webhook de Django
2. Enviar notificación inmediata a Slack/Email
3. Enviar auto-respuesta al usuario (esperamos responder en 24h)
4. Si no se marca como procesado en 24h → Enviar alerta al equipo
5. Cuando se marca como procesado → Enviar email de seguimiento

### 3. Newsletter Campaign Manager (MEDIA PRIORIDAD)
**Trigger**: Nuevo suscriptor o publicación de blog
**Flujo**:
1. Email de bienvenida a nuevo suscriptor
2. Agregar a lista de mailchimp/sendgrid
3. Cuando se publica nuevo blog → Enviar a todos los suscriptores activos
4. Tracking de aperturas y clicks
5. Reactivación de suscriptores inactivos (90 días sin abrir)

### 4. Prospección y Generación de Leads (MEDIA PRIORIDAD)
**Trigger**: Manual o programado
**Flujo**:
1. Buscar empresas potenciales en directorios/APIs
2. Enriquecer datos de contacto
3. Segmentar por industria/tamaño
4. Enviar campañas de cold email personalizadas
5. Tracking de respuestas y engagement
6. Crear tareas de seguimiento para equipo de ventas

### 5. Data Sync & ETL (BAJA PRIORIDAD)
**Trigger**: Programado (diario)
**Flujo**:
1. Sincronizar leads de Django → CRM externo
2. Limpiar datos duplicados
3. Actualizar estados de procesamiento
4. Generar reportes de métricas
5. Enviar dashboard semanal al equipo

---

## 🛠️ Directrices para Claude

### Nivel de Autonomía
**NIVEL: TOTAL - Crear y ejecutar workflows automáticamente**

Claude tiene permiso para:
- ✅ Crear workflows nuevos en n8n sin pedir confirmación previa
- ✅ Modificar workflows existentes
- ✅ Activar y ejecutar workflows
- ✅ Configurar webhooks y triggers
- ✅ Integrar con APIs externas
- ✅ Instalar nodos adicionales si es necesario

**Restricciones**:
- ❌ No eliminar workflows sin confirmar con el usuario
- ❌ No desactivar webhooks críticos sin confirmar
- ❌ No modificar la base de datos directamente sin supervisión

### Estándares de Calidad

#### 1. Naming Conventions
- **Workflows**: `[Categoría] - [Acción] - [Objeto]`
  - Ejemplo: `Lead - Nurture - Cotizacion`
  - Ejemplo: `Marketing - Send - Newsletter`
- **Nodos**: Nombres descriptivos en español
- **Variables**: snake_case para mantener consistencia con Django

#### 2. Error Handling
- Todos los workflows DEBEN incluir manejo de errores
- Usar nodos "Error Trigger" para capturar fallos
- Enviar notificaciones de errores críticos al equipo
- Logs detallados para debugging

#### 3. Testing
- Probar cada workflow con datos de prueba antes de activar
- Validar que los datos lleguen correctamente desde Django
- Verificar que los emails se envíen correctamente
- Documentar casos de prueba

#### 4. Performance
- Evitar loops infinitos
- Usar batch processing para grandes volúmenes
- Implementar rate limiting cuando se integre con APIs externas
- Optimizar para ejecución rápida (< 5 segundos para workflows simples)

### Documentación Requerida

Para cada workflow creado, Claude debe generar:

#### 1. Documentación Técnica Detallada
```markdown
## Workflow: [Nombre]

### Propósito
[Descripción clara del objetivo]

### Trigger
- Tipo: [Webhook/Schedule/Manual]
- URL: [Si es webhook]
- Frecuencia: [Si es schedule]

### Nodos
1. **[Nombre del nodo]**
   - Tipo: [Webhook/HTTP Request/Email/etc]
   - Configuración: [Detalles clave]
   - Output: [Qué datos produce]

2. **[Siguiente nodo]**
   ...

### Variables de Entorno
- `N8N_API_KEY`: [Descripción]
- `DJANGO_WEBHOOK_SECRET`: [Descripción]

### Dependencias
- API de SendGrid (email)
- Credenciales de Django

### Error Handling
- [Describir qué pasa si falla cada paso]
```

#### 2. Casos de Uso y Ejemplos
```markdown
### Caso de Uso 1: Lead de Cotización desde Home
**Escenario**: Usuario completa formulario de cotización en la página de inicio

**Input esperado**:
```json
{
  "nombre": "Juan Pérez",
  "email": "juan@ejemplo.com",
  "empresa": "Importadora XYZ",
  ...
}
```

**Output esperado**:
- Email enviado al equipo de ventas
- Auto-respuesta enviada al lead
- Lead agregado a secuencia de follow-up

**Tiempo de ejecución**: ~3 segundos
```

#### 3. Diagramas Visuales del Flujo
```markdown
### Diagrama del Flujo

```
[Webhook Django]
    ↓
[Validar Datos]
    ↓
[¿Datos válidos?] ────No────> [Registrar Error] → [Notificar Admin]
    ↓ Sí
[Enviar Email Equipo]
    ↓
[Enviar Auto-respuesta]
    ↓
[Agregar a CRM]
    ↓
[Iniciar Secuencia Follow-up]
```
```

---

## 🔐 Credenciales y Configuración

### Configuración MCP Server (COMPLETADO)

**Archivo**: `~/.mcp.json` (ya creado)
**Estado**: ⚠️ Requiere API Key

```json
{
  "mcpServers": {
    "n8n-mcp": {
      "command": "npx",
      "args": ["n8n-mcp"],
      "env": {
        "MCP_MODE": "stdio",
        "LOG_LEVEL": "info",
        "DISABLE_CONSOLE_OUTPUT": "false",
        "N8N_API_URL": "https://eduarodriguez.app.n8n.cloud",
        "N8N_API_KEY": "YOUR_API_KEY_HERE"  ⬅️ ACTUALIZAR AQUÍ
      }
    }
  }
}
```

**Cómo obtener el API Key de n8n Cloud**:

1. **Método 1**: Settings → API Keys
   - Click en el engranaje (Settings) en la esquina superior derecha
   - Busca "API Keys" en el menú lateral
   - Click "Create API Key"
   - Copia el key generado

2. **Método 2**: Perfil de Usuario → Settings → API Keys
   - Click en tu foto/inicial (esquina superior derecha)
   - Settings → API Keys
   - Create API Key

3. **Método 3**: Si no encuentras API Keys
   - Es posible que no tengas permisos de administrador
   - O que n8n Cloud esté usando el MCP Server HTTP integrado
   - Endpoint disponible: `https://eduarodriguez.app.n8n.cloud/mcp-server/http`

**Para actualizar el API Key**:
```bash
# Editar el archivo .mcp.json
nano ~/.mcp.json

# O directamente desde Windows
notepad C:\Users\turin\.mcp.json
```

### Django Settings
```python
# settings.py
N8N_WEBHOOK_BASE_URL = "https://eduarodriguez.app.n8n.cloud/webhook/"
N8N_API_KEY = "[USUARIO PROPORCIONARÁ]"

# Webhooks específicos (actualizar cuando se creen en n8n)
N8N_WEBHOOK_COTIZACION = f"{N8N_WEBHOOK_BASE_URL}cotizacion"
N8N_WEBHOOK_ASESORIA = f"{N8N_WEBHOOK_BASE_URL}asesoria"
N8N_WEBHOOK_NEWSLETTER = f"{N8N_WEBHOOK_BASE_URL}newsletter"
```

### Seguridad
- Usar HMAC signatures para validar webhooks
- Variables de entorno para API keys
- No hardcodear credenciales en código
- Rotar API keys periódicamente
- El archivo .mcp.json contiene credenciales sensibles - no commitear a git

---

## 📋 Checklist de Implementación

### Fase 1: Setup (PENDIENTE)
- [ ] Instalar n8n-mcp server
- [ ] Instalar n8n-skills
- [ ] Configurar API key de n8n en Django
- [ ] Probar conexión con instancia n8n
- [ ] Crear primeros webhooks de prueba

### Fase 2: Workflows Core (PENDIENTE)
- [ ] Crear workflow: Lead Qualification & Nurturing
- [ ] Crear workflow: Advisory Consultation Handler
- [ ] Crear workflow: Newsletter Campaign Manager
- [ ] Actualizar views.py para usar n8n en lugar de Make.com
- [ ] Testing end-to-end de cada workflow

### Fase 3: Workflows Avanzados (PENDIENTE)
- [ ] Crear workflow: Prospección y generación de leads
- [ ] Crear workflow: Data Sync & ETL
- [ ] Integración con CRM externo
- [ ] Dashboard de métricas

### Fase 4: Optimización (PENDIENTE)
- [ ] Monitoreo y logging
- [ ] Performance tuning
- [ ] Documentación completa
- [ ] Training del equipo

---

## 📞 Contacto y Soporte

**Usuario**: Eduardo Rodriguez
**Email**: [PENDIENTE]
**Instancia n8n**: https://eduarodriguez.app.n8n.cloud/

---

## 📝 Notas Adicionales

- **Idioma principal**: Español (Panama)
- **Timezone**: America/Panama (UTC-5)
- **Horario de operación**: [PENDIENTE]
- **Prioridad de respuesta**: Consultas de asesoría (24h), Cotizaciones (48h)

---

## 🚀 Primeros Pasos

### Para Claude:
1. Leer este documento completamente
2. Familiarizarse con los modelos de datos en [website/models.py](website/models.py)
3. Revisar las vistas actuales en [website/views.py](website/views.py)
4. Esperar a que el usuario proporcione las credenciales de n8n
5. Comenzar con el workflow de más alta prioridad: Lead Qualification & Nurturing

### Para el Usuario:
1. Proporcionar API key de n8n
2. Confirmar permisos y accesos
3. Revisar y aprobar los primeros workflows antes de activarlos en producción
4. Proporcionar credenciales de servicios externos (email, CRM, etc.) según sea necesario

---

*Última actualización: 2026-01-24*
*Versión: 1.0 - Borrador inicial*
