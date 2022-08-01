from atividade1.separador import SeparadorResource
from atividade2.graph import GraphResource

class Routes:

  def __init__(self, app) -> None:
    app.add_route(f'/separar', SeparadorResource())
    app.add_route(f'/graph', GraphResource())