## mcp_server.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List
import logging



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class ContextNode(BaseModel):
    id: str
    type: str
    name: str
    description: str
    content: dict

context_store: Dict[str, ContextNode] = {}

@app.post("/register")
def register_context(node: ContextNode):
    logger.info(f"[MCP] Registering context node: {node.id}")
    if node.id in context_store:
        raise HTTPException(status_code=400, detail="Node already exists")
    context_store[node.id] = node
    return {"message": "Registered", "node": node}

@app.get("/context/{node_id}")
def get_context(node_id: str):
    logger.info(f"[MCP] Resolving context node: {node_id}")
    node = context_store.get(node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Context node not found")
    return node

@app.post("/resolve")
def resolve_bundle(node_ids: List[str]):
    resolved = []
    for node_id in node_ids:
        node = context_store.get(node_id)
        if not node:
            raise HTTPException(status_code=404, detail=f"Node {node_id} not found")
        resolved.append(node)
    return {"bundle": resolved}


@app.get("/context")
def list_all_context_nodes():
    logger.info("[MCP] Listing all registered context nodes")
    return list(context_store.values())
