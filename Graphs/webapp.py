from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn
import os
import uuid
from datetime import datetime
import webbrowser
import threading
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from graph_generator import GraphGenerator

app = FastAPI(title="Graph Analysis Web App")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

static_dir = os.path.join(BASE_DIR, "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

templates_dir = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=templates_dir)

generated_dir = os.path.join(BASE_DIR, "generated")
os.makedirs(generated_dir, exist_ok=True)

graph_gen = GraphGenerator()


class Node(BaseModel):
    id: str
    label: str
    type: str = "entity"
    properties: Dict[str, Any] = {}


class Edge(BaseModel):
    source: str
    target: str
    label: Optional[str] = None
    properties: Dict[str, Any] = {}


class GraphData(BaseModel):
    nodes: List[Node]
    edges: List[Edge]
    name: Optional[str] = None


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        "console.html",
        {"request": request, "title": "Graph Constructor"}
    )


@app.post("/api/generate")
async def generate_graph(data: GraphData):
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        filename = f"graph_{timestamp}_{unique_id}.html"
        filepath = os.path.join(generated_dir, filename)

        nodes_data = []
        for n in data.nodes:
            node_dict = {
                "id": n.id,
                "label": n.label,
                "type": n.type
            }
            if n.properties:
                node_dict.update(n.properties)
            nodes_data.append(node_dict)

        edges_data = []
        for e in data.edges:
            edge_dict = {
                "from": e.source,
                "to": e.target
            }
            if e.label:
                edge_dict["label"] = e.label
            if e.properties:
                edge_dict.update(e.properties)
            edges_data.append(edge_dict)

        html_content = graph_gen.generate_interactive_graph(
            nodes=nodes_data,
            edges=edges_data,
            title=data.name or f"Graph Analysis {timestamp}"
        )

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)

        return {
            "success": True,
            "filename": filename,
            "url": f"/view/{filename}",
            "message": f"Граф успешно создан: {filename}"
        }

    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/view/{filename}", response_class=HTMLResponse)
async def view_graph(filename: str):
    filepath = os.path.join(generated_dir, filename)
    if not os.path.exists(filepath):
        return HTMLResponse(
            content=f"<h1>File not found</h1><p>{filename}</p>",
            status_code=404
        )

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    return HTMLResponse(content=content)


@app.get("/api/files")
async def list_files():
    files = []
    if os.path.exists(generated_dir):
        for f in os.listdir(generated_dir):
            if f.endswith(".html"):
                filepath = os.path.join(generated_dir, f)
                stats = os.stat(filepath)
                files.append({
                    "name": f,
                    "created": datetime.fromtimestamp(stats.st_ctime).isoformat(),
                    "size": stats.st_size,
                    "url": f"/view/{f}"
                })

    return {"files": sorted(files, key=lambda x: x["created"], reverse=True)}


def open_browser():
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:8080")


if __name__ == "__main__":
    print("""
        ╔═══════════════════════════════════════════════════════════════╗
        ║  ███████╗██╗  ██╗██╗██████╗  ██████╗ ███╗   ███╗██╗   ██╗     ║
        ║  ██╔════╝██║  ██║██║██╔══██╗██╔═══██╗████╗ ████║██║   ██║     ║
        ║  ███████╗███████║██║██████╔╝██║   ██║██╔████╔██║██║   ██║     ║
        ║  ╚════██║██╔══██║██║██╔══██╗██║   ██║██║╚██╔╝██║██║   ██║     ║
        ║  ███████║██║  ██║██║██║  ██║╚██████╔╝██║ ╚═╝ ██║╚██████╔╝     ║
        ║  ╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝ ╚═════╝      ║
        ║                                                               ║
        ╚═══════════════════════════════════════════════════════════════╝
        """)
    print("System initialized...")
    print("🌐 Listening on: http://127.0.0.1:8080")

    threading.Thread(target=open_browser, daemon=True).start()
    uvicorn.run("webapp:app", host="127.0.0.1", port=8080, reload=True)