from flask import Flask, request, jsonify, render_template
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import folium
import time

app = Flask(__name__)

# Dados dos clientes
dados_clientes = [
    {"nome": "Cliente A", "codigo": "001", "endereco": "SHCN Comércio Local Norte 112 BL A - Brasília, DF", "produtos": ["Produto X", "Produto Y", "Produto Z"]},
    {"nome": "Cliente B", "codigo": "002", "endereco": "Asa Norte Comércio Local Norte 111 S/N Loja 07, 59 - Asa Norte, Brasília - DF", "produtos": ["Produto Y", "Produto Z"]},
    {"nome": "Cliente C", "codigo": "003", "endereco": "SHCN CLN 111 BL B - Asa Norte, Brasília - DF", "produtos": ["Produto X", "Produto Z"]},
    {"nome": "Cliente D", "codigo": "004", "endereco": "Asa Norte CLN 311 BL E Terreo, Loja S 02,06,10,12,16,20 E 72 - Asa Norte, Brasília - DF", "produtos": ["Produto X"]},
    {"nome": "Cliente E", "codigo": "005", "endereco": "SHCN CL QD 311 BLOCO A 72 - Asa Norte, Brasília - DF", "produtos": ["Produto Y"]},
    {"nome": "Cliente F", "codigo": "006", "endereco": "SCN Q 5 Quadra 5 Bloco A Loja 52 W Terreo - Asa Norte, Brasília - DF", "produtos": ["Produto Z"]},
    {"nome": "Cliente G", "codigo": "007", "endereco": "Asa Sul Comércio Local Sul 412 B LOJA - Brasília, DF", "produtos": ["Produto X", "Produto Y"]},
    {"nome": "Cliente H", "codigo": "008", "endereco": "SHCS CLS 412 - Brasilia, DF", "produtos": ["Produto Z", "Produto X"]},
    {"nome": "Cliente I", "codigo": "009", "endereco": "Bloco D Q, Cls 413 Bloco B, 16 - E 22, Brasília - DF", "produtos": ["Produto Y", "Produto Z", "Produto X"]},
    {"nome": "Cliente J", "codigo": "010", "endereco": "Asa Sul CLS 412 BL D LT 43 LT 44 LJ 29 - Asa Sul, Brasília - DF", "produtos": ["Produto Z"]},
    {"nome": "Cliente K", "codigo": "011", "endereco": "SHCS Comércio Residencial Sul 510 - Brasília, DF", "produtos": ["Produto X", "Produto Y"]},
    {"nome": "Cliente L", "codigo": "012", "endereco": "Asa Sul CRS 510 BL C LJ 63 - Asa Sul, Brasília - DF", "produtos": ["Produto Y", "Produto Z"]}
]

# Função para obter as informações de latitude e longitude de um endereço
def obter_lat_long(endereco):
    geolocator = Nominatim(user_agent="cliente_proximo")
    location = geolocator.geocode(endereco)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

# Adicionar informações de latitude e longitude aos dados dos clientes
for cliente in dados_clientes:
    cliente['latitude'], cliente['longitude'] = obter_lat_long(cliente['endereco'])
    # Espere alguns segundos para evitar exceder o limite de requisições por segundo
    time.sleep(1)

# Função para encontrar clientes próximos
def clientes_proximos(codigo_cliente, raio_km):
    cliente_referencia = next((cliente for cliente in dados_clientes if cliente['codigo'] == codigo_cliente), None)
    if cliente_referencia is None:
        return []

    clientes_proximos = []
    for cliente in dados_clientes:
        if cliente['codigo'] != codigo_cliente:
            distancia = geodesic((cliente_referencia['latitude'], cliente_referencia['longitude']), (cliente['latitude'], cliente['longitude'])).kilometers
            if distancia <= raio_km:
                clientes_proximos.append((cliente, cliente['latitude'], cliente['longitude']))

    return clientes_proximos

# Rota para exibir a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para buscar clientes próximos
@app.route('/clientes_proximos', methods=['POST'])
def buscar_clientes_proximos():
    codigo_cliente = request.form.get('codigo_cliente')
    raio_km = float(request.form.get('raio_km'))
    clientes = clientes_proximos(codigo_cliente, raio_km)
    
    # Criar o mapa
    mapa = folium.Map(location=[-15.788497, -47.879873], zoom_start=12)

    # Adicionar marcador para o cliente de referência
    cliente_referencia = next((cliente for cliente in dados_clientes if cliente['codigo'] == codigo_cliente), None)
    if cliente_referencia and cliente_referencia['latitude'] is not None and cliente_referencia['longitude'] is not None:
        folium.Marker(location=(cliente_referencia['latitude'], cliente_referencia['longitude']), popup=cliente_referencia['nome']).add_to(mapa)

    # Adicionar marcadores para os clientes próximos
    for cliente, lat, lon in clientes:
        if lat is not None and lon is not None:
            folium.Marker(location=(lat, lon), popup=f"{cliente['nome']}").add_to(mapa)

    # Salvar o mapa como um arquivo HTML temporário
    mapa.save('templates/mapa.html')
    
    # Retornar o conteúdo do mapa HTML para ser exibido na página
    with open('templates/mapa.html', 'r') as file:
        mapa_html = file.read()

    return mapa_html


if __name__ == '__main__':
    app.run(debug=True)
