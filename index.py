from binance.client import Client
import time

api_key = '7YrTTOWV9VZXLQJiVtPa5ZuadMAhfZfJBb8s6zaNkYxnQGl2FFlujswoqbhbgUjY'
api_secret = 'yjla2ZLQK5aJNbTrAPh6UDiFOQktdYnGPtKTTiedStfpMgkMA6pE2QkvAVMLubUk'

client = Client(api_key, api_secret, tld='us')

symbol = 'BTCUSDT'
diferencia_compra = 5000  # diferencia de 5 mil USD para comprar
porcentaje_compra = 0.02  # 2% del capital total por compra

posiciones = []  # Guardar las posiciones compradas
precio_maximo = 0  # Inicializa el precio máximo

def get_price():
    try:
        ticker = client.get_symbol_ticker(symbol=symbol)
        return float(ticker['price'])
    except Exception as e:
        print(f"[ERROR] No se pudo obtener el precio: {e}")
        return None

def get_usdt_balance():
    try:
        info = client.get_asset_balance(asset='USDT')
        return float(info['free']) if info else 0
    except Exception as e:
        print(f"[ERROR] No se pudo obtener el balance USDT: {e}")
        return 0

def get_btc_balance():
    try:
        info = client.get_asset_balance(asset='BTC')
        return float(info['free']) if info else 0
    except Exception as e:
        print(f"[ERROR] No se pudo obtener el balance BTC: {e}")
        return 0

def buy(usdt_cantidad, precio_actual):
    try:
        cantidad_btc = round(usdt_cantidad / precio_actual, 6)
        print(f"[SIMULACIÓN] COMPRA: {cantidad_btc} BTC por {usdt_cantidad} USDT a precio {precio_actual}")
        posiciones.append({'btc': cantidad_btc, 'precio_compra': precio_actual, 'precio_objetivo_venta': precio_maximo})
    except Exception as e:
        print(f"[ERROR] No se pudo realizar la compra: {e}")

def sell(cantidad_btc, precio_actual):
    try:
        print(f"[SIMULACIÓN] VENTA: {cantidad_btc} BTC a precio {precio_actual}")
    except Exception as e:
        print(f"[ERROR] No se pudo realizar la venta: {e}")

contador = 0
while True:
    contador += 1
    print(f"\n🕒 Iteración número: {contador}")

    precio_actual = get_price()
    if precio_actual is None:
        time.sleep(30)
        continue

    # Actualizar el precio máximo si el precio actual lo supera
    if precio_actual > precio_maximo:
        precio_maximo = precio_actual
        print(f"🔝 Nuevo precio máximo: {precio_maximo} USDT")

    usdt_disponible = get_usdt_balance()
    btc_disponible = get_btc_balance()
    capital_total_usdt = usdt_disponible + (btc_disponible * precio_actual)

    print(f"💰 Capital total: {capital_total_usdt:.2f} USDT (USDT: {usdt_disponible}, BTC: {btc_disponible})")
    print(f"📈 Precio actual: {precio_actual} USDT")

    # Compra si el precio actual está 5 mil USD por debajo del máximo
    if precio_actual <= (precio_maximo - diferencia_compra):
        usdt_a_invertir = capital_total_usdt * porcentaje_compra
        if usdt_a_invertir > usdt_disponible:
            usdt_a_invertir = usdt_disponible  # No gastar más de lo que tenés
        buy(usdt_a_invertir, precio_actual)

    # Venta si el precio vuelve al máximo anterior
    posiciones_para_vender = []
    for pos in posiciones:
        if precio_actual >= pos['precio_objetivo_venta']:
            sell(pos['btc'], precio_actual)
            posiciones_para_vender.append(pos)

    # Eliminar posiciones vendidas
    for pos in posiciones_para_vender:
        posiciones.remove(pos)

    time.sleep(30)
