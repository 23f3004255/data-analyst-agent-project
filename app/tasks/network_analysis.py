import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from app.utils import fig_to_base64,read_csv_files

async def process(qtext, files):
    dfs = await read_csv_files(files)

    if not dfs:
        return {"error": "No CSV files provided"}

    # Assuming we use the first CSV for analysis
    df = dfs[0]

    # --- Network analysis ---
    G = nx.Graph()
    for _, row in df.iterrows():
        G.add_edge(row["source"], row["target"])

    edge_count = G.number_of_edges()
    degrees = dict(G.degree())
    highest_degree_node = max(degrees, key=degrees.get)
    average_degree = sum(degrees.values()) / len(G)
    density = nx.density(G)
    shortest_path_alice_eve = nx.shortest_path_length(G, "Alice", "Eve")

    # Plot network graph
    pos = nx.spring_layout(G, seed=42)
    fig1, ax1 = plt.subplots()
    nx.draw(G, pos, with_labels=True, node_color="lightblue",
            edge_color="gray", node_size=500, font_size=10, ax=ax1)
    network_graph_b64 = fig_to_base64(fig1)

    # Degree histogram
    degree_values = list(degrees.values())
    fig2, ax2 = plt.subplots()
    ax2.bar(range(len(degree_values)), sorted(degree_values, reverse=True), color="green")
    ax2.set_xlabel("Node Index")
    ax2.set_ylabel("Degree")
    degree_histogram_b64 = fig_to_base64(fig2)

    # Build JSON result
    result = {
        "edge_count": edge_count,
        "highest_degree_node": highest_degree_node,
        "average_degree": average_degree,
        "density": density,
        "shortest_path_alice_eve": shortest_path_alice_eve,
        "network_graph": network_graph_b64,
        "degree_histogram": degree_histogram_b64
    }

    return result