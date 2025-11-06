# Guía de Despliegue en AWS Academy con Dominio Personalizado

Esta guía te llevará paso a paso para desplegar tu proyecto Django (Car2Data) en AWS Academy usando EC2, RDS, S3 y configurar un dominio personalizado.

---

## 📋 Requisitos Previos

- [ ] Cuenta de AWS Academy activa
- [ ] Proyecto Django funcionando localmente
- [ ] Git instalado
- [ ] Dominio registrado (ej: GoDaddy, Namecheap, Google Domains)
- [ ] Acceso SSH configurado

---

## 🎯 Arquitectura del Despliegue

```
Internet → Route 53 (DNS) → ALB (Load Balancer) → EC2 (Django + Gunicorn + Nginx)
                                                      ↓
                                                    RDS (PostgreSQL)
                                                      ↓
                                                    S3 (Media Files)
```

---

## 📦 PARTE 1: Preparar el Proyecto para Producción

### 1.1 Actualizar `settings.py`

Crea un archivo `settings_prod.py` o modifica `settings.py`:

```python
import os
from pathlib import Path

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'tu-secret-key-temporal')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'tu-dominio.com',
    'www.tu-dominio.com',
    'tu-ip-elastica-de-aws',
    'tu-instancia-ec2.compute.amazonaws.com'
]

# Database - PostgreSQL en RDS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'car2data_db'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'tu-rds-endpoint.rds.amazonaws.com'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files (User uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# AWS S3 Configuration (opcional para archivos estáticos)
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = 'us-east-1'  # Cambia según tu región

# Security Settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

### 1.2 Actualizar `requirements.txt`

```bash
cd c:\Users\Emman\Car2Data
pip freeze > requirements.txt
```

Asegúrate de incluir:
```txt
Django==4.2.7
gunicorn==21.2.0
psycopg2-binary==2.9.9
boto3==1.29.7
django-storages==1.14.2
python-decouple==3.8
whitenoise==6.6.0
```

### 1.3 Crear archivo `.env.example`

```bash
# .env.example
DJANGO_SECRET_KEY=tu-secret-key-aqui
DEBUG=False
DB_NAME=car2data_db
DB_USER=postgres
DB_PASSWORD=tu-password-seguro
DB_HOST=tu-rds-endpoint.rds.amazonaws.com
DB_PORT=5432
AWS_ACCESS_KEY_ID=tu-access-key
AWS_SECRET_ACCESS_KEY=tu-secret-key
AWS_STORAGE_BUCKET_NAME=car2data-media
```

---

## 🚀 PARTE 2: Configurar AWS Academy

### 2.1 Crear Instancia EC2

1. **Inicia sesión en AWS Academy**
   - Ve a tu curso → AWS Academy Learner Lab
   - Click en "Start Lab" (espera a que el círculo se ponga verde)
   - Click en "AWS" para abrir la consola

2. **Lanzar Instancia EC2**
   ```
   Servicios → EC2 → Launch Instance
   ```

3. **Configuración de la Instancia**
   - **Name**: `car2data-production`
   - **AMI**: Ubuntu Server 22.04 LTS (Free tier eligible)
   - **Instance type**: `t2.medium` (recomendado) o `t2.small` (mínimo)
   - **Key pair**: Crea un nuevo par de llaves → `car2data-key.pem` → Descárgalo
   - **Network settings**:
     - VPC: Default
     - Auto-assign public IP: Enable
     - Security Group: Crear nuevo
       - **SSH (22)**: Tu IP
       - **HTTP (80)**: 0.0.0.0/0
       - **HTTPS (443)**: 0.0.0.0/0
       - **Custom TCP (8000)**: 0.0.0.0/0 (temporal para testing)
   - **Storage**: 20 GB gp3

4. **Launch Instance** → Espera a que esté "Running"

5. **Asignar IP Elástica**
   ```
   EC2 → Elastic IPs → Allocate Elastic IP address
   → Associate Elastic IP address → Selecciona tu instancia
   ```

### 2.2 Crear Base de Datos RDS (PostgreSQL)

1. **Ir a RDS**
   ```
   Servicios → RDS → Create database
   ```

2. **Configuración**
   - **Engine**: PostgreSQL 15.x
   - **Templates**: Free tier
   - **DB instance identifier**: `car2data-db`
   - **Master username**: `postgres`
   - **Master password**: Crea una contraseña segura (guárdala)
   - **DB instance class**: db.t3.micro
   - **Storage**: 20 GB gp3
   - **Connectivity**:
     - VPC: Default
     - Public access: Yes (para desarrollo; No en producción real)
     - VPC security group: Crear nuevo → `car2data-db-sg`
   - **Additional configuration**:
     - Initial database name: `car2data_db`

3. **Modificar Security Group de RDS**
   ```
   EC2 → Security Groups → car2data-db-sg → Inbound rules → Edit
   → Add rule: PostgreSQL (5432) → Source: Security Group de EC2
   ```

### 2.3 Crear Bucket S3 para Media Files

1. **Ir a S3**
   ```
   Servicios → S3 → Create bucket
   ```

2. **Configuración**
   - **Bucket name**: `car2data-media-files` (debe ser único globalmente)
   - **Region**: us-east-1 (o la misma de tu EC2)
   - **Block Public Access**: Desmarcar (solo si necesitas acceso público)
   - **Bucket Versioning**: Enable (recomendado)

3. **Configurar CORS**
   ```
   Bucket → Permissions → CORS → Edit
   ```
   ```json
   [
       {
           "AllowedHeaders": ["*"],
           "AllowedMethods": ["GET", "POST", "PUT", "DELETE"],
           "AllowedOrigins": ["https://tu-dominio.com"],
           "ExposeHeaders": []
       }
   ]
   ```

4. **Crear IAM User para S3**
   ```
   IAM → Users → Add user
   → User name: car2data-s3-user
   → Attach policies: AmazonS3FullAccess
   → Create user → Security credentials → Create access key
   → Guarda Access Key ID y Secret Access Key
   ```

---

## 🔧 PARTE 3: Configurar el Servidor EC2

### 3.1 Conectar por SSH

**Windows (PowerShell):**
```powershell
# Mover la llave a una ubicación segura
Move-Item .\car2data-key.pem ~\.ssh\

