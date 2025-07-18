import streamlit as st
from analysis.graph_loader import load_graph, get_largest_weakly_connected, get_undirected_connected
from analysis.metrics import compute_all_metrics
from analysis.visualizations import show_metrics_dashboard, show_centrality_comparison, show_cluster_visualization

st.set_page_config(layout="wide")
st.title("🚌 Conexões entre Cidades via Ônibus Rodoviário no Brasil")

G = load_graph("data/grafo.gexf")
G_weak = get_largest_weakly_connected(G)
G_un = get_undirected_connected(G)


st.markdown("""
## ℹ️ Sobre o Dataset e a Análise

Este projeto analisa a rede de conexões entre cidades brasileiras a partir de dados disponibilizados pela **ANTT (Agência Nacional de Transportes Terrestres)**. O dataset utilizado contém registros de **viagens interestaduais de ônibus**, representando o fluxo de passageiros entre diferentes municípios do Brasil.

### 📌 Estrutura da Rede
- **Nós**: Cada nó representa uma **cidade brasileira** que está envolvida em pelo menos uma rota de ônibus interestadual.
- **Arestas**: Cada aresta indica a existência de **viagem direta entre duas cidades**, conforme registrado nas autorizações da ANTT. A direção da aresta representa o **sentido da viagem** (origem → destino).

### 🔍 Objetivo da Análise
Compreender as propriedades estruturais dessa rede de mobilidade interurbana, explorando conceitos fundamentais da teoria de grafos e análise de redes complexas. Com isso, podemos responder a perguntas como:
- Quais cidades são mais conectadas e centrais?
- Qual é o nível de conectividade entre as cidades brasileiras por transporte rodoviário intermunicipal?
- Existem agrupamentos regionais (comunidades)?
- A rede é densa ou esparsa? O que isso significa sobre a conectividade do sistema de ônibus?
- Quais comunidades regionais foram identificadas na rede de ônibus?
- Existe coerência geográfica entre os clusters detectados e as regiões reais do Brasil?

### 🧭 Tipos de Grafos Utilizados
Para diferentes análises, usamos duas representações do grafo:

- **Grafo Direcionado (Original)**: mantém o sentido das viagens (útil para componentes fortemente e fracamente conectados).
- **Grafo Não Direcionado**: ignora a direção das viagens (útil para cálculos como **diâmetro**, **densidade**, **centralidade**, **clustering**, etc).

A análise contempla tanto medidas de conectividade quanto centralidade, além de visualizações interativas para explorar os agrupamentos regionais (clusters) obtidos com o algoritmo de **detecção de comunidades Louvain**.
""")

with st.expander("🔎 Métricas da Rede"):
    metrics = compute_all_metrics(G, G_un)
    show_metrics_dashboard(metrics, G)

with st.expander("🏆 Centralidades"):
    show_centrality_comparison(G_un, G)

with st.expander("🧩 Visualização por Cluster"):
    show_cluster_visualization()
