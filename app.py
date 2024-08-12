from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from Utilities.HFManager import HFManager
from Utilities.ModelInference import ModelInference
from Model.model import Model, ModelSearch, ModelPrompt
from Utilities import ModelStats
# Define your model class, as it seems to be external and not described


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model_id = 'No Model Loaded'
model = None

hf = HFManager()


@app.get('/')
def read_root():
    return {'Hello': 'World'}

@app.get("/get_model/")
async def get_model():
    global model_id
    
    return {"Model": model_id}

@app.get("/get_model_stats/")
async def get_model_stats():
    
    ms = ModelStats.ModelStatistics(model_id)
    
    graphic, total_vram, free_vram, used_vram = ms.get_vram()
    graphic, total_ram, free_ram, used_ram = ms.get_ram()
    
    return {
        "Model": model_id,
        "vram_total" : total_vram,
        "vram_used" : used_vram,
        "vram_free" : free_vram,
        "ram_total" : total_ram,
        "ram_used" : used_ram,
        "ram_free" : free_ram
        }
    
@app.get("/get_model_config/")
async def get_model_config():
    
    global model
    
    config = model.get_model_config()
    
    print(config)
    
    return config

@app.post("/search_models/")
async def search_models(model_search: ModelSearch):
    
    model_list = hf.search_models(model_search.author, model_search.sort_by, model_search.n_results)
    
    return {"Results": model_list}

@app.post("/load_model/")
async def load_model(model_object: Model):
    global model_id
    global model
    
    print("Loading Model:", model_object.model_id)
    model = ModelInference(model_object.model_id)
    model_id = model_object.model_id
            
    return {
        "Model_id": model_id
        }

@app.post("/infer_from_model/")
async def infer_from_model(prompt: ModelPrompt):
    
    global model
    
    print("INCOMING PROMPT:",prompt.prompt)
    
    messages = [
        {"role": "user", "content": f"{prompt.prompt}"}
    ]
    
    response = model.infer(messages, stream=True)
    
    return {
        "Response": response
        }

