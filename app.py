from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from pydantic import BaseModel, EmailStr

app = Flask(__name__)
# Allowed origins for the frontend during local development
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
]
CORS(app, resources={r"/*": {"origins": ALLOWED_ORIGINS, "supports_credentials": True}})

# Setup Flasj-JWT-Extended extension
# En JWT la secret key es la clave privada que usa el servidor para firmar cada token mediante HMAC.
# Es importante que esta clave sea segura y se mantenga en secreto para proteger la integridad de los tokens.
# En un entorno de producción, esta clave debería ser compleja y almacenada de forma segura.
# Sirve para garantizar la integridad de los tokens JWT, asegurando que no hayan sido alterados.
# Cualquier servicio que comparta esta clave podrá verificar la autenticidad de los tokens generados.
# mientras la Secret Key permanezca segura y suficientemente aleatoria, los tokens JWT firmados con ella serán confiables.
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this in a real app!

# aunque no utilicemos la variable jwt directamente, es necesaria para inicializar la extensión.
jwt = JWTManager(app)

# HMAC (Hash-based Message Authentication Code) es un mecanismo que combina una función 
# hash criptográfica con una clave secreta para proporcionar integridad y autenticación de mensajes.
# HMAC se utiliza para verificar tanto la integridad de los datos como la autenticidad del mensaje, 
# asegurando que el mensaje no ha sido alterado y que proviene de una fuente legítima que posee la clave secreta compartida.
class Credentials(BaseModel):
    email: EmailStr
    password: str

class Item(BaseModel):
    title: str
    description: str
    price: float


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route('/login', methods=['POST'])
def login():
    print(request.get_json())
    creds = Credentials(**request.get_json(force=True))
    if creds.email != 'test@example.com' or creds.password != 'test':
        return jsonify({"msg": "Bad email or password"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=creds.email)
    return jsonify(access_token=access_token)

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route('/items', methods=['GET'])
@jwt_required()
def list_items():
    # Access the identity of the current user with get_jwt_identity
    items: list[Item] = [
        Item(title="Item1", description="Description1", price=10.0),
        Item(title="Item2", description="Description2", price=20.0),
        Item(title="Item3", description="Description3", price=30.0),
    ]

    current_user = get_jwt_identity()
    # Pydantic models need to be converted to plain dicts before jsonify
    serializable_items = [item.model_dump() if hasattr(item, "model_dump") else item.dict() for item in items]
    return jsonify(logged_in_as=current_user, items=serializable_items)

@app.route('/me', methods=['GET'])
@jwt_required()
def me():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user)

if __name__ == '__main__':
    app.run(debug=True)
