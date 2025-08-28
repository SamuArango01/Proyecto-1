from django.db import models

class Vehiculo(models.Model):
    id_vehiculo = models.AutoField(primary_key=True)
    placa = models.CharField(max_length=10, unique=True)
    marca = models.CharField(max_length=50, blank=True)
    linea = models.CharField(max_length=50, blank=True)
    modelo = models.IntegerField(null=True, blank=True)
    color = models.CharField(max_length=30, blank=True)
    numero_motor = models.CharField(max_length=50, blank=True)
    numero_chasis = models.CharField(max_length=50, blank=True)
    numero_vin = models.CharField(max_length=50, blank=True)
    numero_serie = models.CharField(max_length=50, blank=True)
    cilindraje = models.IntegerField(null=True, blank=True)
    clase_vehiculo = models.CharField(max_length=50, blank=True)
    carroceria = models.CharField(max_length=50, blank=True)
    tipo_combustible = models.CharField(max_length=30, blank=True)
    potencia_hp = models.IntegerField(null=True, blank=True)
    capacidad = models.CharField(max_length=30, blank=True)
    ciudad_matricula = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'vehiculo'
        verbose_name = 'Vehículo'
        verbose_name_plural = 'Vehículos'

    def __str__(self):
        return f"{self.placa} - {self.marca} {self.linea}"

class Persona(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('CE', 'Cédula de Extranjería'),
        ('NIT', 'NIT'),
        ('PAS', 'Pasaporte'),
    ]
    
    id_persona = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    tipo_documento = models.CharField(max_length=10, choices=TIPO_DOCUMENTO_CHOICES, blank=True)
    numero_documento = models.CharField(max_length=20, unique=True)
    direccion = models.CharField(max_length=100, blank=True)
    ciudad = models.CharField(max_length=50, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'persona'
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'

    def __str__(self):
        return f"{self.nombre} - {self.numero_documento}"