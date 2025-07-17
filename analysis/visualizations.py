import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import streamlit as st
import networkx as nx
import seaborn as sns
import os

def show_metrics_dashboard(metrics: dict):
    st.metric("🔹 Nº de Nós", metrics["nós"])
    st.metric("🔸 Nº de Arestas", metrics["arestas"])
    col1, col2 = st.columns(2)
    col1.metric("📏 Densidade", f"{metrics['densidade']:.4f}")
    col2.metric("🔗 Assortatividade", f"{metrics['assortatividade']:.4f}")
    
    st.markdown(f"**📐 Diâmetro da Rede**: {metrics['diâmetro']}")
    st.markdown(f"**📍 Periferia (exemplos)**: {metrics['periferia (exemplos)']}")
    st.markdown(f"**🌍 Clustering Global**: {metrics['clustering_global']:.4f}")
    
    st.markdown("### 📌 Clustering Local (exemplos):")
    for node, val in metrics["clustering_local_exemplos"].items():
        st.write(f"- {node}: {val:.3f}")
    
    st.markdown("### 🔄 Componentes Conectados")
    st.write(f"- Fortemente conectados: {metrics['componentes_fortemente']}")
    st.write(f"- Fracamente conectados: {metrics['componentes_fracamente']}")

def show_degree_histogram(G):
    graus = [d for n, d in G.degree()]
    fig, ax = plt.subplots()
    sns.histplot(graus, bins=50, kde=False, ax=ax, color="skyblue")
    ax.set_title("Distribuição de Grau dos Nós")
    ax.set_xlabel("Grau")
    ax.set_ylabel("Frequência")
    st.pyplot(fig)

def show_centrality_comparison(G_un, G):
    centralities = {
        "Degree": nx.degree_centrality(G_un),
        "Closeness": nx.closeness_centrality(G_un),
        "Betweenness": nx.betweenness_centrality(G_un),
        "Eigenvector": nx.eigenvector_centrality(G_un, max_iter=300),
        "In-Degree": nx.in_degree_centrality(G),
        "Out-Degree": nx.out_degree_centrality(G)
    }

    st.markdown("### 🌟 Top 10 nós por medida de centralidade:")

    cols = st.columns(6)
    for i, (name, centrality) in enumerate(centralities.items()):
        top = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:10]
        with cols[i]:
            st.markdown(f"#### {name}")
            for node, val in top:
                st.markdown(f"- {node} ({val:.3f})")

def show_cluster_visualization():
    st.markdown("### 🔍 Selecione o cluster:")

    grafo_dir = "data/htmls"
    arquivos_html = sorted([f for f in os.listdir(grafo_dir) if f.startswith("grafo_cluster_")])

    nomes_customizados = {
        "grafo_cluster_5.html": "Nordeste",
        "grafo_cluster_43.html": "Centro Oeste e Norte",
        "grafo_cluster_15.html": "Interior de SP e MG"
    }

    opcoes = {}
    for f in arquivos_html:
        nome = nomes_customizados.get(f, f.replace("grafo_cluster_", "Cluster ").replace(".html", ""))
        opcoes[f] = nome

    if not opcoes:
        st.warning("Nenhum cluster encontrado.")
        return

    nomes_ordenados = sorted(opcoes.items(), key=lambda x: (x[1] != "Nordeste", x[1]))
    display_names = [v for _, v in nomes_ordenados]
    file_lookup = {v: k for k, v in opcoes.items()}

    opcao = st.selectbox("Escolha um cluster para visualizar:", display_names, index=0)
    selected_file = file_lookup[opcao]

    with open(os.path.join(grafo_dir, selected_file), "r", encoding="utf-8") as f:
        html_content = f.read()
    components.html(html_content, height=800, scrolling=True)