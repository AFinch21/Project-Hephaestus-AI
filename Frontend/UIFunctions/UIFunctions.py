from nicegui import app, ui
from APIRequests.APIRequests import search_models, load_model, get_model, infer_from_model, get_model_stats, get_model_config
from UIFunctions.UIFunctions import *


async def load_and_set_model(selected_model):
    await load_model(selected_model)
    update_model_stats()

@ui.refreshable
def circular_charts(global_state) -> None:
    with ui.row():
        ram_ui = ui.circular_progress(
        min=0.0, 
        max=global_state['ram_total'], 
        value=global_state["ram_usage"],
        size='200px'
        )
    with ui.row():
        vram_ui = ui.circular_progress(
        min=0.0, 
        max=global_state['vram_total'], 
        value=global_state["vram_usage"],
        size='200px'
        )

@ui.refreshable
def model_name_display(global_state) -> None:
    ui.label(global_state["current_model"])

def update_model_stats(global_state):
    stats = get_model_stats()
    model_config = get_model_config()
    
    print(stats)
    
    # First lets update the cicular charts
    global_state["vram_usage"] = stats['vram_used']
    global_state["ram_usage"] = stats['ram_used']
    circular_charts.refresh()
    
    # Now the model title
    global_state["current_model"] = stats['Model']
    model_name_display.refresh()
    
    return global_state["vram_usage"], global_state["ram_usage"], global_state["current_model"], model_config