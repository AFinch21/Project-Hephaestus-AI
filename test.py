from Utilities.ModelInference import ModelInference

model = ModelInference("TheBloke/Mistral-7B-Instruct-v0.1-GPTQ")

print(model.tokenizer.default_chat_template)

messages = [
    {"role": "user", "content": "What is your favourite condiment?"},
    {"role": "assistant", "content": "Well, I'm quite partial to a good squeeze of fresh lemon juice. It adds just the right amount of zesty flavour to whatever I'm cooking up in the kitchen!"},
    {"role": "user", "content": "Do you have mayonnaise recipes?"}
]
    
print(model.tokenizer.apply_chat_template(messages, tokenize=False))

print("\n\n*** Generate:")

model.infer(messages, stream=True)