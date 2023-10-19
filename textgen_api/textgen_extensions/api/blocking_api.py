from flask import Blueprint, request, jsonify
from modules.loaders import load_model

blocking_blueprint = Blueprint('blocking_api', __name__)

model_path = "/home/mrmagee/Applications/TextGenWebUI/text-generation-webui/models/TheBloke_Wizard-Vicuna-7B-Uncensored-GPTQ"
model = load_model(model_path)


@blocking_blueprint.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data['prompt']
    max_length = data.get('max_length', 50)
    response = model.generate_text(prompt, max_length)
    return jsonify({"response": response})
