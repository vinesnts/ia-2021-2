import queue
import networkx as nx
import matplotlib.pyplot as plt

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
    while len(queue) > 0:
      node = queue.pop()
      if self.nodes_visited[node] == 0:
        self.nodes_visited[node] = 1

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

graph = Graph(0, 16)
graph.load_graph(filename='./atividade2/graph.txt')
graph.busca_em_largura()
graph.shortest_path()
# graph.enter_states()

G = nx.Graph()
# G.add_nodes_from([i for i, n in enumerate(graph.graph)])
for i, node in enumerate(graph.graph):
  edges = [(i, e) for e in node]
  G.add_node(i, color=("red" if i in graph.path else "blue"))
  for edge in edges:
    G.add_edge(*edge, color=("red" if edge[0] in graph.path and edge[1] in graph.path else "black"))

edges_color_map = nx.get_edge_attributes(G, "color")
edges_colors = [edges_color_map.get(edge) for edge in G.edges()]
nodes_color_map = nx.get_node_attributes(G, "color")
nodes_colors = [nodes_color_map.get(node) for node in G.nodes()]

nx.draw(G, with_labels=True, font_weight='bold', font_color='white', edge_color=edges_colors, node_color=nodes_colors)
plt.savefig('teste.png')