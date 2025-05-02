import jwt
from datetime import datetime, timedelta
import os
from functools import wraps
from flask import request, jsonify, g

def generate_jwt_token(user_id, tipo):
    secret = os.getenv("JWT_SECRET", "defaultsecret")
    exp_minutes = int(os.getenv("JWT_EXP_MINUTES", 30))
    payload = {
        "sub": str(user_id),
        "tipo": tipo,
        "exp": datetime.utcnow() + timedelta(minutes=exp_minutes)
    }

    token = jwt.encode(payload, secret, algorithm="HS256")

    if isinstance(token, bytes):
        token = token.decode('utf-8')
    
    return token



def decode_jwt(token):
    try:
        secret = os.getenv("JWT_SECRET", "defaultsecret")
        return jwt.decode(token, secret, algorithms=["HS256"])
    except jwt.ExpiredSignatureError as e:
        print("ExpiredSignatureError:", e)
    except jwt.InvalidTokenError as e:
        print("InvalidTokenError:", e)
    return None


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            bearer = request.headers['Authorization']
            parts = bearer.split()
            if len(parts) == 2 and parts[0].lower() == 'bearer':
                token = parts[1]
        if not token:
            return jsonify({"OK": False, "DESCRIPCION": "Token de autenticación requerido.", "RESPUESTA": {}}), 401
        decoded = decode_jwt(token)
        if not decoded:
            return jsonify({"OK": False, "DESCRIPCION": "Token inválido o expirado."+parts[1], "RESPUESTA": {}}), 401

        g.user = decoded

        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not hasattr(g, 'user') or g.user.get("tipo") != "admin":
            return jsonify({"OK": False, "DESCRIPCION": "Acceso restringido a administradores.", "RESPUESTA": {}}), 403
        return f(*args, **kwargs)
    return decorated