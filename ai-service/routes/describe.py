from flask import Blueprint, request, jsonify
from datetime import datetime, timezone
import json
import os
from services.groq_client import GroqClient

describe_bp = Blueprint('describe', __name__)
groq_client = GroqClient()

def load_prompt():
    prompt_path = os.path.join(os.path.dirname(__file__), '../prompts/primary_prompt.txt')
    with open(prompt_path, 'r') as f:
        return f.read()

@describe_bp.route('/describe', methods=['POST'])
def describe():
    """
    Day 3 Task: POST /describe 
    validates input, loads prompt, calls Groq, returns JSON with generated_at
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input, JSON payload required"}), 400

    prompt_template = load_prompt()
    prompt = prompt_template.replace('{input_data}', json.dumps(data))
    
    response_content = groq_client.generate_response(prompt, is_json=True)
    
    try:
        parsed_response = json.loads(response_content)
        parsed_response['generated_at'] = datetime.now(timezone.utc).isoformat()
        return jsonify(parsed_response), 200
    except Exception as e:
        return jsonify({"is_fallback": True, "error": "Failed to parse AI response"}), 500
