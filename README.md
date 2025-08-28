# Car2Data

Sistema de gestión de datos de vehículos y generación de documentos.

## Descripción

Car2Data es una aplicación web desarrollada en Django que permite gestionar información de vehículos, documentos relacionados y generar formularios automáticamente.

## Características

- **Gestión de Vehículos**: Registro y administración de información de vehículos
- **Gestión de Documentos**: Almacenamiento y organización de documentos PDF
- **Generación de Formularios**: Creación automática de formularios basados en plantillas
- **Sistema de Autenticación**: Control de acceso y gestión de usuarios
- **Panel de Administración**: Interfaz administrativa completa

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
│   │   ├── documents/             # Gestión de documentos
│   │   ├── vehicles/              # Gestión de vehículos
│   │   ├── forms_generation/      # Generación de formularios
│   │   └── administration/        # Panel administrativo
│   ├── static/                    # Archivos estáticos
│   ├── templates/                 # Plantillas HTML
│   ├── media/                     # Archivos multimedia
│   ├── requirements/              # Dependencias del proyecto
│   └── manage.py                  # Script de gestión Django
├── docs/                          # Documentación
├── tests/                         # Pruebas unitarias
├── scripts/                       # Scripts de utilidad
└── README.md                      # Este archivo
```

## Instalación

### Prerrequisitos

- Python 3.8 o superior
- pip
- Git

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
   cp env.example .env
   # Editar .env con tus configuraciones
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

1. Accede a `http://localhost:8000` en tu navegador
2. Inicia sesión con las credenciales del superusuario
3. Navega por las diferentes secciones del sistema

## Configuración

### Variables de Entorno

Copia el archivo `env.example` a `.env` y configura las siguientes variables:

- `SECRET_KEY`: Clave secreta de Django
- `DEBUG`: Modo debug (True/False)
- `ALLOWED_HOSTS`: Hosts permitidos
- `DB_*`: Configuración de base de datos
- `EMAIL_*`: Configuración de email

### Entornos

- **Desarrollo**: `python manage.py runserver --settings=car2data_project.settings.development`
- **Producción**: `python manage.py runserver --settings=car2data_project.settings.production`

## Desarrollo

### Estructura de Aplicaciones

Cada aplicación Django sigue la estructura estándar:

```
app_name/
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── views.py
├── urls.py
├── forms.py
├── tests/
└── templates/
    └── app_name/
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

# Recolectar archivos estáticos
python manage.py collectstatic
```

## Pruebas

```bash
# Ejecutar todas las pruebas
python manage.py test

# Ejecutar pruebas de una aplicación específica
python manage.py test apps.vehicles

# Ejecutar con cobertura
coverage run --source='.' manage.py test
coverage report
```

## Despliegue

### Producción

1. Configurar variables de entorno para producción
2. Instalar dependencias de producción: `pip install -r requirements/production.txt`
3. Configurar servidor web (nginx, Apache)
4. Configurar servidor WSGI (gunicorn, uwsgi)
5. Configurar base de datos PostgreSQL

### Docker (Opcional)

```bash
# Construir imagen
docker build -t car2data .

# Ejecutar contenedor
docker run -p 8000:8000 car2data
```

## Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Contacto

- **Desarrollador**: [Tu Nombre]
- **Email**: [tu-email@ejemplo.com]
- **Proyecto**: [https://github.com/usuario/car2data](https://github.com/usuario/car2data)

## Changelog

### v1.0.0
- Versión inicial del proyecto
- Sistema de autenticación básico
- Gestión de vehículos
- Gestión de documentos
- Generación de formularios
