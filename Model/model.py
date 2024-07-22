from pydantic import BaseModel

    
class ModelSearch(BaseModel):
    author: str
    task: str
    sort_by: str
    n_results: int

class Model(BaseModel):
    model_id: str
    
class ModelPrompt(BaseModel):
    prompt: str

class Variable(BaseModel):
    value: str
