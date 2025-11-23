# Mini API JWT con Flask

Aplicacion minima construida con Flask y Flask-JWT-Extended que expone un login con JSON Web Tokens (JWT), un endpoint para obtener el usuario autenticado y otro para listar items protegidos. Incluye un pequeño frontend estatico para probar el flujo completo.

## Requisitos previos

- Python 3.11 o superior.
- `pip` para instalar dependencias.
- (Opcional) `python -m venv` para aislar el entorno.
- Node.js (incluye `npx`) si quieres servir el frontend estatico con `http-server`.

## Instalacion y configuracion

1. Clona el repositorio y ubicate en la carpeta `jwt-app`.
2. Crea un entorno virtual:
   - Windows: `python -m venv .venv` y `.\.venv\Scripts\activate`
   - Linux/macOS: `python3 -m venv .venv` y `source .venv/bin/activate`
3. Instala las dependencias:
   ```bash
   pip install -r requirements.in
   ```
4. (Opcional) Define tu propia clave para firmar los JWT exportando `JWT_SECRET_KEY` o cambiando la constante en `app.py`. Nunca reutilices la clave de ejemplo en produccion.

## Ejecucion

Con el entorno virtual activo ejecuta:

```bash
python app.py
```

Flask levantara el servidor en `http://127.0.0.1:5000`. Para recargar automaticamente durante el desarrollo puedes exportar `FLASK_ENV=development` y usar `flask run`. El CORS esta configurado para permitir `http://127.0.0.1:3000`, `http://localhost:3000` y `http://localhost:8000`.

## Servir el frontend de ejemplo

El proyecto incluye un frontend simple en `example-frontend`. Para levantarlo en el puerto 3000:

1. Asegurate de tener Node.js instalado (viene con `npx`).
2. Entra a la carpeta del frontend: `cd example-frontend`.
3. Ejecuta: `npx http-server . -p 3000`
4. Abre `http://127.0.0.1:3000` en el navegador.

Si prefieres instalar el servidor estatico de forma global, puedes usar `npm install -g http-server` y luego `http-server . -p 3000`.

## Endpoints

| Ruta      | Metodo | Descripcion                                                                                                   |
|-----------|--------|---------------------------------------------------------------------------------------------------------------|
| `/login`  | POST   | Recibe `email` y `password` en JSON. Si son `test@example.com` / `test`, genera y devuelve un JWT de acceso.  |
| `/me`     | GET    | Requiere `Authorization: Bearer <token>`. Devuelve el usuario autenticado.                                    |
| `/items`  | GET    | Igual que `/me`, pero retorna ademas una lista de items de ejemplo.                                           |

### Ejemplo: solicitar un token

```bash
curl -X POST http://127.0.0.1:5000/login ^
     -H "Content-Type: application/json" ^
     -d "{\"email\": \"test@example.com\", \"password\": \"test\"}"
```

Respuesta esperada:

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Ejemplo: consumir los endpoints protegidos

```bash
curl http://127.0.0.1:5000/me ^
     -H "Authorization: Bearer <access_token>"
```

Respuesta:

```json
{
  "logged_in_as": "test@example.com"
}
```

```bash
curl http://127.0.0.1:5000/items ^
     -H "Authorization: Bearer <access_token>"
```

Respuesta (resumida):

```json
{
  "logged_in_as": "test@example.com",
  "items": [
    { "title": "Item1", "description": "Description1", "price": 10.0 },
    { "title": "Item2", "description": "Description2", "price": 20.0 }
  ]
}
```

## Estructura del proyecto

- `app.py`: aplicacion Flask con configuracion CORS, endpoints de login, usuario y items protegidos por JWT.
- `requirements.in`: dependencias de Python.
- `example-frontend/`: frontend estatico (HTML/JS) para probar login y consumo de la API.

## Buenas practicas y proximos pasos

1. **Gestionar usuarios reales**: sustituir las credenciales codificadas por un almacen persistente (base de datos, servicio externo, etc.).
2. **Proteger la clave secreta**: usar variables de entorno, gestores de secretos y rotar la clave periodicamente.
3. **HTTPS obligatorio**: en entornos productivos habilita TLS para evitar la exposicion del token.
4. **Control de caducidad y refresh tokens**: configura tiempos de expiracion y, si es necesario, un flujo de `refresh_token`.
5. **Tests automatizados**: agrega pruebas unitarias/integracion que validen el flujo de autenticacion.

Con estos pasos tendras una base solida para evolucionar esta API hacia un servicio de autenticacion mas completo y seguro.

