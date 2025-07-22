import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
test_app = Flask(__name__)

# Import Google Agent ADK
try:
    from google_agent_adk import Agent
except ImportError:
    raise ImportError("Ensure 'google-agent-adk' is installed: pip install google-agent-adk")

# Initialize the Agent with project-specific settings
agent = Agent(
    project_id=os.getenv('PROJECT_ID'),
    region=os.getenv('REGION'),
    service_name=os.getenv('SERVICE_NAME')
)

@test_app.route('/agent-endpoint', methods=['POST'])
def agent_endpoint():
    """
    Main entrypoint for the agent: expects JSON with 'input' and optional 'parameters'.
    """
    payload = request.get_json(force=True)
    user_input = payload.get('input')
    params = payload.get('parameters', {})

    # Execute the agent logic
    result = agent.run(user_input, **params)

    return jsonify({'result': result})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    test_app.run(host='0.0.0.0', port=port, debug=True)

