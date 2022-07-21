import falcon
from atividade1.cors import CorsMiddleware

from atividade1.routes import Routes

app = application = falcon.App(middleware=[
  CorsMiddleware()
])

router = Routes(app)