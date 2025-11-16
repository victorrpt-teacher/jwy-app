# Mini API JWT con Flask

Aplicacion minima construida con Flask y Flask-JWT-Extended que expone un flujo de autenticacion con JSON Web Tokens (JWT). Incluye un endpoint de login que genera un token firmado mediante HMAC y un endpoint protegido que solo responde si el token es valido.

## Requisitos previos

- Python 3.11 o superior.
- `pip` para instalar dependencias.
- (Opcional) `python -m venv` para aislar el entorno.

## Instalacion y configuracion

1. Clona el repositorio y ubicate en la carpeta `jwt-app`.
2. Crea un entorno virtual:
   - Windows: `python -m venv .venv` y `.\.venv\Scripts\activate`
   - Linux/macOS: `python3 -m venv .venv` y `source .venv/bin/activate`
3. Instala las dependencias:
   ```bash
   pip install -r requirements.in
   ```
4. (Opcional) Define tu propia clave para firmar los JWT exportando `JWT_SECRET_KEY` o cambiando la constante en `app.py`. Nunca reutilices la clave de ejemplo (`super-secret`) en produccion.

## Ejecucion

Con el entorno virtual activo ejecuta:

```bash
python app.py
```

Flask levantara el servidor en `http://127.0.0.1:5000`. Para recargar automaticamente durante el desarrollo puedes exportar `FLASK_ENV=development` y usar `flask run`.

## Endpoints

| Ruta         | Metodo | Descripcion                                                                                                  |
|--------------|--------|--------------------------------------------------------------------------------------------------------------|
| `/login`     | POST   | Recibe `username` y `password` en JSON. Si ambos son `test`, genera y devuelve un JWT de acceso.             |
| `/protected` | GET    | Requiere el encabezado `Authorization: Bearer <token>`. Responde con el usuario asociado al JWT proporcionado.|

### Ejemplo: solicitar un token

```bash
curl -X POST http://127.0.0.1:5000/login ^
     -H "Content-Type: application/json" ^
     -d "{\"username\": \"test\", \"password\": \"test\"}"
```

Respuesta esperada:

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Ejemplo: consumir el endpoint protegido

```bash
curl http://127.0.0.1:5000/protected ^
     -H "Authorization: Bearer <access_token>"
```

Respuesta:

```json
{
  "logged_in_as": "test"
}
```

## Estructura del proyecto

- `app.py`: aplicacion Flask con la configuracion de JWT, el endpoint de inicio de sesion y el recurso protegido.
- `requirements.in`: dependencias minimas necesarias para ejecutar el proyecto.

## Buenas practicas y proximos pasos

1. **Gestionar usuarios reales**: sustituir las credenciales codificadas por un almacen persistente (base de datos, servicio externo, etc.).
2. **Proteger la clave secreta**: usar variables de entorno, gestores de secretos y rotar la clave periodicamente.
3. **HTTPS obligatorio**: en entornos productivos habilita TLS para evitar la exposicion del token.
4. **Control de caducidad y refresh tokens**: configura tiempos de expiracion y, si es necesario, un flujo de `refresh_token`.
5. **Tests automatizados**: agrega pruebas unitarias/integracion que validen el flujo de autenticacion.

Con estos pasos tendras una base solida para evolucionar esta API hacia un servicio de autenticacion mas completo y seguro.
