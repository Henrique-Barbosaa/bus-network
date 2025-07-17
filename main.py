import streamlit as st
from analysis.graph_loader import load_graph, get_largest_weakly_connected, get_undirected_connected
from analysis.metrics import compute_all_metrics
from analysis.visualizations import show_metrics_dashboard, show_degree_histogram, show_centrality_comparison, show_cluster_visualization

st.set_page_config(layout="wide")
st.title("🚌 Análise de Redes - Cidades por Ônibus (ANTT)")

G = load_graph("data/grafo.gexf")
G_weak = get_largest_weakly_connected(G)
G_un = get_undirected_connected(G)

st.markdown("## 🌐 Sobre o Grafo")
st.markdown("""
Este dataset representa fluxos de passageiros de ônibus entre cidades brasileiras.
- **Nós**: cidades envolvidas.
- **Arestas**: relações de viagem entre cidades.
Para métricas específicas, usamos:
  - **Grafo fraco (mantém direção)** → componentes fortemente/fracamente conectados.
  - **Grafo não direcionado** → matriz de adjacência, densidade, diâmetro, centralidades, clustering, etc.
""")

with st.expander("🔎 Métricas da Rede"):
    metrics = compute_all_metrics(G_weak, G_un)
    show_metrics_dashboard(metrics)

with st.expander("📊 Distribuição de Grau"):
    show_degree_histogram(G_un)

with st.expander("🏆 Centralidades"):
    show_centrality_comparison(G_un, G)

with st.expander("🧩 Visualização por Cluster"):
    show_cluster_visualization()
