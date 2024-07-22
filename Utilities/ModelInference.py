from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import  TextStreamer

class ModelInference:
    
    def __init__(self, model_id, model_kwargs=None, tokenizer_kwargs=None, streamer_kwargs=None, revision="main"):
        self.model_id = model_id
        self.revision = revision
        self.model_kwargs = model_kwargs if model_kwargs is not None else {}
        self.tokenizer_kwargs = tokenizer_kwargs if tokenizer_kwargs is not None else {}
        self.streamer_kwargs = streamer_kwargs if streamer_kwargs is not None else {}
        
        # Load model and tokenizer
        self.model = self.load_model()
        self.tokenizer = self.load_tokenizer()
        self.streamer = self.load_streamer()

    def load_model(self):
        model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            device_map="auto",
            trust_remote_code=False,
            revision=self.revision,
            **self.model_kwargs  # Pass additional keyword arguments
        )
        return model

    def load_tokenizer(self):
        tokenizer = AutoTokenizer.from_pretrained(
            self.model_id,
            **self.tokenizer_kwargs  # Pass additional keyword arguments
        )
        return tokenizer
    
    
    def load_streamer(self):
        
        streamer = TextStreamer(
            self.tokenizer, 
            **self.streamer_kwargs)
        
        return streamer
    
    def tokenize(self, prompt : str, **kwargs):
        
        input_ids = self.tokenizer(prompt, return_tensors='pt').input_ids.cuda()
        
        return input_ids
    
    def infer(self, prompt : dict, temperature : float = 0.5, top_p : float = 0.95, top_k : float = 40, max_new_tokens : int = 256, stream : bool = False, add_generation_prompt : bool = False, **kwargs):
        
        prompt_template =  self.tokenizer.apply_chat_template(prompt, tokenize=False)
        
        print(prompt_template)
        
        input_ids = self.tokenizer(prompt_template, return_tensors='pt').input_ids.cuda()

        
        output = self.model.generate(
            inputs=input_ids, 
            temperature=temperature, 
            do_sample=True, 
            top_p=top_p, 
            top_k=top_k, 
            max_new_tokens=max_new_tokens, 
            streamer=self.streamer if stream else None,
            **kwargs
            )
        
        return self.tokenizer.decode(output[0])