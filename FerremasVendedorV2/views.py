from django.shortcuts import render, redirect
from django.conf import settings
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
import requests
import uuid

def products_view(request):
    url = "https://sa-east-1.aws.data.mongodb-api.com/app/data-iutfwvi/endpoint/data/v1/action/find"
    headers = {
        "Content-Type": "application/json",
        "api-key": settings.MONGODB_API_KEY
    }
    payload = {
        "dataSource": "FerremasCluster",
        "database": "ferremasbd",
        "collection": "producto",
        "projection": {"_id": 1, "nombre": 1, "precio": 1, "stock": 1}
    }
    response = requests.post(url, headers=headers, json=payload)
    products = response.json()

    for product in products["documents"]:
        product['id'] = product.pop('_id')  # Replace '_id' with 'id'

    return render(request, "products.html", {"products": products["documents"]})

def comprar_producto(request, product_id):
    # Obtener los datos del producto desde MongoDB u otra fuente
    url = "https://sa-east-1.aws.data.mongodb-api.com/app/data-iutfwvi/endpoint/data/v1/action/findOne"
    headers = {
        "Content-Type": "application/json",
        "api-key": settings.MONGODB_API_KEY
    }
    payload = {
        "dataSource": "FerremasCluster",
        "database": "ferremasbd",
        "collection": "producto",
        "filter": {"_id": {"$oid": product_id}}
    }
    response = requests.post(url, headers=headers, json=payload)
    product = response.json().get("document")

    if product:
        amount = product['precio']
        raw_uuid = uuid.uuid4()
        buy_order = str(raw_uuid)[:26]  # Truncar el UUID a 26 caracteres
        session_id = request.session.session_key or "session_id"
        return_url = request.build_absolute_uri('/pago_exitoso/')  # URL de retorno después del pago

        # Configurar Transbank
        tx = Transaction(WebpayOptions(
            settings.TRANSBANK['COMMERCE_CODE'],
            settings.TRANSBANK['API_KEY_SECRET']
        ))
        response = tx.create(buy_order, session_id, amount, return_url)

        # Redirigir al usuario a la página de pago de Transbank
        return redirect(response['url'] + '?token_ws=' + response['token'])

    # Si no se encuentra el producto, redirigir de vuelta a la lista de productos
    return redirect('products')

def pago_exitoso(request):
    token = request.GET.get('token_ws')
    tx = Transaction(WebpayOptions(
        settings.TRANSBANK['COMMERCE_CODE'],
        settings.TRANSBANK['API_KEY_SECRET']
    ))
    response = tx.commit(token)

    if response['response_code'] == 0:
        # Extract product_id from buy_order
        buy_order = response['buy_order']
        if '_' in buy_order:
            product_id = buy_order.split('_')[1]
        else:
            # Handle unexpected buy_order format
            product_id = None  # or raise an error, log, etc.

        # Update stock in MongoDB after successful purchase
        if product_id:
            url = "https://sa-east-1.aws.data.mongodb-api.com/app/data-iutfwvi/endpoint/data/v1/action/updateOne"
            headers = {
                "Content-Type": "application/json",
                "api-key": settings.MONGODB_API_KEY
            }
            payload = {
                "dataSource": "FerremasCluster",
                "database": "ferremasbd",
                "collection": "producto",
                "filter": {"_id": {"$oid": product_id}},
                "update": {"$inc": {"stock": -1}}
            }
            requests.post(url, headers=headers, json=payload)

        return render(request, 'pago_exitoso.html', {'response': response})
    else:
        return render(request, 'pago_fallido.html', {'response': response})
