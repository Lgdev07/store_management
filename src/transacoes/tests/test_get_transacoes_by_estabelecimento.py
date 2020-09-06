import json
from http import HTTPStatus

from src.transacoes.tests.test_common import TestCommon

class TestGetTransacoes(TestCommon):

  def test_get_transacoes_no_cnpj(self):
    response = self.app.get('/api/v1/transacoes/estabelecimento/')

    self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
    self.assertEqual(json.loads(response.data), {"erro": "Favor informar o CNPJ"})

  def test_get_transacoes_wrong_cnpj(self):
    response = self.app.get('/api/v1/transacoes/estabelecimento/?cnpj=61701190296461')

    self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
    self.assertEqual(json.loads(response.data), {"erro": "CNPJ não encontrado"})
