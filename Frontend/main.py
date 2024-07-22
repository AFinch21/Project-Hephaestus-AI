from fastapi import FastAPI
from nicegui import app, ui
from pydantic import BaseModel
import requests
from nicegui import ui
import json
from UIFunctions.UIFunctions import search_models, load_model, get_model, infer_from_model


global_state = {"current_model": None} 

@ui.page('/main') 
def main_page(): 
     
    global_state["current_model"] = get_model()['Model'] 
    print(global_state["current_model"]) 
    model_list = [] 
    
    ui.html('<h1 style="font-size:26px;">Model Loaded:</h1>')
    ui.label(global_state["current_model"])
    
    prompt = ui.input(
                label='hello...', 
                placeholder='start typing',
                validation={'Input too long': lambda value: len(value) < 20}).classes('w-60')
    ui.button('infer...', icon='rocket', on_click=lambda: infer_from_model(prompt.value)).classes('w-60')

    def load_and_set_model(selected_model): 
        load_model(selected_model)
        print("Old model is:", global_state["current_model"]) 
        global_state["current_model"] = get_model()['Model'] 
        print("Current model is:", global_state["current_model"]) 
        return global_state["current_model"] 
    
    with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
        ui.label('Project Hephaestus')

        ui.button(on_click=lambda: right_drawer.toggle(), icon='menu').props('flat color=white')
    with ui.left_drawer(top_corner=True, bottom_corner=True).style('background-color: #d7e3f4'):
        
        ui.html('<h1 style="font-size:26px;">Model Search</h1>')
        
        
        ui.html('<h4 style="font-size:20px;">Model Creator</h4>')
        with ui.row():
            # Some of the most popular options eyeballing huggingface
            options = ['meta-llama', 'microsoft', 'mistralai', 'TheBloke', 'Groq', 'openai-community', 'google', 'tiiuae', 'unsloth']
            model_name = ui.input(
                label='meta-llama...', 
                placeholder='start typing',
                autocomplete=options,
                validation={'Input too long': lambda value: len(value) < 20}).classes('w-60')
            n_results_drop = ui.select(
                [5, 10, 20], 
                value=5,
                label='n-Results').classes('w-60')

        # parameter slider
        ui.html('<h4 style="font-size:20px;">Model Parameters</h4>')
        ui.html('<br>')
        ui.range(
            min=1, 
            max=70, 
            value={'min': 3, 'max': 13}).props('label-always snap label-color="secondary" right-label-text-color="black"').classes('w-60')
        
        ui.html('<h4 style="font-size:20px;">Sort By...</h4>')
        sort_by_radio = ui.radio(['Downloads', 'Likes'], value=1).props('inline')
        

        # search button
        search_button = ui.button('Search models', on_click=lambda: model_selector.set_options(search_models(model_name.value, sort_by_radio.value, n_results_drop.value)), icon='search').classes('w-60')

        model_selector = ui.select(model_list).classes('w-60')
        
        # Button creation
        ui.button('Load Model...', icon='rocket', on_click=lambda: load_and_set_model(model_selector.value)).classes('w-60')


    with ui.right_drawer(fixed=False).style('background-color: #ebf1fa').props('bordered').classes('w-200') as right_drawer:
        ui.label('RIGHT DRAWER')
        
    with ui.footer().style('background-color: #3874c8'):
        ui.label('FOOTER')
    
         

ui.link('Visit other page', main_page)

ui.run()