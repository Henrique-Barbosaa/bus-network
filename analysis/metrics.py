import networkx as nx

def get_big_cities_clustering(G_un: nx.Graph):
    cidades = ["SAO PAULO/SP", "CURITIBA/PR", "SALVADOR/BA", "MANAUS/AM", "BRASILIA/DF"]

    clustering = {}
    for cidade in cidades:
        if cidade in G_un:
            clustering[cidade] = nx.clustering(G_un, cidade)
        else:
            clustering[cidade] = "Cidade não encontrada no grafo"

    return clustering


def compute_all_metrics(G: nx.Graph, G_un: nx.Graph):

    num_nodes = G_un.number_of_nodes()
    num_edges = G_un.number_of_edges()

    densidade = nx.density(G_un)
    assort = nx.degree_assortativity_coefficient(G_un)
    diametro = nx.diameter(G_un)
    peripheria = nx.periphery(G_un)
    clustering_global = nx.average_clustering(G_un)


    bridges = list(nx.bridges(G_un))
    grandes_cidades = ["SAO PAULO/SP", "CURITIBA/PR", "SALVADOR/BA", "BRASILIA/DF", "MANAUS/AM"]
    # Filtrar bridges locais
    bridges_locais = [b for b in bridges if b[0] in grandes_cidades or b[1] in grandes_cidades]


    clustering_local = get_big_cities_clustering(G_un)

    centralities = {
        'degree': nx.degree_centrality(G_un),
        'closeness': nx.closeness_centrality(G_un),
        'betweenness': nx.betweenness_centrality(G_un),
        'eigenvector': nx.eigenvector_centrality(G_un, max_iter=300)
    }

    num_weak = len(list(nx.weakly_connected_components(G)))
    num_strong = len(list(nx.strongly_connected_components(G)))

    return {
        "nós": num_nodes,
        "arestas": num_edges,
        "densidade": densidade,
        "assortatividade": assort,
        "diâmetro": diametro,
        "periferia": peripheria[:10], # type: ignore
        "clustering_global": clustering_global,
        "clustering_local": clustering_local,
        "centralities": centralities,
        "componentes_fracamente": num_weak,
        "componentes_fortemente": num_strong,
        "bridges": bridges,
        "local_bridges": bridges_locais,
    }
