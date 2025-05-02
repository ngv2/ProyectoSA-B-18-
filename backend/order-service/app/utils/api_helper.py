import requests
import os

def actualizar_total_compra_usuario(id_usuario, data, token):
    url = f"{os.getenv('RUTA_USERS')}/users/{id_usuario}/total_compra"
    headers = {"Authorization": token}
    return requests.patch(url, json=data, headers=headers).json()

def inactivar_descuento_usuario(id_usuario, token):
    url = f"{os.getenv('RUTA_USERS')}/users/{id_usuario}/descuento"
    headers = {"Authorization": token}
    return requests.patch(url, headers=headers).json()

def verificar_descuento_usuario(id_usuario, token):
    url = f"{os.getenv('RUTA_USERS')}/users/{id_usuario}/descuento"
    headers = {"Authorization": token}
    return requests.get(url, headers=headers).json()

def actualizar_ventas_producto(id_producto, cantidad, token):
    url = f"{os.getenv('RUTA_PRODUCTS')}/products/ventas/{id_producto}"
    headers = {"Authorization": token}
    return requests.put(url, json={"cantidad_vendida": cantidad}, headers=headers).json()
