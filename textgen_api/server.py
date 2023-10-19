from modules.loaders import load_autogptq_model, load_autogptq_tokenizer
from fastapi import FastAPI, HTTPException, Depends, Body
import gc
from fastapi import FastAPI, HTTPException
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = FastAPI()


print("loading Model...")
model_name_or_path = "/home/mrmagee/Applications/TextGenWebUI/text-generation-webui/models/TheBloke_Wizard-Vicuna-7B-Uncensored-GPTQ"
model = AutoModelForCausalLM.from_pretrained(
    model_name_or_path, torch_dtype=torch.float16).cpu()  # Load model in 8-bit mode to CPU first
gc.collect()  # Explicitly run garbage collection
model = model.to('cuda')  # Now move the model to GPU
tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)
print("Model Loaded successfully!!!")  # server.py


model_path = "/home/mrmagee/Applications/TextGenWebUI/text-generation-webui/models/TheBloke_Wizard-Vicuna-7B-Uncensored-GPTQ"
model = load_autogptq_model(model_path)
tokenizer = load_autogptq_tokenizer(model_path)

app = FastAPI()


@app.post("/generate")
def generate_text(prompt: str, max_length: int = 50):
    print(f"Received request with prompt: {prompt}")
    try:
        input_ids = tokenizer.encode(prompt, return_tensors='pt').to('cuda')
        output = model.forward(input_ids)
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
        return {"response": generated_text}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    print("Starting FastAPI server...")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


@app.get("/generate/")
def generate_text(prompt: str):
    try:
        prompt_template = f'''A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions. USER: {prompt} ASSISTANT: '''
        input_ids = tokenizer(
            prompt_template, return_tensors='pt').input_ids.cuda()
        output = model.generate(inputs=input_ids, temperature=0.7,
                                do_sample=True, top_p=0.95, top_k=40, max_new_tokens=512)
        generated_text = tokenizer.decode(output[0])
        return {"generated_text": generated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
