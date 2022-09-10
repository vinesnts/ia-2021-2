import traceback
import falcon
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime
import base64

class GraphResource():

  def on_post(self, req, resp):
    try:
      body = req.media

      search_type = body['search_type']
      graph_matrix = body['graph']
      origin = int(body['origin'])
      destiny = int(body['destiny'])

      plt.clf()
      graph = Graph(origin, destiny)
      graph.set_graph(graph_matrix)
      filename = ''
      if search_type == 'p':
        graph.busca_em_profundidade()
        graph.shortest_path()
        filename = graph.gen_graph_image()
      elif search_type == 'l':
        graph.busca_em_largura()
        graph.shortest_path()
        filename = graph.gen_graph_image()
      elif search_type == 'a':
        graph.busca_a_estrela()
        filename = graph.gen_graph_image()

      if not graph_matrix or search_type not in ('p', 'l', 'a'):
        resp.media = {
          'success': False,
          'payload': None,
          'error': 'Nenhum grafo fornecido'
        }
        resp.status = falcon.HTTP_400
        return
      
      encoded = None
      with open(filename, 'rb') as file:
        encoded = base64.b64encode(file.read())

      resp.media = {
        'success': True,
        'payload': encoded.decode('utf-8'),
        'error': None
      }
      resp.status = falcon.HTTP_200
    except Exception as e:
      traceback.print_exc()
      print(str(e), flush=True)
      resp.status = falcon.HTTP_500
    finally:
      print('Graph ended')


class Graph():

  def __init__(self, origin: int = None, destiny: int = None) -> None:
    self.graph = []
    self.origin = origin
    self.destiny = destiny
    self.nodes_visited = []
    self.distance = []
    self.pred = []
    self.path = []
    pass

  def busca_a_estrela(self):
    meu_h = Graph.retorna_h(self.destiny, self.graph)
    calcular_caminho = Graph.retorna_caminho(self.destiny, self.graph, meu_h)
    caminhos = calcular_caminho(self.origin)
    self.path = caminhos

  def busca_em_largura(self):
    queue = []
    queue.append(self.origin)
    while len(queue) > 0:
      node = queue.pop(0)
      self.nodes_visited[node] = 1
      if node == self.destiny:
        if self.nodes_visited[n] == 0:
          self.nodes_visited[n] = 1
        break
      for n in self.graph[node]:
        if self.nodes_visited[n] == 0:
          self.nodes_visited[n] = 1
          self.distance[n] = self.distance[node] + 1
          self.pred[n] = node
          queue.append(n)

  def busca_em_profundidade(self):
    queue = []
    queue.append(self.origin)
    last = -1
    while len(queue) > 0:
      node = queue.pop()
      if self.nodes_visited[node] == 0:
        self.nodes_visited[node] = 1
        if last != -1:
          self.pred[last] = node
        last = node

        if node == self.destiny:
          break
        else:
          for n in self.graph[node]:
            queue.append(n)

  def shortest_path(self):
    self.path = []
    crawl = self.destiny
    self.path.append(crawl)
     
    while (self.pred[crawl] != -1):
      self.path.append(self.pred[crawl])
      crawl = self.pred[crawl]

  def set_origin_state(self, node) -> None:
    self.origin = node

  def set_destiny_state(self, node) -> None:
    self.destiny = node

  def load_graph(self, filename: str) -> None:
    with open(filename, 'r') as file:
      content = file.read()
      content_split = content.split('\n')
      for line in content_split:
        self.graph.append([int(x) for x in line.split(',')])
    if self.graph:
      self.nodes_visited = [0 for n in self.graph]
      self.distance = [100000 for n in self.graph]
      self.pred = [-1 for n in self.graph]

  def set_graph(self, text: str) -> None:
    content_split = text.split('\n')
    for line in content_split:
      self.graph.append([int(x) for x in line.split(',')])
    if self.graph:
      self.nodes_visited = [0 for n in self.graph]
      self.distance = [100000 for n in self.graph]
      self.pred = [-1 for n in self.graph]

  def enter_graph(self) -> None:
    try:
      node_qty = input('> Digite a quantidade de nós do grafo: ')
      node_qty = int(node_qty)
      for i in range(node_qty):
        line = input(f'> Digite os vizinhos do nó {i} separado por vírgula: ')
        self.graph.append(line.split(','))
    except ValueError as e:
      print('Entrada inválida')

  def enter_states(self) -> None:
    try:
      origin = input('> Digite o nó inicial: ')
      self.origin = int(origin)

      destiny = input('> Digite o nó destino: ')
      self.destiny = int(destiny)
    except ValueError as e:
      print('Entrada inválida')

  def gen_graph_image(self) -> None:
    G = nx.Graph()
    for i, node in enumerate(self.graph):
      edges = [(i, e) for e in node]
      G.add_node(i, color=("red" if i in self.path else "blue"))
      for edge in edges:
        G.add_edge(*edge, color=("red" if edge[0] in self.path and edge[1] in self.path else "black"))

    edges_color_map = nx.get_edge_attributes(G, "color")
    edges_colors = [edges_color_map.get(edge) for edge in G.edges()]
    nodes_color_map = nx.get_node_attributes(G, "color")
    nodes_colors = [nodes_color_map.get(node) for node in G.nodes()]

    nx.draw(G, with_labels=True, font_weight='bold', font_color='white', edge_color=edges_colors, node_color=nodes_colors)
    now = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    filename = f'./atividade2/static/temp-{now}.png'
    plt.savefig(filename)
    return filename

  @staticmethod
  def retorna_h(destino, node):
    def h(n):
        def caminhar(pos, visitados, distancia):
            caminhos = node[pos]
            distancias = []
            visitados.add(pos)
            if pos == destino:
                return distancia
            distancia += 1
            for novo_pos in caminhos:
                if novo_pos == destino:
                    return distancia
                if not novo_pos in visitados:
                    try:
                        distancias.append( caminhar(novo_pos,set(visitados), distancia) )
                    except:
                        pass
            return min(distancias)


        try:
            return caminhar(n,set(), 0)
        except:
            return None
                    
    return h

  @staticmethod
  def retorna_caminho(destino, node, meu_h):
    def meu_f(n):
        def calculo_f(pos, g_anterior):
            valor = meu_h(pos)
            if not valor:
                raise Exception('Não há caminho para determinado destino')
            return g_anterior + valor
        pos = n
        g = 0
        path = [pos]
        try:
            while True:
                menor = 999999
                idx_menor = -1
                caminhos = node[pos]
                for caminho in caminhos:
                    if caminho == destino:
                        path.append(caminho)
                        return path
                    if caminho in path:
                        continue
                    heuristica = calculo_f(caminho, g+1)
                    if heuristica < menor:
                        menor = heuristica
                        idx_menor = caminho
                if idx_menor != -1:
                    pos = idx_menor
                    path.append(idx_menor)
                    g += 1
                    continue
                else:
                    break
        except:
            return []
        return path
    return meu_f