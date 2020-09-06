from http import HTTPStatus

from marshmallow import ValidationError
from flask import Blueprint, jsonify
from flask import request

from src.transacoes.schemas import TransacoesSchema
from src.estabelecimentos.models import EstabelecimentoModel
from src.recebimentos.models import RecebimentoModel
from src.database import db

transacoes_api = Blueprint('transacoes_api', __name__)

@transacoes_api.route('/transacao/', methods=["POST"])
def create_transacao():
  data = request.get_json()
  schema = TransacoesSchema()
  
  try:
    schema.load(data)
  except ValidationError:
    return jsonify({"aceito": False}), HTTPStatus.BAD_REQUEST

  return jsonify({"aceito": True}), HTTPStatus.CREATED

@transacoes_api.route('/transacoes/estabelecimento/', methods=["GET"])
def get_transacoes_by_estabelecimento():
  cnpj = request.args.get('cnpj')

  if not cnpj:
    return jsonify({"erro": "Favor informar o CNPJ"}), HTTPStatus.BAD_REQUEST

  estabelecimento = EstabelecimentoModel.query.filter_by(cnpj=cnpj).first()

  if not estabelecimento:
    return jsonify({"erro": "CNPJ não encontrado"}), HTTPStatus.BAD_REQUEST

  recebimentos = RecebimentoModel.query.filter_by(estabelecimento_id=estabelecimento.id).all()

  return_values = {
    "estabelecimento": estabelecimento.serialize,
  }

  if not recebimentos:
    return_values.update({
      "recebimentos": [],
      "total_recebido": 0
    })
    return jsonify(return_values), HTTPStatus.ACCEPTED
  
  recebimentos_list = [receb.serialize for receb in recebimentos]
  total_values = sum(receb.valor for receb in recebimentos)

  return_values.update({
    "recebimentos": recebimentos_list,
    "total_recebido": total_values
  })

  return jsonify(return_values), HTTPStatus.ACCEPTED
