import networkx as nx

def compute_all_metrics(G_weak: nx.Graph, G_un: nx.Graph):

    num_nodes = G_un.number_of_nodes()
    num_edges = G_un.number_of_edges()

    densidade = nx.density(G_un)
    assort = nx.degree_assortativity_coefficient(G_un)
    diametro = nx.diameter(G_un)
    peripheria = nx.periphery(G_un)
    clustering_global = nx.average_clustering(G_un)

    exemplos = list(G_un.nodes())[:3]
    clustering_local = {node: nx.clustering(G_un, node) for node in exemplos}

    centralities = {
        'degree': nx.degree_centrality(G_un),
        'closeness': nx.closeness_centrality(G_un),
        'betweenness': nx.betweenness_centrality(G_un),
        'eigenvector': nx.eigenvector_centrality(G_un, max_iter=300)
    }

    num_weak = len(list(nx.weakly_connected_components(G_weak)))
    num_strong = len(list(nx.strongly_connected_components(G_weak)))

    return {
        "nós": num_nodes,
        "arestas": num_edges,
        "densidade": densidade,
        "assortatividade": assort,
        "diâmetro": diametro,
        "periferia (exemplos)": peripheria[:5], # type: ignore
        "clustering_global": clustering_global,
        "clustering_local_exemplos": clustering_local,
        "centralities": centralities,
        "componentes_fracamente": num_weak,
        "componentes_fortemente": num_strong,
    }