# Cambiar permisos (solo lectura para ti)
icacls ~\.ssh\car2data-key.pem /inheritance:r
icacls ~\.ssh\car2data-key.pem /grant:r "$($env:USERNAME):(R)"

# Conectar
ssh -i ~\.ssh\car2data-key.pem ubuntu@TU-IP-ELASTICA
```

**Linux/Mac:**
```bash
chmod 400 car2data-key.pem
ssh -i car2data-key.pem ubuntu@TU-IP-ELASTICA
```

### 3.2 Instalar Dependencias en EC2

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python y herramientas
sudo apt install -y python3.11 python3.11-venv python3-pip
sudo apt install -y postgresql-client libpq-dev
sudo apt install -y nginx git curl

# Instalar Node.js (si usas npm para frontend)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
```

### 3.3 Clonar y Configurar el Proyecto

```bash
# Crear directorio para la aplicación
sudo mkdir -p /var/www/car2data
sudo chown -R ubuntu:ubuntu /var/www/car2data
cd /var/www/car2data

# Clonar repositorio
git clone https://github.com/SamuArango01/Proyecto-1.git .

# Crear entorno virtual
python3.11 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# Crear archivo .env
nano .env
```

**Contenido de `.env`:**
```bash
DJANGO_SECRET_KEY=genera-una-nueva-secret-key-aqui
DEBUG=False
DB_NAME=car2data_db
DB_USER=postgres
DB_PASSWORD=tu-password-de-rds
DB_HOST=tu-rds-endpoint.rds.amazonaws.com
DB_PORT=5432
AWS_ACCESS_KEY_ID=tu-access-key-de-iam
AWS_SECRET_ACCESS_KEY=tu-secret-key-de-iam
AWS_STORAGE_BUCKET_NAME=car2data-media-files
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com,tu-ip-elastica
```

**Guardar:** `Ctrl+O` → Enter → `Ctrl+X`

### 3.4 Configurar Django

