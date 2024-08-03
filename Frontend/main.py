from fastapi import FastAPI
from nicegui import app, ui
from pydantic import BaseModel
import requests
from nicegui import ui
import json
from UIFunctions.UIFunctions import search_models, load_model, get_model, infer_from_model
from langchain_openai import ChatOpenAI
from log_callback_handler import NiceGuiLogElementCallbackHandler
import torch
import psutil


global_state = {
    "current_model": None,
    "chat_log" : [],
    "vram_usage" : 0,
    "ram_usage" : 0
    } 

@ui.page('/main') 
def main_page(): 
     
    global_state["current_model"] = get_model()['Model'] 
    print(global_state["current_model"]) 
    model_list = [] 
    
    ui.html('<h1 style="font-size:26px;">Model Loaded:</h1>')
    ui.label(global_state["current_model"])
    
    with ui.grid(columns='1fr 1fr').classes('w-full gap-0'):

        with ui.row():
            ui.label('1fr')
            chart = ui.highchart({
                'title': False,
                'chart': {'type': 'bar'},
                'xAxis': {'categories': ['Memory Usage']},

                'series': [
                    {'name': 'VRAM', 'data': [torch.cuda.mem_get_info()[0] / 1024 ** 3]},
                    {'name': 'RAM', 'data': [psutil.virtual_memory().available / 1024 ** 3]},
                ],
            }).classes('w-full h-64')
            
        with ui.grid(columns='1fr 1fr').classes('w-full gap-0'):
            with ui.row():
                ui.label('Available RAM:')
                ram_total = psutil.virtual_memory().total / 1024 ** 3
                ram_ui = ui.circular_progress(
                    min=0.0, 
                    max=float("{:.2f}".format(ram_total)), 
                    value=global_state['ram_usage'],
                    size='200px'
                    )
            with ui.row():
                ui.label('Available VRAM:')
                vram_total = torch.cuda.mem_get_info()[1] / 1024 ** 3
                vram_ui = ui.circular_progress(
                    min=0.0, 
                    max=float("{:.2f}".format(vram_total)), 
                    value=global_state['vram_usage'],
                    size='200px'
                    )
                
        ui.label('test').classes('border p-1')

    def get_vram_ram_usage():

        # Update RAM usage
        ram_total = psutil.virtual_memory().total / 1024 ** 3
        ram_free = psutil.virtual_memory().available / 1024 ** 3


        # Update VRAM usage
        vram_free = torch.cuda.mem_get_info()[0] / 1024 ** 3
        vram_total = torch.cuda.mem_get_info()[1] / 1024 ** 3
        
        global_state['vram_usage'] = vram_total - vram_free
        global_state['ram_usage'] = ram_total - ram_free
        
        vram_ui.value = global_state['vram_usage']
        ram_ui.value = global_state['ram_usage']
        
        print(global_state)
        
        return global_state['vram_usage']

    def load_and_set_model(selected_model): 
        load_model(selected_model)
    
        global_state["current_model"] = get_model()['Model']
        get_vram_ram_usage()

        
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


    with ui.right_drawer(fixed=False).style('background-color: #ebf1fa').props('width=600') as right_drawer:
        
        async def send() -> None:
            question = text.value
            text.value = ''

            with message_container:
                ui.chat_message(text=question, name='You', sent=True)
                response_message = ui.chat_message(name='LLM', sent=False)
                # Display the spinner inside the response message
                with response_message:
                    spinner = ui.spinner(type='dots')

            response = await call_model(question)  # Ensure this is an asynchronous call

            # Remove spinner and display the response
            response_message.clear()
            
            # Display the actual response
            with response_message:
                ui.label(response['Response'])
            
            # Scroll down to the latest message
            ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')

        async def call_model(question: str):
            # Call the model and wait for the response
            raw_response = await infer_from_model(question)
        
            return raw_response

        # Inline CSS for anchor tags
        ui.add_css(r'a:link, a:visited {color: inherit !important; text-decoration: none; font-weight: 500}')

        # Expand content to footer
        ui.query('.q-page').classes('flex')
        ui.query('.nicegui-content').classes('w-full')

        # Tabs for Chat and Logs
        with ui.tabs().classes('w-full') as tabs:
            chat_tab = ui.tab('Chat')
            logs_tab = ui.tab('Logs')
        with ui.tab_panels(tabs, value=chat_tab).classes('w-full max-w-2xl mx-auto flex-grow items-stretch'):
            message_container = ui.tab_panel(chat_tab).classes('items-stretch')
            with ui.tab_panel(logs_tab):
                log = ui.log().classes('w-full h-full')

        # Text input and Send button
        with ui.row().classes('w-full no-wrap items-center'):
            text = ui.input(placeholder="Type your prompt here...").props('rounded outlined input-class=mx-3').classes('w-full self-center').on('keydown.enter', send)  
        
    with ui.footer().style('background-color: #3874c8'):
        ui.label('FOOTER')
    
         

ui.link('Visit other page', main_page)

ui.run()