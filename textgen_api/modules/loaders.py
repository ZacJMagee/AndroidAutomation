# loaders.py

from transformers import AutoTokenizer
from .models import AutoGPTQ


def load_autogptq_model(model_path):
    return AutoGPTQ(model_path)


def load_autogptq_tokenizer(model_path):
    return AutoTokenizer.from_pretrained(model_path)
