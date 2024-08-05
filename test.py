import asyncio
from nicegui import ui
from Frontend.UIFunctions.UIFunctions import search_models, get_model, infer_from_model, get_model_stats, load_model
import aiohttp



global_state = {
    "current_model": "No Model Loaded",
    "chat_log": [],
    "vram_usage": 0,
    "ram_usage": 0,
    "vram_total": 0,
    "ram_total": 0
}

print(global_state)

initial_stats = get_model_stats()
global_state["vram_total"] = initial_stats['vram_total']
global_state["ram_total"] = initial_stats['ram_total']
global_state["vram_usage"] = initial_stats['vram_used']
global_state["ram_usage"] = initial_stats['ram_used']

@ui.refreshable
def circular_charts() -> None:
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

def update_circular_charts():
    stats = get_model_stats()
    print(stats)
    global_state["vram_usage"] = stats['vram_used']
    global_state["ram_usage"] = stats['ram_used']
    circular_charts.refresh()
    return global_state["vram_usage"], global_state["ram_usage"]

async def load_and_set_model(selected_model):
    await load_model(selected_model)
    update_circular_charts()

def do_something_else() -> None:
    print("Doing something")

async def managed_functions():
    await load_and_set_model("TheBloke/Mistral-7B-Instruct-v0.1-GPTQ")
    do_something_else()

@ui.page('/main')
def main_page():
    circular_charts()
    ui.button('Add random number', on_click=lambda: asyncio.ensure_future(managed_functions()))

ui.run()