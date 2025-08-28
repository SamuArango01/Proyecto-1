class DatabaseRouter:
    """
    Router para manejar las tablas existentes de MySQL
    """
    
    def db_for_read(self, model, **hints):
        """Leer desde la base de datos por defecto"""
        return 'default'

    def db_for_write(self, model, **hints):
        """Escribir en la base de datos por defecto"""
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """Permitir relaciones entre objetos"""
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Permitir migraciones en la base de datos por defecto"""
        return db == 'default'