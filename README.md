# Project-Hephaestus
Repo for Project-Hephaestus - a local LLM testing app.

# Managing the .venv

So I've really messed up the .venv for this project - partly because a bunch of other repositories wont play ball. You (I mean YOU Andrew not anyone reading this) need to specify the .venv you want to use. 

So in this case the command needs to specify the path to the .venv - then use pip within that - i.e.:

e:\projects\Project-Hephaestus-AI\.venv\scripts\python.exe -m pip install langchain_openai

Then to run your API and frontent - you need to run them within that specific .venv:

