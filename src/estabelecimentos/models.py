from src.database import db

class EstabelecimentoModel(db.Model):
    __tablename__ = 'estabelecimentos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String())
    cnpj = db.Column(db.String())
    dono = db.Column(db.String())
    telefone = db.Column(db.String())

    def __repr__(self):
        return f"<Estabelecimento {self.nome}>"
    
    @property
    def serialize(self):
      cnpj = self.format_cnpj(self.cnpj)

      return {
        'id': self.id,
        'nome': self.nome,
        'cnpj': cnpj,
        'dono': self.dono,
        'telefone': self.telefone,
      }
    
    def format_cnpj(self, cnpj):
      return cnpj[:2] + '.' + cnpj[2:5] + '.' + cnpj[5:8] + '/' + cnpj[8:12] + '-' + cnpj[12:]
