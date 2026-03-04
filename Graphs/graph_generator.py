import json
from typing import List, Dict, Any, Optional
import networkx as nx
import plotly.graph_objects as go
import plotly.offline as pyo
import logging

logger = logging.getLogger(__name__)


class GraphGenerator:

    def generate_interactive_graph(self,
                                   nodes: List[Dict[str, Any]],
                                   edges: List[Dict[str, Any]],
                                   title: str = "Graph Analysis") -> str:

        G = nx.Graph()

        node_labels = {}
        node_colors = {}
        node_sizes = {}

        color_map = {
            "person": "#FF6B6B",
            "company": "#4ECDC4",
            "domain": "#45B7D1",
            "email": "#96CEB4",
            "ip": "#FFE194",
            "default": "#95A5A6"
        }

        for node in nodes:
            node_id = node["id"]
            node_type = node.get("type", "default")
            G.add_node(node_id, **node)
            node_labels[node_id] = node.get("label", node_id)
            node_colors[node_id] = color_map.get(node_type, color_map["default"])
            node_sizes[node_id] = 30

        for edge in edges:
            G.add_edge(edge["from"], edge["to"], label=edge.get("label", ""))

        pos = nx.spring_layout(G, k=2, iterations=50)

        edge_trace_x = []
        edge_trace_y = []
        edge_text = []

        for edge in G.edges(data=True):
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace_x.extend([x0, x1, None])
            edge_trace_y.extend([y0, y1, None])
            edge_text.append(edge[2].get('label', ''))

        edge_trace = go.Scatter(
            x=edge_trace_x, y=edge_trace_y,
            line=dict(width=1, color='#888'),
            hoverinfo='text',
            mode='lines',
            text=edge_text * 3
        )

        node_trace = go.Scatter(
            x=[pos[node][0] for node in G.nodes()],
            y=[pos[node][1] for node in G.nodes()],
            mode='markers+text',
            text=[node_labels[node] for node in G.nodes()],
            textposition="top center",
            hovertext=[f"ID: {node}<br>Type: {G.nodes[node].get('type', 'unknown')}"
                       for node in G.nodes()],
            hoverinfo='text',
            marker=dict(
                color=[node_colors[node] for node in G.nodes()],
                size=[node_sizes[node] for node in G.nodes()],
                line=dict(width=2, color='white')
            )
        )

        fig = go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                title=title,
                showlegend=False,
                hovermode='closest',
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                plot_bgcolor='rgba(0,0,0,0)',
                width=1200,
                height=800,
                margin=dict(l=20, r=20, t=40, b=20)
            )
        )

        config = {
            'scrollZoom': True,
            'displayModeBar': True,
            'modeBarButtonsToAdd': ['drawline', 'drawopenpath', 'eraseshape']
        }

        html = pyo.plot(fig, include_plotlyjs='cdn', output_type='div', config=config)

        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{title}</title>
            <meta charset="utf-8">
            <style>
                body {{
                    margin: 0;
                    padding: 20px;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                }}
                .graph-container {{
                    background: white;
                    border-radius: 20px;
                    padding: 20px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                    margin: 20px auto;
                    max-width: 1400px;
                }}
                h1 {{
                    color: white;
                    text-align: center;
                    margin-bottom: 30px;
                    font-weight: 300;
                    letter-spacing: 2px;
                }}
                .controls {{
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    background: white;
                    padding: 15px;
                    border-radius: 10px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                    z-index: 1000;
                }}
                .controls button {{
                    background: #667eea;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 14px;
                    transition: background 0.3s;
                }}
                .controls button:hover {{
                    background: #764ba2;
                }}
            </style>
        </head>
        <body>
            <h1>{title}</h1>
            <div class="controls">
                <button onclick="window.location.href='/'">← Назад к консоли</button>
                <button onclick="location.reload()">⟳ Обновить</button>
            </div>
            <div class="graph-container">
                {html}
            </div>
        </body>
        </html>
        """

        return full_html
