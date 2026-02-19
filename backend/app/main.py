from fastapi import FastAPI, UploadFile, File
from PIL import Image
import io
import os
from app.utils import load_landmarks
from app.model import get_embedding
from app.search import VectorSearch
from app.graph import CampusGraph
from app.utils import build_or_load_cache
from app.utils import path_to_instructions


app = FastAPI()

search_engine = None
campus_graph = None



@app.on_event("startup")
def startup():

    global search_engine
    global campus_graph
    global landmarks
    from app.utils import build_or_load_cache
    landmarks = load_landmarks()


    

    image_root = "data/images"

    print("\nPreparing embedding cache...\n")

    embeddings, ids = build_or_load_cache(image_root)

    if not embeddings:
        raise RuntimeError("No images found in data/images")

    dim = len(embeddings[0])
    search_engine = VectorSearch(dim)
    search_engine.add(embeddings, ids)

    print("\nFAISS index ready with", len(ids), "images\n")

    campus_graph = CampusGraph()
    print("Campus graph loaded\n")



@app.get("/")
def root():
    return {"message": "Campus Navigation Backend Running"}


@app.post("/locate")
async def locate(file: UploadFile = File(...)):

    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    emb = get_embedding(image)

    result = search_engine.search(emb)

    return {"matched_image": result}


@app.post("/route")
async def route(
    file: UploadFile = File(...),
    destination: str = "D.jpg"
):

    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    emb = get_embedding(image)

    current = search_engine.search(emb)[0]

    path = campus_graph.shortest_path(current, destination)

    return {
        "current": current,
        "destination": destination,
        "path": path
    }


@app.post("/navigate")
async def navigate(
    file: UploadFile = File(...),
    destination_name: str = "Gate"
):

    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    emb = get_embedding(image)

    current = search_engine.search(emb)[0]

    if destination_name not in landmarks:
        return {"error": "Unknown destination"}

    destination = landmarks[destination_name]

    path = campus_graph.shortest_path(current, destination)

    instructions = path_to_instructions(path, landmarks)


    return {
        "current_frame": current,
        "destination_name": destination_name,
        "path": path,
        "instructions": instructions
    }

