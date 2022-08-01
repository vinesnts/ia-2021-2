from graph import Graph

graph = Graph(0, 16)
graph.load_graph(filename='./atividade2/static/graph.txt')
graph.busca_em_largura()
graph.shortest_path()
graph.gen_graph_image()