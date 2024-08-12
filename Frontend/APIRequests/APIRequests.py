import requests
import httpx
import json
import aiohttp

def get_model():

    # # API endpoint
    url = 'http://localhost:8081/get_model/'
    
    # Making the POST request
    response = requests.get(url)
    
    # Checking if the request was successful
    if response.status_code == 200:
        response = json.loads(response.text)
        return response
    else:
        print('Bad response')
        return
    
def get_model_stats():

    # # API endpoint
    url = 'http://localhost:8081/get_model_stats/'
    
    # Making the POST request
    response = requests.get(url)
    
    # Checking if the request was successful
    if response.status_code == 200:
        response = json.loads(response.text)
        return response
    else:
        print('Bad response')
        return 
    
def get_model_config():

    # # API endpoint
    url = 'http://localhost:8081/get_model_config/'
    
    # Making the POST request
    response = requests.get(url)
    
    # Checking if the request was successful
    if response.status_code == 200:
        response = json.loads(response.text)
        return response
    else:
        print('Bad response')
        return 

def search_models(author=None, sort_by='downloads', n_results=5):
    global model_list

    # # API endpoint
    url = 'http://localhost:8081/search_models/'
    
    # Sample item data
    model_search_params = {
        'author': author,
        'task': 'text-generation',
        'sort_by': sort_by.lower(),
        'n_results': n_results,
    }

    # Making the POST request
    response = requests.post(url, json=model_search_params)
    
    # Checking if the request was successful
    if response.status_code == 200:
        response = json.loads(response.text)
        model_list = [model for model in response['Results']]
        return model_list
    else:
        print('Bad response')
        model_list = []
        return model_list

async def load_model(model_id):
    if model_id is None:
        model_id = 'No Model Loaded'
    
    # API endpoint
    url = 'http://localhost:8081/load_model/'

    # Parameters to be sent
    model_load_params = {
        'model_id': model_id,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=model_load_params) as response:
            if response.status == 200:
                response_data = await response.json()
                print("Model Load Response:\n", response_data)
                return response_data
            else:
                print('Bad response')
                return None
    


async def infer_from_model(prompt):
    url = 'http://localhost:8081/infer_from_model/'
    model_load_params = {
        'prompt': prompt,
    }

    # Create an asynchronous client
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=model_load_params, timeout=60)

    if response.status_code == 200:
        response = response.json()
        print("Model Load Response:\n", response)
        return response
    else:
        print('Bad response')
        return
    