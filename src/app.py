from flask import Flask, request, jsonify, g
from flasgger import Swagger
import sqlite3
import json
from waitress import serve  # Importe o servidor Waitress

app = Flask(__name__)
swagger = Swagger(app)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('dados.db')
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/webhook', methods=['POST'])
def blip_webhook():
    """
    Endpoint para receber dados do webhook.

    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Dados
          properties:
            dados:
              type: string
    responses:
      200:
        description: Sucesso
    """
    try:
        data = json.dumps(request.get_json())
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO relatorios (dados) VALUES (?)", (data,))
        db.commit()
        return '', 200
    except Exception as e:
        db.rollback()
        return str(e), 500

@app.route('/relatorios', methods=['GET'])
def get_relatorios():
    """
    Endpoint para obter todos os relatórios.

    ---
    responses:
      200:
        description: Retorna todos os relatórios
    """
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM relatorios")
        relatorios = cursor.fetchall()
        return jsonify(relatorios)
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5001)  # Use o Waitress para servir a aplicação
