from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from services.ipma_service import IPMAService
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

# Habilitar CORS para permitir requisições do frontend
CORS(app)

# Inicializar serviço do IPMA
ipma_service = IPMAService()


@app.route('/')
def index():
    """Servir a interface web"""
    return send_from_directory('.', 'index.html')


@app.route('/api', methods=['GET'])
def api_info():
    """Endpoint com informações da API"""
    return jsonify({
        'mensagem': 'API de Previsão Meteorológica - IPMA',
        'versao': '1.0.0',
        'endpoints': {
            '/': 'Interface web de testes',
            '/api': 'Informações da API',
            '/distritos': 'Lista todos os distritos disponíveis',
            '/localidades': 'Lista todas as localidades (filtro opcional: ?distrito_id=X)',
            '/previsao/<localidade_id>': 'Previsão meteorológica para uma localidade',
            '/previsao': 'Previsão com parâmetros de query (?localidade_id=X&dias=Y)'
        }
    }), 200


@app.route('/distritos', methods=['GET'])
def get_distritos():
    """
    Retorna a lista de todos os distritos

    Returns:
        JSON com lista de distritos
    """
    try:
        distritos = ipma_service.get_distritos()

        if not distritos:
            return jsonify({
                'erro': 'Não foi possível obter os distritos',
                'mensagem': 'Verifique a conexão com a API do IPMA'
            }), 503

        return jsonify({
            'sucesso': True,
            'total': len(distritos),
            'distritos': distritos
        }), 200

    except Exception as e:
        return jsonify({
            'erro': 'Erro interno do servidor',
            'mensagem': str(e)
        }), 500


@app.route('/localidades', methods=['GET'])
def get_localidades():
    """
    Retorna a lista de localidades, com filtro opcional por distrito

    Query Parameters:
        distrito_id (int): ID do distrito para filtrar (opcional)

    Returns:
        JSON com lista de localidades
    """
    try:
        distrito_id = request.args.get('distrito_id', type=int)

        localidades = ipma_service.get_localidades(distrito_id)

        if not localidades:
            return jsonify({
                'erro': 'Nenhuma localidade encontrada',
                'mensagem': 'Verifique o ID do distrito ou a conexão com a API'
            }), 404

        return jsonify({
            'sucesso': True,
            'total': len(localidades),
            'filtro_distrito': distrito_id,
            'localidades': localidades
        }), 200

    except Exception as e:
        return jsonify({
            'erro': 'Erro interno do servidor',
            'mensagem': str(e)
        }), 500


@app.route('/previsao/<int:localidade_id>', methods=['GET'])
def get_previsao_por_id(localidade_id):
    """
    Retorna a previsão meteorológica para uma localidade específica

    Args:
        localidade_id: ID da localidade

    Returns:
        JSON com a previsão meteorológica
    """
    try:
        dias = request.args.get('dias', default=5, type=int)

        # Validar número de dias
        if dias < 1 or dias > 10:
            return jsonify({
                'erro': 'Parâmetro inválido',
                'mensagem': 'O número de dias deve estar entre 1 e 10'
            }), 400

        previsao = ipma_service.get_previsao(localidade_id, dias)

        if not previsao:
            return jsonify({
                'erro': 'Previsão não encontrada',
                'mensagem': f'Não foi possível obter a previsão para a localidade {localidade_id}'
            }), 404

        return jsonify({
            'sucesso': True,
            'dados': previsao
        }), 200

    except Exception as e:
        return jsonify({
            'erro': 'Erro interno do servidor',
            'mensagem': str(e)
        }), 500


@app.route('/previsao', methods=['GET'])
def get_previsao_query():
    """
    Retorna a previsão meteorológica usando query parameters

    Query Parameters:
        localidade_id (int): ID da localidade (obrigatório)
        dias (int): Número de dias de previsão (opcional, padrão: 5)

    Returns:
        JSON com a previsão meteorológica
    """
    try:
        localidade_id = request.args.get('localidade_id', type=int)

        if not localidade_id:
            return jsonify({
                'erro': 'Parâmetro obrigatório ausente',
                'mensagem': 'É necessário fornecer o parâmetro localidade_id'
            }), 400

        return get_previsao_por_id(localidade_id)

    except Exception as e:
        return jsonify({
            'erro': 'Erro interno do servidor',
            'mensagem': str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handler para erros 404"""
    return jsonify({
        'erro': 'Endpoint não encontrado',
        'mensagem': 'O recurso solicitado não existe'
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handler para erros 405"""
    return jsonify({
        'erro': 'Método não permitido',
        'mensagem': 'O método HTTP utilizado não é suportado neste endpoint'
    }), 405


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=Config.PORT,
        debug=(Config.FLASK_ENV == 'development')
    )
