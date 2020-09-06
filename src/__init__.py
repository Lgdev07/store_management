from flask import Flask

def create_app(config_name):
  from src.database import init_db
  from src.transacoes.views import transacoes_api

  app = Flask(__name__)

  try:
    app.config.from_object(f'config.{config_name}')
  except ImportError:
    raise Exception('Invalid Config')
  
  init_db(app)
  app.register_blueprint(transacoes_api, url_prefix='/api/v1/')

  return app