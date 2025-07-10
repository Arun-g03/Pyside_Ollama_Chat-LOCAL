#!/usr/bin/env python3
"""
Program Flow Graph Utility

This script analyzes the PySide Ollama Chat application, builds a process/component
graph, and outputs an interactive HTML visualization using pyvis. The graph shows
the top-down flow of the main processes/components, with nodes for main, OllamaChat,
ServiceManager, UIManager, EventHandler, Worker, etc., and edges representing calls,
initializations, and signal connections.
"""

import os
from pathlib import Path
from pyvis.network import Network
import networkx as nx

# Define the main components and their relationships (based on previous analysis)
COMPONENTS = [
    "main.py",
    "OllamaChat",
    "ServiceManager",
    "UIManager",
    "EventHandler",
    "AppLifecycleManager",
    "ChatController",
    "Worker",
    "OllamaService",
    "ConversationService",
    "EnhancementService",
    "MemoryService",
    "SummarizationService",
    "ConversationManager",
    "ChatTab",
    "ModelTab",
    "PersonalityTab",
    "MemoryTab",
]

# Edges: (source, target, label)
EDGES = [
    ("main.py", "OllamaChat", "creates"),
    ("OllamaChat", "ServiceManager", "initializes"),
    ("OllamaChat", "UIManager", "initializes"),
    ("OllamaChat", "EventHandler", "initializes"),
    ("OllamaChat", "AppLifecycleManager", "initializes"),
    ("OllamaChat", "ChatController", "initializes"),
    ("ServiceManager", "OllamaService", "creates"),
    ("ServiceManager", "ConversationService", "creates"),
    ("ServiceManager", "EnhancementService", "creates"),
    ("ServiceManager", "MemoryService", "creates (if enabled)"),
    ("ServiceManager", "SummarizationService", "creates"),
    ("ServiceManager", "ConversationManager", "creates"),
    ("UIManager", "ChatTab", "creates"),
    ("UIManager", "ModelTab", "creates"),
    ("UIManager", "PersonalityTab", "creates"),
    ("UIManager", "MemoryTab", "creates (if enabled)"),
    ("EventHandler", "ChatController", "connects signals"),
    ("EventHandler", "OllamaService", "connects signals"),
    ("EventHandler", "ChatTab", "connects signals"),
    ("EventHandler", "ModelTab", "connects signals"),
    ("EventHandler", "PersonalityTab", "connects signals"),
    ("EventHandler", "ConversationManager", "connects signals"),
    ("ChatController", "Worker", "spawns for async"),
    ("ChatTab", "Worker", "receives stream"),
    ("Worker", "ChatTab", "emits stream_chunk_signal"),
    ("Worker", "EventHandler", "emits finished_signal"),
]


def build_graph():
    G = nx.DiGraph()
    for comp in COMPONENTS:
        G.add_node(comp)
    for src, tgt, label in EDGES:
        G.add_edge(src, tgt, label=label)
    return G


def visualize_graph(G, output_html):
    net = Network(height="900px", width="100%", directed=True, bgcolor="#232323", font_color="#fff")
    net.barnes_hut()
    
    # Add nodes
    for node in G.nodes:
        net.add_node(node, label=node, title=node, color="#0078d4" if node in ["main.py", "OllamaChat"] else "#444")
    # Add edges
    for src, tgt, data in G.edges(data=True):
        net.add_edge(src, tgt, label=data.get("label", ""), color="#aaa")
    
    net.set_options('''
    var options = {
      "nodes": {
        "borderWidth": 2,
        "shadow": true,
        "shape": "box",
        "font": {"size": 18}
      },
      "edges": {
        "arrows": {"to": {"enabled": true}},
        "font": {"size": 14, "align": "middle"},
        "smooth": {"type": "cubicBezier"}
      },
      "layout": {
        "hierarchical": {
          "enabled": true,
          "direction": "UD",
          "sortMethod": "directed"
        }
      },
      "physics": {
        "enabled": false
      }
    }
    ''')
    net.show(output_html)


def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    output_html = os.path.join(project_root, "Reports/PROGRAM_FLOW_GRAPH.html")
    G = build_graph()
    visualize_graph(G, output_html)
    print(f"✅ Program flow graph generated!")
    print(f"🌐 View the interactive graph at: {output_html}")

if __name__ == "__main__":
    main() 