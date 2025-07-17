import networkx as nx

def load_graph(path: str) -> nx.Graph:
    return nx.read_gexf(path)

def get_largest_weakly_connected(G: nx.Graph) -> nx.Graph:
    """Retorna o maior componente fracamente conectado de um grafo (mantém direcionamento)."""
    if nx.is_weakly_connected(G):
        return G
    wk = max(nx.weakly_connected_components(G), key=len)
    return G.subgraph(wk).copy()

def get_undirected_connected(G: nx.Graph) -> nx.Graph:
    """Converte para grafo não-direcionado e retorna o maior componente conectado."""
    G_und = G.to_undirected()
    if nx.is_connected(G_und):
        return G_und
    mt = max(nx.connected_components(G_und), key=len)
    return G_und.subgraph(mt).copy()