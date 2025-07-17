import networkx as nx
from pyvis.network import Network
import community as co
import os
import matplotlib.cm as cm
import matplotlib.colors as mcolors

def load_graph(path: str) -> nx.Graph:
    """Carrega grafo salvo em formato GEXF."""
    try:
        return nx.read_gexf(path)
    except FileNotFoundError:
        print(f"Erro: O arquivo GEXF '{path}' não foi encontrado. Certifique-se de que o caminho está correto.")
        raise
    except Exception as e:
        print(f"Erro ao carregar o grafo do arquivo '{path}': {e}")
        raise

def get_distinct_colors(num_colors):
    """
    Gera uma lista de cores distintas usando um colormap do Matplotlib
    e as retorna em formato hexadecimal.
    """
    colors = []
    if num_colors <= 20:
        # Usando a nova sintaxe para colormaps (para evitar o DeprecationWarning)
        cmap = cm.get_cmap('tab20', num_colors) # Ainda usa get_cmap para compatibilidade com versões antigas de Matplotlib
    else:
        # Usando a nova sintaxe para colormaps
        cmap = cm.get_cmap('hsv', num_colors) # Ainda usa get_cmap para compatibilidade com versões antigas de Matplotlib

    for i in range(num_colors):
        rgba = cmap(i)
        hex_color = mcolors.to_hex(rgba)
        colors.append(hex_color)
    return colors

def save_html_graph(G, path, node_color_attr=None, color_map=None):
    """Salva o grafo em um arquivo HTML interativo usando Pyvis com configurações de layout."""
    net = Network(height='600px', width='100%', notebook=False, cdn_resources='local', directed=False)
    net.from_nx(G)

    # --- Configurações do layout para melhor visualização (similar a força/repulsão) ---
    net.toggle_physics(True) # Garante que a física esteja ativada

    # CORREÇÃO: Usando aspas duplas para todas as chaves JSON e strings, e escapando as internas.
    net.set_options("""
    {
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -50,
          "centralGravity": 0.005,
          "springLength": 100,
          "springConstant": 0.08,
          "avoidOverlap": 0.9
        },
        "minVelocity": 0.75,
        "solver": "forceAtlas2Based"
      }
    }
    """)
    # -----------------------------------------------------------------------------

    if node_color_attr and color_map:
        for node_pyvis in net.nodes:
            node_id_nx = node_pyvis['id']
            attr_value = G.nodes[node_id_nx].get(node_color_attr)
            if attr_value is not None and attr_value in color_map:
                node_pyvis['color'] = color_map[attr_value]
            else:
                node_pyvis['color'] = "#97C2FC"
            
            if 'cluster' in G.nodes[node_id_nx]:
                node_pyvis['title'] = f"Cluster: {G.nodes[node_id_nx]['cluster']}"
            else:
                node_pyvis['title'] = f"Nó: {node_id_nx}"

    net.show(path)


def gerar_visualizacoes_clusters(input_path: str, output_dir: str):
    print("Carregando grafo...")
    G = load_graph(input_path)
    if G.is_directed():
        print("Convertendo grafo direcionado para não direcionado...")
        G = G.to_undirected()

    print("Detectando comunidades com Louvain...")
    partition = co.best_partition(G)
    nx.set_node_attributes(G, partition, 'cluster')

    os.makedirs(output_dir, exist_ok=True)

    clusters = sorted(list(set(partition.values())))
    num_clusters = len(clusters)
    distinct_colors = get_distinct_colors(num_clusters)
    
    cluster_color_map = {cluster_id: distinct_colors[i] for i, cluster_id in enumerate(clusters)}

    print("Salvando visualização do grafo completo...")
    save_html_graph(G, os.path.join(output_dir, "grafo_geral.html"), 
                    node_color_attr='cluster', color_map=cluster_color_map)

    print("Gerando visualizações individuais por cluster...")
    for c in clusters:
        sub_nodes = [n for n in G.nodes if partition[n] == c]
        subgraph = G.subgraph(sub_nodes).copy()

        if len(subgraph) < 5:
            print(f"Pulando cluster {c} com apenas {len(subgraph.nodes)} nós (muito pequeno).")
            continue

        output_path = os.path.join(output_dir, f"grafo_cluster_{c}.html")
        print(f"Salvando cluster {c} com {len(subgraph.nodes)} nós...")
        save_html_graph(subgraph, output_path, node_color_attr='cluster', color_map=cluster_color_map)

    print("Concluído!")

if __name__ == "__main__":
    gerar_visualizacoes_clusters("data/grafo.gexf", "data/htmls")