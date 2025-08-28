"""
MySQL settings for Car2Data project.
"""

from .base import *
import pymysql

# Configurar PyMySQL como reemplazo de MySQLdb
pymysql.install_as_MySQLdb()

# Database - Configuración para MySQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME', default='car2data'),
        'USER': config('DB_USER', default='root'),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'autocommit': True,
        },
    }
}

# Configuración adicional para tablas existentes
DATABASE_ROUTERS = ['car2data_project.routers.DatabaseRouter']
