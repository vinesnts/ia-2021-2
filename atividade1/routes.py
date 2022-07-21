from atividade1.separador import SeparadorResource

class Routes:

  def __init__(self, app) -> None:
    app.add_route(f'/separar', SeparadorResource())
