# models.py

from transformers import AutoModelForCausalLM


class AutoGPTQ:
    def __init__(self, model_path):
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path).to('cuda')

    def forward(self, input_ids):
        return self.model.generate(input_ids)
