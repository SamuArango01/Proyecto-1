# Car2Data

Sistema de gestión de datos de vehículos y generación de documentos con IA.

## Descripción

Car2Data es una aplicación web desarrollada en Django que permite gestionar información de vehículos, documentos relacionados y generar formularios automáticamente. Utiliza inteligencia artificial (Gemini AI) para extraer información automáticamente de tarjetas de propiedad de vehículos.

## Características

- **Gestión de Vehículos**: Registro y administración de información de vehículos
- **Gestión de Documentos**: Almacenamiento y organización de documentos PDF
- **Extracción Automática con IA**: Procesamiento automático de tarjetas de propiedad usando Gemini AI
- **Generación de Formularios**: Creación automática de formularios basados en plantillas
- **Sistema de Autenticación**: Control de acceso y gestión de usuarios con autenticación social
- **Panel de Administración**: Interfaz administrativa completa
- **Tema Personalizado**: Diseño con temática de placa vehicular negra y amarilla
- **Animaciones Modernas**: Efectos GSAP para una experiencia de usuario superior

## Tecnologías Utilizadas

- **Backend**: Django 4.2.7 (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Base de Datos**: SQLite (desarrollo), PostgreSQL (producción)
- **IA**: Google Gemini AI para procesamiento de documentos
- **Autenticación**: Django AllAuth con soporte para Google OAuth
- **Animaciones**: GSAP (GreenSock Animation Platform)
- **Estilos**: Tailwind CSS
- **Dependencias**: Pillow, Faker, y más

## Estructura del Proyecto

```
car2data/
├── venv/                          # Entorno virtual
├── car2data_project/              # Proyecto Django principal
│   ├── car2data_project/          # Configuración del proyecto
│   │   ├── settings/              # Configuraciones por entorno
│   │   ├── urls.py                # URLs principales
│   │   └── wsgi.py                # Configuración WSGI
│   ├── apps/                      # Aplicaciones Django
│   │   ├── authentication/        # Autenticación de usuarios
│   │   ├── documents/             # Gestión de documentos y extracción IA
│   │   ├── vehicles/              # Gestión de vehículos
│   │   ├── forms_generation/      # Generación de formularios
│   │   └── administration/        # Panel administrativo
│   ├── static/                    # Archivos estáticos (CSS, JS, imágenes)
│   ├── templates/                 # Plantillas HTML
│   ├── media/                     # Archivos multimedia subidos por usuarios
│   ├── services/                  # Servicios externos (IA, APIs)
│   ├── requirements/              # Archivos de dependencias
│   └── manage.py                  # Script de gestión Django
├── docs/                          # Documentación adicional
├── tests/                         # Pruebas unitarias
├── scripts/                       # Scripts de utilidad
└── README.md                      # Este archivo
```

## Instalación

### Prerrequisitos

- Python 3.8 o superior
- pip
- Git
- Una cuenta de Google para obtener API key de Gemini AI

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd car2data
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   ```

3. **Activar entorno virtual**
   ```bash
   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

4. **Instalar dependencias**
   ```bash
   cd car2data_project
   pip install -r requirements/development.txt
   ```

5. **Configurar variables de entorno**
   ```bash
   cd car2data_project
   cp env.example .env
   # Editar .env con tus configuraciones
   ```

   **Variables importantes en `.env`:**
   ```env
   # Django
   SECRET_KEY=your-secret-key-here
   DEBUG=True

   # IA Services (OBLIGATORIO)
   GEMINI_API_KEY=tu-api-key-de-gemini-aqui

   # Base de datos
   DB_NAME=car2data
   DB_USER=car2data_admin
   DB_PASSWORD=tu-password

   # Email (opcional)
   EMAIL_HOST=smtp.gmail.com
   EMAIL_HOST_USER=tu-email@gmail.com
   EMAIL_HOST_PASSWORD=tu-password-de-app
   ```

6. **Ejecutar migraciones**
   ```bash
   python manage.py migrate
   ```

7. **Crear superusuario**
   ```bash
   python manage.py createsuperuser
   ```

8. **Ejecutar el servidor de desarrollo**
   ```bash
   python manage.py runserver
   ```

## Uso

1. **Accede a la aplicación**:
   - Abre tu navegador y ve a: `http://localhost:8000`
   - Inicia sesión con las credenciales del superusuario

2. **Funcionalidades principales**:
   - **Dashboard**: Vista general del sistema
   - **Subir documentos**: Carga tarjetas de propiedad para extracción automática
   - **Vista previa**: Revisa la información extraída por IA
   - **Generar formularios**: Crea documentos basados en plantillas
   - **Administración**: Gestiona usuarios, vehículos y documentos

3. **Extracción con IA**:
   - Sube un PDF de tarjeta de propiedad
   - El sistema usa Gemini AI para extraer información automáticamente
   - Revisa y confirma los datos extraídos
   - Genera formularios con la información procesada

## Configuración

### Variables de Entorno

Copia el archivo `env.example` a `.env` y configura las siguientes variables:

#### Obligatorias:
- `GEMINI_API_KEY`: Tu API key de Google Gemini AI (obtén una en https://aistudio.google.com/app/apikey)

#### Django:
- `SECRET_KEY`: Clave secreta de Django (genera una segura)
- `DEBUG`: `True` para desarrollo, `False` para producción
- `ALLOWED_HOSTS`: Lista de hosts permitidos

#### Base de Datos:
- `DB_NAME`: Nombre de la base de datos
- `DB_USER`: Usuario de la base de datos
- `DB_PASSWORD`: Contraseña de la base de datos
- `DB_HOST`: Host de la base de datos (por defecto: localhost)
- `DB_PORT`: Puerto de la base de datos (por defecto: 3306 para MySQL, 5432 para PostgreSQL)

#### Email (opcional):
- `EMAIL_HOST`: Servidor SMTP
- `EMAIL_PORT`: Puerto SMTP
- `EMAIL_HOST_USER`: Tu email
- `EMAIL_HOST_PASSWORD`: Contraseña de aplicación
- `EMAIL_USE_TLS`: Usar TLS (True/False)

### Configuración de Producción

Para entorno de producción:

1. Configura `DEBUG=False` en `.env`
2. Instala dependencias de producción: `pip install -r requirements/production.txt`
3. Configura una base de datos PostgreSQL
4. Usa un servidor WSGI como Gunicorn
5. Configura un servidor web como Nginx

## Desarrollo

### Estructura de Aplicaciones

Cada aplicación Django sigue la estructura estándar:

```
app_name/
├── __init__.py
├── admin.py          # Configuración del admin de Django
├── apps.py           # Configuración de la aplicación
├── models.py         # Modelos de datos
├── views.py          # Vistas y lógica de negocio
├── urls.py           # Rutas URL
├── forms.py          # Formularios
├── tests/            # Pruebas unitarias
└── templates/        # Plantillas HTML
    └── app_name/     # Templates específicos de la app
```

### Comandos Útiles

```bash
# Crear una nueva aplicación
python manage.py startapp app_name

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Ejecutar pruebas
python manage.py test

# Ejecutar pruebas específicas
python manage.py test apps.documents

# Recolectar archivos estáticos
python manage.py collectstatic

# Crear superusuario
python manage.py createsuperuser

# Ver SQL de migraciones
python manage.py sqlmigrate app_name migration_name
```

### Desarrollo con IA

El servicio de extracción de documentos utiliza:

- **Google Gemini AI** para análisis de PDFs
- **Procesamiento automático** de tarjetas de propiedad
- **Extracción estructurada** de datos vehiculares
- **Validación automática** de información

## Pruebas

```bash
# Ejecutar todas las pruebas
python manage.py test

# Ejecutar pruebas de una aplicación específica
python manage.py test apps.documents

# Ejecutar pruebas con cobertura
pip install coverage
coverage run --source='.' manage.py test
coverage report

# Ver líneas no cubiertas
coverage html
```

## Despliegue

### Producción con Docker (Recomendado)

```bash
# Construir imagen
docker build -t car2data .

# Ejecutar contenedor
docker run -p 8000:8000 car2data

# Con variables de entorno
docker run -p 8000:8000 \
  -e GEMINI_API_KEY=tu-api-key \
  -e SECRET_KEY=tu-secret-key \
  car2data
```

### Producción Manual

1. **Configurar entorno**:
   ```bash
   export DJANGO_SETTINGS_MODULE=car2data_project.settings.production
   ```

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements/production.txt
   ```

3. **Recolectar archivos estáticos**:
   ```bash
   python manage.py collectstatic --noinput
   ```

4. **Configurar servidor WSGI**:
   ```bash
   pip install gunicorn
   gunicorn --bind 0.0.0.0:8000 car2data_project.wsgi:application
   ```

5. **Configurar servidor web** (ejemplo con Nginx):
   ```nginx
   server {
       listen 80;
       server_name tudominio.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }

       location /static/ {
           alias /path/to/staticfiles/;
       }

       location /media/ {
           alias /path/to/media/;
       }
   }
   ```

## Características Avanzadas

### Procesamiento con IA

- **Extracción automática** de información de tarjetas de propiedad
- **Análisis inteligente** usando Google Gemini AI
- **Procesamiento en segundo plano** para mejor experiencia de usuario
- **Validación automática** de datos extraídos

### Autenticación Social

- **Inicio de sesión** con Google OAuth
- **Gestión de usuarios** avanzada
- **Permisos granulares** por aplicación

### Tema y Animaciones

- **Tema personalizado** con colores negro y amarillo (estilo placa vehicular)
- **Animaciones GSAP** para transiciones suaves
- **Efectos hover** y partículas
- **Responsive design** para móviles y tablets

## Solución de Problemas

### Problemas comunes:

1. **Error de cuota de Gemini AI**:
   - Obtén una nueva API key en Google AI Studio
   - Verifica que tengas cuota disponible

2. **Error de modelos de Gemini**:
   - Usa modelos como `gemini-2.0-flash-exp` o `gemini-1.5-pro`
   - Actualiza la librería: `pip install --upgrade google-generativeai`

3. **Error de permisos en archivos**:
   - Verifica permisos en carpetas `media/` y `static/`
   - Asegura que el usuario tenga permisos de escritura

4. **Error de migraciones**:
   ```bash
   python manage.py migrate --fake-initial
   ```

## Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Soporte

Para soporte técnico o consultas:
- **Email**: soporte@car2data.com
- **Documentación**: /docs/
- **Issues**: Reporta problemas en el repositorio

## Changelog

### v2.0.0 (Actual)
- ✅ Integración completa con Google Gemini AI
- ✅ Extracción automática de datos vehiculares
- ✅ Animaciones GSAP avanzadas
- ✅ Procesamiento en segundo plano
- ✅ Interfaz moderna y responsive

### v1.0.0
- Sistema de autenticación básico
- Gestión básica de vehículos
- Gestión básica de documentos
- Generación básica de formularios

---

**Desarrollado con ❤️ usando Django, Gemini AI y tecnologías modernas**
