from src.database import db

class RecebimentoModel(db.Model):
    __tablename__ = 'recebimentos'

    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String())
    valor = db.Column(db.Float())
    descricao = db.Column(db.String())
    estabelecimento_id = db.Column(db.Integer, db.ForeignKey('estabelecimentos.id'))

    def __repr__(self):
        return f"<Recebimento {self.id}>"
    
    @property
    def serialize(self):
      return {
        'cliente': self.cliente,
        'valor': self.valor,
        'descricao': self.descricao,
      }