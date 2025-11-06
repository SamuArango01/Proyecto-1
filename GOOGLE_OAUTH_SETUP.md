# 🔐 Configuración de Inicio de Sesión con Google

## Paso 1: Crear Credenciales en Google Cloud Console

### 1.1 Accede a Google Cloud Console
- Ve a: https://console.cloud.google.com/
- Inicia sesión con tu cuenta de Google

### 1.2 Crear o Seleccionar un Proyecto
1. Haz clic en el menú desplegable del proyecto (parte superior izquierda)
2. Selecciona "Nuevo Proyecto" o elige un proyecto existente
3. Dale un nombre como "Car2Data" y crea el proyecto

### 1.3 Habilitar la API de Google+
1. En el menú lateral, ve a **"APIs y servicios" > "Biblioteca"**
2. Busca **"Google+ API"** o **"Google Identity"**
3. Haz clic en **"Habilitar"**

### 1.4 Crear Credenciales OAuth 2.0
1. Ve a **"APIs y servicios" > "Credenciales"**
2. Haz clic en **"Crear credenciales" > "ID de cliente de OAuth 2.0"**
3. Si es la primera vez, deberás configurar la **"Pantalla de consentimiento de OAuth"**:
   - Tipo: **Externo** (para desarrollo)
   - Nombre de la aplicación: **Car2Data**
   - Correo de soporte: tu email
   - Dominios autorizados: (déjalo vacío por ahora)
   - Información de contacto: tu email
   - Guarda y continúa

4. Vuelve a **"Credenciales" > "Crear credenciales" > "ID de cliente de OAuth 2.0"**
5. Tipo de aplicación: **Aplicación web**
6. Nombre: **Car2Data Web Client**
7. **URIs de redireccionamiento autorizados**:
   ```
   http://localhost:8000/accounts/google/login/callback/
   http://127.0.0.1:8000/accounts/google/login/callback/
   ```
   
   Para producción, agrega también:
   ```
   https://tudominio.com/accounts/google/login/callback/
   ```

8. Haz clic en **"Crear"**
9. **¡IMPORTANTE!** Guarda el **Client ID** y el **Client Secret** que aparecen

## Paso 2: Configurar las Variables de Entorno

### 2.1 Crear/Editar archivo .env
En la raíz del proyecto (`c:\Users\Emman\Car2Data\car2data_project\`), crea o edita el archivo `.env`:

```env
# Credenciales de Google OAuth
GOOGLE_CLIENT_ID=tu_client_id_aqui.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=tu_client_secret_aqui

# APIs existentes
GEMINI_API_KEY=tu_gemini_key
OPENAI_API_KEY=tu_openai_key
```

**Reemplaza** `tu_client_id_aqui` y `tu_client_secret_aqui` con las credenciales que obtuviste en el paso anterior.

## Paso 3: Configurar en Django Admin

### 3.1 Iniciar el servidor
```bash
cd c:\Users\Emman\Car2Data\car2data_project
python manage.py runserver
```

### 3.2 Acceder al Admin de Django
1. Ve a: http://localhost:8000/admin/
2. Inicia sesión con tu cuenta de superusuario
   - Si no tienes un superusuario, créalo con:
     ```bash
     python manage.py createsuperuser
     ```

### 3.3 Configurar Social Application
1. En el admin, busca la sección **"SITES"**
2. Haz clic en **"Sites"** y verifica que exista un sitio con:
   - Domain name: `localhost:8000` (para desarrollo)
   - Display name: `Car2Data`
   
3. Busca la sección **"SOCIAL ACCOUNTS"**
4. Haz clic en **"Social applications"**
5. Haz clic en **"Add social application"** (botón arriba a la derecha)
6. Llena el formulario:
   - **Provider**: Google
   - **Name**: Google OAuth
   - **Client id**: Pega tu GOOGLE_CLIENT_ID
   - **Secret key**: Pega tu GOOGLE_CLIENT_SECRET
   - **Key**: (déjalo vacío)
   - **Sites**: Selecciona tu sitio (`localhost:8000` o `example.com`) y muévelo a "Chosen sites"
7. Haz clic en **"Save"**

## Paso 4: Probar la Integración

### 4.1 Probar Login
1. Ve a: http://localhost:8000/login/
2. Haz clic en **"Iniciar sesión con Google"**
3. Deberías ser redirigido a la página de autorización de Google
4. Selecciona tu cuenta de Google
5. Autoriza la aplicación
6. Deberías ser redirigido de vuelta a tu dashboard

### 4.2 Probar Registro
1. Ve a: http://localhost:8000/register/
2. Haz clic en **"Registrarse con Google"**
3. Sigue el mismo flujo de autorización
4. Se creará automáticamente una cuenta nueva

## Paso 5: Verificar que Funciona

### 5.1 En el Admin
1. Ve a: http://localhost:8000/admin/auth/user/
2. Deberías ver el nuevo usuario creado con tu cuenta de Google
3. Ve a: http://localhost:8000/admin/socialaccount/socialaccount/
4. Deberías ver la conexión de Google asociada al usuario

## Troubleshooting

### Error: "redirect_uri_mismatch"
**Solución**: Verifica que las URIs de redireccionamiento en Google Cloud Console coincidan exactamente con:
```
http://localhost:8000/accounts/google/login/callback/
```

### Error: "Site matching query does not exist"
**Solución**: 
1. Ve al admin de Django
2. Sites > Sites
3. Edita el sitio existente o crea uno nuevo con domain: `localhost:8000`

### Error: "SocialApp matching query does not exist"
**Solución**: 
1. Ve al admin de Django
2. Social applications
3. Crea una nueva aplicación social con tus credenciales de Google

### El botón no hace nada
**Solución**: 
1. Verifica que las variables de entorno estén cargadas correctamente
2. Reinicia el servidor de Django
3. Verifica la consola del navegador para errores de JavaScript

## URLs Importantes

- **Google Cloud Console**: https://console.cloud.google.com/
- **Django Admin**: http://localhost:8000/admin/
- **Login**: http://localhost:8000/login/
- **Register**: http://localhost:8000/register/

## Producción

Para producción, asegúrate de:

1. Cambiar las URIs de redireccionamiento en Google Cloud Console a tu dominio real:
   ```
   https://tudominio.com/accounts/google/login/callback/
   ```

2. Actualizar el Site en Django Admin con tu dominio real

3. Asegurar que las variables de entorno estén configuradas en tu servidor de producción

4. **NUNCA** commitear tu `.env` al repositorio de Git

## Seguridad

- ✅ El `.env` debe estar en `.gitignore`
- ✅ Las credenciales nunca deben estar en el código
- ✅ Usa HTTPS en producción
- ✅ Restringe los dominios autorizados en Google Cloud Console
