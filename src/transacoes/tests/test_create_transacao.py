import json
from http import HTTPStatus

from src.transacoes.tests.test_common import TestCommon

class TestCreateTransacao(TestCommon):

    def test_wrong_client(self):
      data = {
        "estabelecimento": "60.701.190/2964-61",
        "cliente": "095.214.930-01",
        "valor": 590.01,
        "descricao": "Almoço em restaurante"
      }

      response = self.app.post(
          '/api/v1/transacao/',
          data=json.dumps(data),
          content_type='application/json'
      )

      self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_wrong_cnpj(self):
      data = {
        "estabelecimento": "61.701.190/2964-61",
        "cliente": "094.214.930-01",
        "valor": 590.01,
        "descricao": "Almoço em restaurante"
      }

      response = self.app.post(
          '/api/v1/transacao/',
          data=json.dumps(data),
          content_type='application/json'
      )

      self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_create_transaction(self):
      response = self.app.post(
        '/api/v1/transacao/',
        data=json.dumps({
          "estabelecimento": "60.701.190/2964-61",
          "cliente": "094.214.930-01",
          "valor": 590.01,
          "descricao": "Almoço em restaurante"
        }),
        content_type='application/json'
      )

      self.assertEqual(response.status_code, HTTPStatus.CREATED)
      self.assertEqual(json.loads(response.data), {"aceito":True})

