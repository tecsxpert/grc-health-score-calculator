import os
from flask import Flask, jsonify
from routes.describe import describe_bp
from routes.recommend import recommend_bp
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(describe_bp)
app.register_blueprint(recommend_bp)

# Health endpoint placeholder (Day 7 task)
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
