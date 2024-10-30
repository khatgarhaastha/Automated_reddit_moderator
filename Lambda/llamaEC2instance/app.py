from transformers import LlamaForCausalLM, LlamaTokenizer
from flask import Flask, request, jsonify
import torch

app = Flask(__name__)

# Load the Llama model and tokenizer
model_name = "meta-llama/Llama-2-7b-chat-hf"  # Adjust this to your preferred model
tokenizer = LlamaTokenizer.from_pretrained(model_name)
model = LlamaForCausalLM.from_pretrained(model_name)

# Define the API endpoint
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json.get('input_text', '')
    inputs = tokenizer(data, return_tensors="pt").to("cuda")  # Move to GPU if available
    
    with torch.no_grad():
        outputs = model.generate(inputs["input_ids"], max_length=100, num_return_sequences=1)
    
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return jsonify({'response': generated_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
