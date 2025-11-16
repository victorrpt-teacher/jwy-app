from flask import Flask, jsonify, request

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

app = Flask(__name__)

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


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username != 'test' or password != 'test':
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == '__main__':
    app.run()