```bash
# Activar entorno virtual
cd /var/www/car2data
source venv/bin/activate

# Migraciones
python manage.py makemigrations
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Recolectar archivos estáticos
python manage.py collectstatic --noinput

# Probar servidor (temporal)
python manage.py runserver 0.0.0.0:8000
```

Abre `http://TU-IP-ELASTICA:8000` en tu navegador para verificar.

---

## 🌐 PARTE 4: Configurar Gunicorn y Nginx

### 4.1 Crear Servicio Systemd para Gunicorn

```bash
sudo nano /etc/systemd/system/gunicorn.service
```

**Contenido:**
```ini
[Unit]
Description=Gunicorn daemon for Car2Data Django app
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/var/www/car2data/car2data_project
Environment="PATH=/var/www/car2data/venv/bin"
EnvironmentFile=/var/www/car2data/.env
ExecStart=/var/www/car2data/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/var/www/car2data/gunicorn.sock \
          car2data_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

**Iniciar Gunicorn:**
```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn
```

### 4.2 Configurar Nginx

```bash
sudo nano /etc/nginx/sites-available/car2data
```

**Contenido:**
```nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;

    client_max_body_size 100M;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /var/www/car2data/car2data_project/staticfiles/;
    }

    location /media/ {
        alias /var/www/car2data/car2data_project/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/car2data/gunicorn.sock;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }
}
```

**Activar configuración:**
```bash
sudo ln -s /etc/nginx/sites-available/car2data /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🔐 PARTE 5: Configurar HTTPS con Let's Encrypt

### 5.1 Instalar Certbot

```bash
sudo apt install -y certbot python3-certbot-nginx
```

### 5.2 Obtener Certificado SSL

```bash
sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com
```

Sigue las instrucciones:
- Email: tu-email@ejemplo.com
- Acepta términos: Y
- Compartir email: N (opcional)
- Redirect HTTP → HTTPS: 2 (recomendado)

### 5.3 Renovación Automática

```bash
sudo certbot renew --dry-run
```

El certificado se renovará automáticamente cada 90 días.

---

## 🌍 PARTE 6: Configurar Dominio

### 6.1 Configurar DNS en tu Proveedor de Dominio

Ve a tu proveedor de dominio (GoDaddy, Namecheap, etc.) y configura:

**Registros DNS:**
```
Tipo    Nombre    Valor                          TTL
A       @         TU-IP-ELASTICA-DE-AWS          600
A       www       TU-IP-ELASTICA-DE-AWS          600
CNAME   www       tu-dominio.com                 3600
```

**Ejemplo con GoDaddy:**
1. My Products → Domains → DNS
2. Add Record → Type: A → Name: @ → Value: TU-IP-ELASTICA → TTL: 600
3. Add Record → Type: A → Name: www → Value: TU-IP-ELASTICA → TTL: 600

**Espera 5-30 minutos para propagación DNS.**

### 6.2 Verificar DNS

```bash
# En tu computadora local
nslookup tu-dominio.com
ping tu-dominio.com
```

---

## 🔄 PARTE 7: Despliegue y Actualizaciones

### 7.1 Script de Despliegue

Crea un script para automatizar actualizaciones:

```bash
nano /var/www/car2data/deploy.sh
```

**Contenido:**
```bash
#!/bin/bash

echo "🚀 Iniciando despliegue..."

# Ir al directorio del proyecto
cd /var/www/car2data

# Activar entorno virtual
source venv/bin/activate

# Pull últimos cambios
git pull origin main

# Instalar/actualizar dependencias
pip install -r requirements.txt

# Migraciones
python car2data_project/manage.py migrate

# Recolectar estáticos
python car2data_project/manage.py collectstatic --noinput

# Reiniciar Gunicorn
sudo systemctl restart gunicorn

# Reiniciar Nginx
sudo systemctl restart nginx

echo "✅ Despliegue completado!"
```

**Hacer ejecutable:**
```bash
chmod +x /var/www/car2data/deploy.sh
```

### 7.2 Desplegar Cambios

```bash
# Desde tu computadora local
git add -A
git commit -m "Nueva funcionalidad"
git push origin main

# En el servidor EC2
cd /var/www/car2data
./deploy.sh
```

---

## 📊 PARTE 8: Monitoreo y Logs

### 8.1 Ver Logs

