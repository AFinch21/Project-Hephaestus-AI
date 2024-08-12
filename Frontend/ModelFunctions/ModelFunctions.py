from APIRequests.APIRequests import search_models, load_model, get_model, infer_from_model, get_model_stats
from UIFunctions.UIFunctions import *


async def load_and_set_model(selected_model, global_state):
    await load_model(selected_model)
    update_model_stats(global_state)