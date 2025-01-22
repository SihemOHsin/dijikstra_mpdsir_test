import streamlit as st
import networkx as nx
from graph_utils import save_graph, load_graph
import matplotlib.pyplot as plt
import os

# --- GENERAL SETTINGS ---
favicon = "https://res.cloudinary.com/dvz16ceua/image/upload/v1692056331/sihem/favicon_q0aqzk.ico"
PAGE_TITLE = "Mini Projet | Sihem Ouled Hsin"

st.set_page_config(page_title=PAGE_TITLE, page_icon=favicon, layout="wide")

# Load or create the graph
graph_file = "data/graph.json"
G = load_graph()


# Graph visualization
def draw_graph(G, path=None):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=10)
    if path:
        edges_in_path = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=edges_in_path, edge_color='red', width=2)
    plt.savefig("data/graph_visualization.png")  
    st.image("data/graph_visualization.png")

# Streamlit Sidebar Menu
st.sidebar.title(" Menu de Graph ")
menu_option = st.sidebar.radio(
    "Choisir le plus proche chemin",
    [
        "1. Afficher Graph",
        "2. Modifier Graph",
        "3. Trouver le chemin le plus court",
        "4. Enregistrer Graph",
        "5. Importer Graph",
        "6. Creation Graph"
    ]
)

# Menu Options
if menu_option.startswith("1"):
    st.title("Afficher Graph")
    if len(G.nodes) == 0:
        st.warning("The graph est vide")
    else:
        draw_graph(G)

elif menu_option.startswith("2"):
    st.title("Modifier Graph")
    u = st.text_input("De Noeud:")
    v = st.text_input("A Noeud:")
    weight = st.number_input("Distance:", min_value=1, step=1)

    if st.button("Modifier Graph"):
        if u and v:
            G.add_edge(u, v, weight=weight)
            save_graph(G, graph_file)
            st.success(f"Distance Ajouter: {u} -> {v} avec distance {weight}")
            draw_graph(G)
        else:
            st.warning("Specifier les deux nom des noeud ")

elif menu_option.startswith("3"):
    st.title("Trouver le chemin le plus court")
    if len(G.nodes) < 2:
        st.warning("Le graph doit avoir au moins deux nœuds pour trouver un chemin")
    else:
        source = st.selectbox("où es-tu:", list(G.nodes))
        target = st.selectbox("où veux-tu aller:", list(G.nodes))

        if st.button("Trouver plus court chemin"):
            try:
                path = nx.shortest_path(G, source=source, target=target, weight='weight')
                distance = nx.shortest_path_length(G, source=source, target=target, weight='weight')
                st.success(f"plus court chemin : {path} avec distance {distance}")
                draw_graph(G, path=path)
            except nx.NetworkXNoPath:
                st.error("Aucun chemin trouvé entre les nœuds sélectionnés")

elif menu_option.startswith("4"):
    st.title("Enregistrer Graph")
    file_path = st.text_input("Entrer path fichier to enregistrer graph:", graph_file)
    overwrite = st.radio("Overwrite si fichier exist?", ["oui", "Non"])
    if st.button("Enregistrer Graph"):
        if overwrite == "No" and os.path.exists(file_path):
            st.warning("Graph n'est pas Enregistrer. Changer le file path ou enable overwriting.")
        else:
            save_graph(G, file_path)
            st.success(f"Graph Enregistre a {file_path}.")

elif menu_option.startswith("5"):
    st.title("Importer Graph")
    file_path = st.text_input("Entrez le chemin du fichier pour importer le graph:", graph_file)
    if st.button("Importer Graph"):
        try:
            G = load_graph(file_path)
            st.success(f"Graph importer avec succes de {file_path}.")
            draw_graph(G)
        except Exception as e:
            st.error(f"Erreur import de graph: {e}")

elif menu_option.startswith("6"):
    st.title("Creation Graph")
    st.write("Cela effacera le graph actuel et écrasera le graph enregistré.")

    confirm = st.radio(
        "Voulez-vous écraser le graph existant?",
        options=["non", "oui"],
        index=0
    )

    if confirm == "oui" and st.button("Creer"):
        G.clear() 
        save_graph(G, graph_file)  # Saves the empty graph
        st.success("Nouvelle graph est cree et enregistrer.")
    elif confirm == "non" and st.button("Creer"):
        st.warning("Creation de Graph annulée. Le graph actuel reste inchangé.")

