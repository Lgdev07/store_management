import requests 
from marshmallow import Schema, fields, post_load, validates, ValidationError

from src.database import db
from src.estabelecimentos.models import EstabelecimentoModel
from src.recebimentos.models import RecebimentoModel

class TransacoesSchema(Schema):
    estabelecimento = fields.Str(required=True)
    cliente = fields.Str(required=True)
    valor = fields.Float(required=True)
    descricao = fields.Str(required=True)

    @validates('estabelecimento')
    def validate_estabelecimento(self, estabelecimento, **kwargs):
        remove_characters = [".", "/", "-"]

        for character in remove_characters:
            estabelecimento = estabelecimento.replace(character, "")

        r = requests.get(f"https://www.receitaws.com.br/v1/cnpj/{estabelecimento}")
        
        try:
            data = r.json()
        except ValueError:
            raise ValidationError('Error connecting to External API')

        if data["status"] == "ERROR":
            raise ValidationError(f"CNPJ {estabelecimento} did not found")

        estab_found = EstabelecimentoModel.query.filter_by(cnpj=estabelecimento).first()

        if estab_found:
            self.estabelecimento_id = estab_found.id
            return
        
        self.create_estabelecimento(data, estabelecimento)

    @validates('cliente')
    def validate_cliente(self, cliente, **kwargs):
        remove_characters = [".", "-"]

        for character in remove_characters:
            cliente = cliente.replace(character, "")

        if not self.validate_cpf(cliente):
            raise ValidationError(f"Invalid CPF {cliente}")

    def create_estabelecimento(self, data, estabelecimento):
        values = {
            "nome": data["fantasia"] or data["nome"],
            "cnpj": estabelecimento,
            "dono": data["nome"],
            "telefone": data["telefone"]
        }

        estab = EstabelecimentoModel(**values)
        db.session.add(estab)
        db.session.commit()
        db.session.refresh(estab)
        
        self.estabelecimento_id = estab.id

    @post_load
    def create_recebimento(self, data, **kwargs):
        values = {
            "cliente": data["cliente"],
            "valor": data["valor"],
            "descricao": data["descricao"],
            "estabelecimento_id": self.estabelecimento_id
        }

        recebimento = RecebimentoModel(**values)
        db.session.add(recebimento)
        db.session.commit()

    def validate_cpf(self, cpf):
        if len(cpf) < 11:
            return False    
        
        if cpf in [s * 11 for s in [str(n) for n in range(10)]]:
            return False
        
        calc = lambda t: int(t[1]) * (t[0] + 2)
        d1 = (sum(map(calc, enumerate(reversed(cpf[:-2])))) * 10) % 11
        d2 = (sum(map(calc, enumerate(reversed(cpf[:-1])))) * 10) % 11
        return str(d1) == cpf[-2] and str(d2) == cpf[-1]