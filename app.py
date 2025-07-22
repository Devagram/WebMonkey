import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
test_app = Flask(__name__)


@test_app.route('/agent-endpoint', methods=['POST'])
def agent_endpoint():
    """
    Main entrypoint for the agent: expects JSON with 'input' and optional 'parameters'.
    """
    payload = request.get_json(force=True)
    user_input = payload.get('input')
    params = payload.get('parameters', {})

    # Execute the agent logic

    return jsonify({'result': "Processed input: " + user_input, 'parameters': params})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    test_app.run(host='0.0.0.0', port=port, debug=True)

