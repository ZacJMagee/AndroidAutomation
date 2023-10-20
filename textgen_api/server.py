import gc
from fastapi import FastAPI, HTTPException
from transformers import AutoModelForCausalLM, AutoTokenizer
import deepspeed

app = FastAPI()

print("Loading model...")

model_name_or_path = "/home/mrmagee/Applications/TextGenWebUI/text-generation-webui/models/TheBloke_Wizard-Vicuna-7B-Uncensored-GPTQ"
model = AutoModelForCausalLM.from_pretrained(model_name_or_path).cpu()

# Initialize DeepSpeed
model_engine, _, _, _ = deepspeed.initialize(model)

tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)

print("Model loaded successfully!")


@app.get("/generate/")
def generate_text(prompt: str):
    print(f"Received request with prompt: {prompt}")
    try:
        prompt_template = f'''A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions. USER: {prompt} ASSISTANT: '''
        input_ids = tokenizer(
            prompt_template, return_tensors='pt').input_ids.cuda()
        output = model_engine.generate(
            inputs=input_ids, temperature=0.7, do_sample=True, top_p=0.95, top_k=40, max_new_tokens=512)
        generated_text = tokenizer.decode(output[0])
        return {"generated_text": generated_text}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    print("Starting FastAPI server...")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