```bash
# Logs de Gunicorn
sudo journalctl -u gunicorn -f

# Logs de Nginx
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# Logs de Django
tail -f /var/www/car2data/car2data_project/logs/django.log
```

### 8.2 Comandos Útiles

```bash
# Reiniciar servicios
sudo systemctl restart gunicorn
sudo systemctl restart nginx

# Ver estado
sudo systemctl status gunicorn
sudo systemctl status nginx

# Verificar configuración de Nginx
sudo nginx -t

# Recargar Nginx sin downtime
sudo systemctl reload nginx
```

---

## 🛡️ PARTE 9: Seguridad Adicional

### 9.1 Configurar Firewall (UFW)

```bash
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
sudo ufw status
```

### 9.2 Fail2Ban (Protección contra ataques)

```bash
sudo apt install -y fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 9.3 Backups Automáticos

```bash
# Crear script de backup
sudo nano /usr/local/bin/backup-car2data.sh
```

**Contenido:**
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/car2data"
mkdir -p $BACKUP_DIR

# Backup de base de datos
PGPASSWORD=$DB_PASSWORD pg_dump -h $DB_HOST -U $DB_USER $DB_NAME > $BACKUP_DIR/db_$DATE.sql

# Backup de archivos media
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /var/www/car2data/car2data_project/media

# Subir a S3 (opcional)
aws s3 cp $BACKUP_DIR/db_$DATE.sql s3://car2data-backups/
aws s3 cp $BACKUP_DIR/media_$DATE.tar.gz s3://car2data-backups/

# Limpiar backups antiguos (más de 7 días)
find $BACKUP_DIR -type f -mtime +7 -delete
```

**Automatizar con Cron:**
```bash
sudo chmod +x /usr/local/bin/backup-car2data.sh
sudo crontab -e
```

Agregar:
```
0 2 * * * /usr/local/bin/backup-car2data.sh
```

---

## ✅ Checklist Final

- [ ] EC2 instancia corriendo con IP elástica
- [ ] RDS PostgreSQL configurado y conectado
- [ ] S3 bucket creado para media files
- [ ] Proyecto clonado y configurado en EC2
- [ ] Gunicorn corriendo como servicio
- [ ] Nginx configurado y corriendo
- [ ] SSL/HTTPS configurado con Let's Encrypt
- [ ] DNS apuntando a IP elástica
- [ ] Dominio accesible vía HTTPS
- [ ] Backups automáticos configurados
- [ ] Firewall y seguridad configurados

---

## 🆘 Troubleshooting

### Problema: "502 Bad Gateway"
```bash
# Verificar Gunicorn
sudo systemctl status gunicorn
sudo journalctl -u gunicorn -n 50

# Verificar socket
ls -la /var/www/car2data/gunicorn.sock

# Reiniciar
sudo systemctl restart gunicorn
```

### Problema: "Static files no cargan"
```bash
cd /var/www/car2data
source venv/bin/activate
python manage.py collectstatic --noinput
sudo systemctl restart nginx
```

### Problema: "No se puede conectar a RDS"
```bash
# Verificar security group de RDS
# Debe permitir tráfico desde security group de EC2 en puerto 5432

# Probar conexión
psql -h tu-rds-endpoint.rds.amazonaws.com -U postgres -d car2data_db
```

### Problema: "Domain no resuelve"
```bash
# Verificar DNS
nslookup tu-dominio.com

# Esperar propagación (hasta 48 horas, usualmente 5-30 min)
# Verificar en: https://dnschecker.org
```

---

## 📚 Recursos Adicionales

- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)

---

## 🎉 ¡Felicidades!

Tu aplicación Car2Data ahora está desplegada en AWS Academy con:
- ✅ Dominio personalizado
- ✅ HTTPS/SSL
- ✅ Base de datos PostgreSQL en RDS
- ✅ Archivos media en S3
- ✅ Servidor de producción con Gunicorn + Nginx
- ✅ Backups automáticos
- ✅ Seguridad configurada

**URL de acceso:** `https://tu-dominio.com`
**Panel admin:** `https://tu-dominio.com/admin`

---

**Última actualización:** Noviembre 2025
**Autor:** Car2Data Team
**Versión:** 1.0
