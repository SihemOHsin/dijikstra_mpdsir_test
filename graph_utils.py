import os
import networkx as nx
import json

def save_graph(G, filename="data/graph.json"):
    """Save the graph to a JSON file."""
    data = nx.node_link_data(G)
    with open(filename, 'w') as f:
        json.dump(data, f)

def load_graph(filename="data/graph.json"):
    """Load the graph from a JSON file."""
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        # Validate that the data has the necessary keys
        if 'nodes' in data and 'links' in data:
            return nx.node_link_graph(data)
        else:
            raise ValueError("Invalid graph structure in JSON file.")
    except (FileNotFoundError, ValueError, json.JSONDecodeError):
        # Return an empty graph if the file is missing or invalid
        return nx.DiGraph()
