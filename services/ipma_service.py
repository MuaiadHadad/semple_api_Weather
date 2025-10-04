import requests
from typing import Dict, List, Optional
from config import Config


class IPMAService:
    """Serviço para comunicação com a API do IPMA"""

    def __init__(self):
        self.base_url = Config.IPMA_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

        # Mapeamento de IDs de distrito para nomes
        self.distritos_map = {
            1: "Aveiro",
            2: "Beja",
            3: "Braga",
            4: "Bragança",
            5: "Castelo Branco",
            6: "Coimbra",
            7: "Évora",
            8: "Faro",
            9: "Guarda",
            10: "Leiria",
            11: "Lisboa",
            12: "Portalegre",
            13: "Porto",
            14: "Santarém",
            15: "Setúbal",
            16: "Viana do Castelo",
            17: "Vila Real",
            18: "Viseu",
            30: "Ilha da Madeira",
            31: "Ilha de Porto Santo",
            40: "Ilha de Santa Maria",
            41: "Ilha de São Miguel",
            42: "Ilha Terceira",
            43: "Ilha da Graciosa",
            44: "Ilha de São Jorge",
            45: "Ilha do Pico",
            46: "Ilha do Faial",
            47: "Ilha das Flores",
            48: "Ilha do Corvo"
        }

    def get_distritos(self) -> List[Dict]:
        """
        Obtém a lista de todos os distritos disponíveis

        Returns:
            Lista de distritos com id e nome
        """
        try:
            # Usar o endpoint correto que tem lista de localidades
            response = self.session.get("https://api.ipma.pt/open-data/distrits-islands.json", timeout=10)
            response.raise_for_status()
            data = response.json()

            # Extrair IDs de distrito únicos da chave 'data'
            distritos_ids = set()
            if 'data' in data and isinstance(data['data'], list):
                for loc in data['data']:
                    distrito_id = loc.get('idDistrito')
                    if distrito_id:
                        distritos_ids.add(distrito_id)

            # Criar lista de distritos com nomes
            distritos = []
            for distrito_id in sorted(distritos_ids):
                nome = self.distritos_map.get(distrito_id, f"Distrito {distrito_id}")
                distritos.append({
                    'id': distrito_id,
                    'nome': nome
                })

            return distritos
        except requests.RequestException as e:
            print(f"Erro ao obter distritos: {e}")
            return []
        except Exception as e:
            print(f"Erro inesperado ao processar distritos: {e}")
            return []

    def get_localidades(self, distrito_id: Optional[int] = None) -> List[Dict]:
        """
        Obtém a lista de localidades, opcionalmente filtradas por distrito

        Args:
            distrito_id: ID do distrito para filtrar (opcional)

        Returns:
            Lista de localidades com id, nome e distrito
        """
        try:
            response = self.session.get("https://api.ipma.pt/open-data/distrits-islands.json", timeout=10)
            response.raise_for_status()
            data = response.json()

            localidades = []
            if 'data' in data and isinstance(data['data'], list):
                for loc in data['data']:
                    # Filtrar por distrito se fornecido
                    if distrito_id and loc.get('idDistrito') != distrito_id:
                        continue

                    localidades.append({
                        'id': loc.get('globalIdLocal'),
                        'nome': loc.get('local'),
                        'distrito_id': loc.get('idDistrito'),
                        'distrito_nome': self.distritos_map.get(loc.get('idDistrito'), 'Desconhecido'),
                        'latitude': loc.get('latitude'),
                        'longitude': loc.get('longitude')
                    })

            return localidades
        except requests.RequestException as e:
            print(f"Erro ao obter localidades: {e}")
            return []
        except Exception as e:
            print(f"Erro inesperado ao processar localidades: {e}")
            return []

    def get_previsao(self, localidade_id: int, dias: int = 5) -> Optional[Dict]:
        """
        Obtém a previsão meteorológica para uma localidade

        Args:
            localidade_id: ID da localidade
            dias: Número de dias de previsão (padrão: 5)

        Returns:
            Dados da previsão ou None se houver erro
        """
        try:
            # Tentar obter previsão específica da localidade
            url_especifica = f"{Config.IPMA_FORECAST_URL}/{localidade_id}.json"
            response = self.session.get(url_especifica, timeout=10)
            response.raise_for_status()
            data = response.json()

            if 'data' in data and isinstance(data['data'], list):
                return self._formatar_previsao(data['data'][:dias], localidade_id)

            return None
        except requests.RequestException as e:
            print(f"Erro ao obter previsão para localidade {localidade_id}: {e}")
            return None
        except Exception as e:
            print(f"Erro inesperado ao processar previsão: {e}")
            return None

    def _formatar_previsao(self, dados: List[Dict], localidade_id: int) -> Dict:
        """
        Formata os dados de previsão para um formato mais legível

        Args:
            dados: Dados brutos da API
            localidade_id: ID da localidade

        Returns:
            Dados formatados
        """
        previsoes = []

        for dia in dados:
            previsao_dia = {
                'data': dia.get('forecastDate'),
                'temperatura_minima': dia.get('tMin'),
                'temperatura_maxima': dia.get('tMax'),
                'probabilidade_precipitacao': dia.get('precipitaProb'),
                'vento_velocidade': dia.get('ffVento'),
                'vento_direcao': dia.get('ddVento'),
                'humidade_relativa': dia.get('hR'),
                'id_tempo': dia.get('idWeatherType'),
                'descricao_tempo': self._get_descricao_tempo(dia.get('idWeatherType'))
            }
            previsoes.append(previsao_dia)

        return {
            'localidade_id': localidade_id,
            'previsoes': previsoes,
            'total_dias': len(previsoes)
        }

    def _get_descricao_tempo(self, id_tempo: Optional[int]) -> str:
        """
        Converte o ID do tipo de tempo para descrição legível

        Args:
            id_tempo: ID do tipo de tempo

        Returns:
            Descrição do tempo
        """
        tipos_tempo = {
            1: "Céu limpo",
            2: "Céu pouco nublado",
            3: "Céu parcialmente nublado",
            4: "Céu muito nublado ou encoberto",
            5: "Céu nublado por nuvens altas",
            6: "Aguaceiros",
            7: "Aguaceiros fracos",
            8: "Aguaceiros fortes",
            9: "Chuva",
            10: "Chuva fraca ou chuvisco",
            11: "Chuva forte",
            12: "Períodos de chuva",
            13: "Períodos de chuva fraca",
            14: "Períodos de chuva forte",
            15: "Trovoada",
            16: "Aguaceiros com trovoada",
            17: "Neve",
            18: "Neve fraca",
            19: "Granizo",
            20: "Nevoeiro",
            21: "Neblina",
            22: "Vento forte",
            23: "Nortada",
            24: "Geada",
            25: "Chuva e neve",
            26: "Aguaceiros e trovoada",
            27: "Nebulosidade variável"
        }

        return tipos_tempo.get(id_tempo, "Informação não disponível")
