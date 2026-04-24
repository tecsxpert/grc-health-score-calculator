from flask import Blueprint, request, jsonify
import json
from services.groq_client import GroqClient

recommend_bp = Blueprint('recommend', __name__)
groq_client = GroqClient()

@recommend_bp.route('/recommend', methods=['POST'])
def recommend():
    """
    Day 4 Task: POST /recommend
    Returns 3 recommendations as JSON array, each with action_type, description, priority
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input, JSON payload required"}), 400

    prompt = (
        f"Given the following health data: {json.dumps(data)}\n"
        "Provide exactly 3 actionable health recommendations. "
        "Return ONLY a JSON object containing a 'recommendations' array. "
        "Each recommendation must be an object with keys: 'action_type' (e.g., Lifestyle, Diet, Medical), "
        "'description', and 'priority' (High, Medium, Low)."
    )
    
    response_content = groq_client.generate_response(prompt, is_json=True)
    
    try:
        parsed_response = json.loads(response_content)
        # Ensure it always has recommendations array
        if 'recommendations' not in parsed_response:
            parsed_response = {"recommendations": [parsed_response]}
        return jsonify(parsed_response), 200
    except Exception as e:
        return jsonify({"is_fallback": True, "recommendations": []}), 500
